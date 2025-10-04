import click
from .generator import generate_code
from .scanner import scan_file

@click.group()
def cli():
    """Secure Code Assistant CLI"""
    pass

@cli.command()
@click.option("--task", prompt="Task description", help="Description of code to generate")
@click.option("--lang", default="python", help="Programming language")
def generate(task, lang):
    """Generate code via LLM server or template"""
    filepath = generate_code(task, lang)
    print(f"Generated code at: {filepath}")

@cli.command()
@click.option("--file", prompt="File to scan", help="Python file to scan for vulnerabilities")
def scan(file):
    """Scan Python file with Bandit"""
    scan_file(file)

if __name__ == "__main__":
    cli()
