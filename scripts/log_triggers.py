import argparse
import json
import os
import datetime

LOG_DIR = ".tenx_triggers"
LOG_FILE = os.path.join(LOG_DIR, "logs.json")

def ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def load_logs():
    ensure_log_dir()
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_log(entry):
    logs = load_logs()
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def handle_passage(message):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": "passage",
        "message": message
    }
    save_log(entry)
    # Silent success for passage trigger

def handle_performance(message, details):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": "performance",
        "message": message,
        "details": details
    }
    save_log(entry)
    
    print("\n*****************************************")
    print("Analysis Feedback:")
    print(f"Performance Alert: {message}")
    print(f"Details: {details}")
    print("*****************************************\n")

def main():
    parser = argparse.ArgumentParser(description="Local shim for trigger logging.")
    parser.add_argument("--type", choices=["passage", "performance"], required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--details", default="")
    
    args = parser.parse_args()
    
    if args.type == "passage":
        handle_passage(args.message)
    elif args.type == "performance":
        handle_performance(args.message, args.details)

if __name__ == "__main__":
    main()
