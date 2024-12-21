import subprocess
import sys
import time
import os
from rx import operators as ops

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput", "rx"])
        print("Libraries successfully installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing libraries: {e}")
        sys.exit(1)

def log_event_to_file(event):
    try:
        log_path = os.path.join(os.path.dirname(__file__), "output", "keyboard_events.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(event + "\n")
        print(event)
    except Exception as e:
        print(f"Error writing to file: {e}")

def handle_error(error):
    print(f"An error occurred: {error}")

def run_tracker():
    from src.keyboard_tracker import KeyboardTracker
    tracker = KeyboardTracker()

    tracker.subject.pipe(
        ops.do_action(log_event_to_file),  
        ops.catch(handle_error) 
    ).subscribe()

    tracker.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Terminating program...")
        tracker.stop()

def main():
    install_requirements()
    run_tracker()

if __name__ == "__main__":
    main()
