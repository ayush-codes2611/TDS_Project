import subprocess
import sys
import urllib.request
import os

# Step 1: Check if 'uv' is installed, install if needed
def ensure_uv_installed():
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True, text=True)
        print("✅ 'uv' is already installed.")
    except subprocess.CalledProcessError:
        print("⚠️ 'uv' not found, installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
        print("✅ 'uv' installed successfully.")

# Step 2: Download 'datagen.py'
def download_datagen():
    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    file_path = "datagen.py"
    
    if not os.path.exists(file_path):  # Avoid redundant downloads
        print("📥 Downloading datagen.py...")
        urllib.request.urlretrieve(url, file_path)
        print("✅ Download complete.")
    else:
        print("ℹ️ datagen.py already exists, skipping download.")

# Step 3: Run 'datagen.py' with user.email
def run_datagen(email):
    print(f"🚀 Running datagen.py with email: {email}")
    subprocess.run([sys.executable, "datagen.py", email], check=True)
    print("✅ datagen.py executed successfully.")

if __name__ == "__main__":
    user_email = "23f2001286@ds.study.iitm.ac.in"  # Your email

    ensure_uv_installed()
    download_datagen()
    run_datagen(user_email)
