import os
from datetime import datetime
from jinja2 import Template

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def timestamped_filename(prefix, ext="py"):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}.{ext}"

def save_code(code: str, prefix: str, output_dir: str):
    ensure_dir(output_dir)
    filename = timestamped_filename(prefix)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w") as f:
        f.write(code)
    return filepath

def render_template(template_path: str, context: dict):
    with open(template_path) as f:
        template = Template(f.read())
    return template.render(**context)
