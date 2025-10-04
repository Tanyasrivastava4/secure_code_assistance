
# project-13/code_assistant/generator.py

import requests
import os
import subprocess
import sys
from .config import LLM_SERVER_URL, SALAD_SECRET, OUTPUT_DIR
from .utils import save_code, render_template, ensure_dir

# Path to templates folder
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


def _run_auto_scan(filepath: str) -> bool:
    """
    Try to run the auto-scan script/module on `filepath`.
    Returns True if the scan command returned exit code 0, False otherwise.
    """
    py = sys.executable or "python"
    # Prefer running as a module inside the package
    try:
        # This expects `code_assistant/auto_scan.py` to exist and be runnable as a module
        print(f"[INFO] Running auto-scan via module: {py} -m code_assistant.auto_scan {filepath}")
        res = subprocess.run([py, "-m", "code_assistant.auto_scan", filepath], capture_output=True, text=True)
        print(res.stdout, end="")
        if res.returncode == 0:
            print("[INFO] Auto-scan (module) completed successfully.")
            return True
        else:
            print(f"[WARN] Auto-scan (module) exited with code {res.returncode}. stderr:\n{res.stderr}")
    except Exception as e_mod:
        print(f"[WARN] Auto-scan (module) failed: {e_mod}")

    # Fallback: try running a top-level script `auto_scan.py` from project root
    try:
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "auto_scan.py")
        if os.path.exists(script_path):
            print(f"[INFO] Running auto-scan via script: {py} {script_path} {filepath}")
            res2 = subprocess.run([py, script_path, filepath], capture_output=True, text=True)
            print(res2.stdout, end="")
            if res2.returncode == 0:
                print("[INFO] Auto-scan (script) completed successfully.")
                return True
            else:
                print(f"[WARN] Auto-scan (script) exited with code {res2.returncode}. stderr:\n{res2.stderr}")
        else:
            print(f"[WARN] Fallback auto_scan.py not found at: {script_path}")
    except Exception as e_script:
        print(f"[WARN] Auto-scan (script) failed: {e_script}")

    return False


def generate_code(task: str, lang: str = "python"):
    """
    Sends a prompt to the LLM server to generate code.
    If server unavailable, uses fallback template.

    Args:
        task (str): Description of the task to generate code for.
        lang (str): Programming language (default: python)

    Returns:
        str: Filepath of the generated code in examples/
    """

    payload = {"prompt": task, "language": lang}

    # Optional headers if webhook secret exists
    headers = {}
    if SALAD_SECRET:
        headers["Authorization"] = f"Bearer {SALAD_SECRET}"

    try:
        # Send request to LLM server (longer timeout for big models)
        response = requests.post(f"{LLM_SERVER_URL}/generate", json=payload, headers=headers, timeout=120)
        response.raise_for_status()
        code = response.json().get("code", "")
        if not code:
            raise ValueError("Empty code received from LLM server.")

    except Exception as e:
        # Fallback to template if LLM server is unavailable
        print(f"[WARN] LLM server unavailable or error occurred: {e}")

        # Decide template based on task keyword
        if "upload" in task.lower():
            template_file = "file_upload.py.j2"
        else:
            template_file = "sql_demo.py.j2"

        template_path = os.path.join(TEMPLATES_DIR, template_file)

        # Render template with placeholders
        code = render_template(template_path, {"task": task, "language": lang})

    # Ensure output directory exists
    ensure_dir(OUTPUT_DIR)

    # Save the generated code to examples folder with a timestamped filename
    safe_task_name = task.replace(" ", "_")
    filepath = save_code(code, prefix=safe_task_name, output_dir=OUTPUT_DIR)

    print(f"[INFO] Code saved to {filepath}")

    # -----------------------------
    # Auto-scan the generated file
    # -----------------------------
    try:
        ok = _run_auto_scan(filepath)
        if not ok:
            print("[WARN] Auto-scan finished with warnings or errors. Please inspect the scan output.")
        else:
            print("[INFO] Auto-scan passed for generated file.")
    except Exception as e:
        print(f"[WARN] Auto scan failed with exception: {e}")

    return filepath


















# local/code_assistant/generator.py
#this code i was using and now updating this code see above after adding auto_scan.py to automatically scan without excuting a line for scanning
#import requests
#import os
#from .config import LLM_SERVER_URL, SALAD_SECRET, OUTPUT_DIR
#from .utils import save_code, render_template, ensure_dir

# Path to templates folder
#TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


#def generate_code(task: str, lang: str = "python"):
 #   """
  #  Sends a prompt to the LLM server to generate code.
  #  If server is unavailable, uses fallback template.
    
 #   Args:
  #     task (str): Description of the task to generate code for.
  #     lang (str): Programming language (default: python)
  # 
  # Returns:
  #     str: Filepath of the generated code in examples/
  # """

  # payload = {"prompt": task, "language": lang}

  # # Optional headers if webhook secret exists
  # headers = {}
  # if SALAD_SECRET:
  #     headers["Authorization"] = f"Bearer {SALAD_SECRET}"

  # try:
  #     # Send request to LLM server
  #     response = requests.post(f"{LLM_SERVER_URL}/generate", json=payload, headers=headers, timeout=120)
  #     response.raise_for_status()
  #     code = response.json().get("code", "")
  #     if not code:
  #         raise ValueError("Empty code received from LLM server.")

  # except Exception as e:
  #     # Fallback to template if LLM server is unavailable
  #     print(f"[WARN] LLM server unavailable or error occurred: {e}")
  #     
  #     # Decide template based on task keyword
  #     if "upload" in task.lower():
  #         template_file = "file_upload.py.j2"
  #     else:
  #         template_file = "sql_demo.py.j2"

  #     template_path = os.path.join(TEMPLATES_DIR, template_file)

  #     # Render template with placeholders
  #     code = render_template(template_path, {"task": task, "language": lang})

  # # Ensure output directory exists
  # ensure_dir(OUTPUT_DIR)

    # Save the generated code to examples folder with a timestamped filename
    #safe_task_name = task.replace(" ", "_")
    #filepath = save_code(code, prefix=safe_task_name, output_dir=OUTPUT_DIR)

   # print(f"[INFO] Code saved to {filepath}")
   # return filepath

























#import requests
#from .config import LLM_SERVER_URL
#from .utils import save_code, render_template, ensure_dir
#import os

#TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

#def generate_code(task: str, lang: str = "python"):
 #   """
  #  Sends prompt to LLM server to generate code.
   # If server unavailable, uses fallback template.
   # """
   # payload = {"prompt": task, "language": lang}
   # try:
   #     response = requests.post(f"{LLM_SERVER_URL}/generate", json=payload, timeout=30)
    #    response.raise_for_status()
    #    code = response.json().get("code", "")
    #    if not code:
     #       raise ValueError("Empty code received")
    #except Exception as e:
     #   print(f"[WARN] LLM server unavailable, using fallback template: {e}")
        # Fallback template
      #  template_file = "file_upload.py.j2" if "upload" in task.lower() else "sql_demo.py.j2"
       # template_path = os.path.join(TEMPLATES_DIR, template_file)
        #code = render_template(template_path, {"task": task, "language": lang})
    # Save code to examples
    #from .config import OUTPUT_DIR
    #filepath = save_code(code, prefix=task.replace(" ", "_"), output_dir=OUTPUT_DIR)
    #print(f"[INFO] Code saved to {filepath}")
    #return filepath
