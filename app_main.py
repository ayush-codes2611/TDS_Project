import subprocess
import sys
import os
import urllib.request

config = {
    "email": "",
    "root": "/data"
}

# Task A1: Install uv and run datagen.py
def install_uv():
    try:
        import uv
    except ImportError:
        print("uv is not installed. Installing uv...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "uv"])

def run_datagen(email):
    datagen_url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    datagen_path = "/tmp/datagen.py"
    
    urllib.request.urlretrieve(datagen_url, datagen_path)
    
    subprocess.run(["python", datagen_path, email])

def a1_run_datagen():
    install_uv()
    run_datagen(config["email"])

# Task A2: Format /data/format.md using prettier@3.4.2
def install_prettier():
    try:
        subprocess.check_call(["prettier", "--version"])
    except FileNotFoundError:
        print("Prettier is not installed. Installing prettier@3.4.2...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "prettier@3.4.2"])

def format_markdown():
    format_path = os.path.join(config["root"], "format.md")
    if os.path.exists(format_path):
        subprocess.run(["prettier", "--write", format_path])
    else:
        print(f"Error: {format_path} not found.")

def a2_format_markdown():
    install_prettier()
    format_markdown()

# Main function to run both tasks
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("email")
    parser.add_argument("--root", default="/data")
    args = parser.parse_args()
    
    config["email"] = args.email
    config["root"] = os.path.abspath(args.root)

    os.makedirs(config["root"], exist_ok=True)

    # Running both A1 and A2 tasks
    a1_run_datagen()
    a2_format_markdown()
