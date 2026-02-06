#!/usr/bin/env python3
"""
Chimera Docker Management Script
Cross-platform alternative to Makefile for Windows users.

Usage:
    python chimera.py setup   - Build the Docker image
    python chimera.py test    - Run tests in Docker
    python chimera.py shell   - Open interactive shell
    python chimera.py clean   - Remove Docker image
"""

import sys
import subprocess
import os

IMAGE_NAME = "chimera:dev"

def run_command(cmd, shell=False):
    """Execute a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=shell, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}")
        return False

def build():
    """Build the Docker image."""
    print(f"Building Docker image '{IMAGE_NAME}'...")
    return run_command(["docker", "build", "-t", IMAGE_NAME, "."])

def setup():
    """Build the Docker image (alias for build)."""
    if build():
        print(f"\n✅ Setup complete: Docker image '{IMAGE_NAME}' built with project dependencies.")
        return True
    return False

def test():
    """Run tests inside Docker container."""
    print("Running tests inside Docker...")
    pwd = os.getcwd()
    return run_command([
        "docker", "run", "--rm",
        "-v", f"{pwd}:/app",
        "-w", "/app",
        IMAGE_NAME,
        "pytest", "-q"
    ])

def shell():
    """Open an interactive bash shell in the container."""
    print("Starting shell inside Docker (interactive)...")
    pwd = os.getcwd()
    return run_command([
        "docker", "run", "--rm", "-it",
        "-v", f"{pwd}:/app",
        "-w", "/app",
        IMAGE_NAME,
        "/bin/bash"
    ])

def clean():
    """Remove the Docker image."""
    print(f"Removing image '{IMAGE_NAME}'...")
    return run_command(["docker", "rmi", "-f", IMAGE_NAME])

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nAvailable commands: setup, build, test, shell, clean")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    commands = {
        "setup": setup,
        "build": build,
        "test": test,
        "shell": shell,
        "clean": clean,
    }
    
    if command not in commands:
        print(f"Unknown command: {command}")
        print("Available commands: setup, build, test, shell, clean")
        sys.exit(1)
    
    success = commands[command]()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
