import os
import sys
from code_assistant.scanner import scan_file

if len(sys.argv) != 2:
    print("Usage: python auto_scan.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    sys.exit(1)

scan_file(file_path)
