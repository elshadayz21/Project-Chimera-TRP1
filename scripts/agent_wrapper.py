#!/usr/bin/env python3
"""
Agent wrapper: ensures triggers are called before running analysis or actions.
Usage:
  python scripts/agent_wrapper.py --message "Brief message" [--performance "details"] [--run "command"]

Behavior:
- Calls the local passage trigger shim (does not print output).
- If --performance is provided, calls the performance trigger shim and captures the Analysis Feedback block, printing it (wrapped per spec).
- Only after triggers complete successfully will it run the provided command (if any) or print READY.
"""
import argparse
import subprocess
import sys
import shlex
import os

SCRIPT_DIR = os.path.dirname(__file__)
LOG_SHIM = os.path.join(SCRIPT_DIR, 'log_triggers.py')

parser = argparse.ArgumentParser()
parser.add_argument('--message', required=True)
parser.add_argument('--performance', help='Optional performance details (triggers performance log)')
parser.add_argument('--run', help='Optional shell command to run after triggers')
args = parser.parse_args()

# Step 1: Run passage trigger
pass_cmd = [sys.executable, LOG_SHIM, '--type', 'passage', '--message', args.message]
res = subprocess.run(pass_cmd, capture_output=True, text=True)
if res.returncode != 0:
    print('ERROR: passage trigger failed', file=sys.stderr)
    print(res.stderr, file=sys.stderr)
    sys.exit(2)

# Step 2: Optional performance trigger
if args.performance:
    perf_cmd = [sys.executable, LOG_SHIM, '--type', 'performance', '--message', args.message, '--details', args.performance]
    res = subprocess.run(perf_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print('ERROR: performance trigger failed', file=sys.stderr)
        print(res.stderr, file=sys.stderr)
        sys.exit(3)
    # The shim prints the Analysis Feedback block already; ensure it's present
    if 'Analysis Feedback:' not in res.stdout:
        print('ERROR: performance trigger output missing Analysis Feedback block', file=sys.stderr)
        print(res.stdout)
        sys.exit(4)
    # Print the performance feedback exactly as produced (includes the required markers)
    print(res.stdout.strip())

# Step 3: Run the user command or signal ready
if args.run:
    print('Running command after triggers: {}'.format(args.run))
    # Use shell to allow complex commands
    proc = subprocess.run(args.run, shell=True)
    sys.exit(proc.returncode)
else:
    print('READY')
    sys.exit(0)
