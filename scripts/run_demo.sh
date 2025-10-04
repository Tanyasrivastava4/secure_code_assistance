#!/bin/bash
# Simple automation script
python -m code_assistant.cli generate --task "file upload endpoint"
python -m code_assistant.cli scan --file local/examples/generated_file_upload.py
