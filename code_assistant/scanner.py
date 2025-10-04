import subprocess
from .config import BANDIT_TIMEOUT

def scan_file(filepath: str):
    """
    Runs Bandit to scan a Python file for vulnerabilities
    """
    print(f"[INFO] Scanning {filepath} with Bandit...")
    try:
        result = subprocess.run(
            ["bandit", "-r", filepath],
            capture_output=True,
            text=True,
            timeout=BANDIT_TIMEOUT
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"[WARN] Bandit reported issues in {filepath}")
    except Exception as e:
        print(f"[ERROR] Bandit scan failed: {e}")
