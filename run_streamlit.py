"""
Launcher: find a free port (8501-8520), start Streamlit, and open the browser.
Run from project root: python run_streamlit.py
"""
import subprocess
import webbrowser
import time
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_PATH = os.path.join(SCRIPT_DIR, "app.py")
PORT_START = 8501
PORT_END = 8520
WAIT_SEC = 4

def main():
    os.chdir(SCRIPT_DIR)
    print("Starting Golden Ratio Quantum Pulse Visualizer...")
    print()
    for port in range(PORT_START, PORT_END + 1):
        print(f"Trying port {port}...", end=" ", flush=True)
        proc = subprocess.Popen(
            [
                sys.executable, "-m", "streamlit", "run", APP_PATH,
                "--server.port", str(port),
                "--server.headless", "true",
            ],
            cwd=SCRIPT_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(WAIT_SEC)
        if proc.poll() is not None:
            print("in use.")
            continue
        url = f"http://localhost:{port}"
        print("started.")
        print(f"Opening {url} in your browser...")
        webbrowser.open(url)
        proc.wait()
        return
    print(f"\nNo free port in {PORT_START}-{PORT_END}. Close other apps or try a higher port.")
    sys.exit(1)

if __name__ == "__main__":
    main()
