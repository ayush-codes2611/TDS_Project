FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app
COPY app_main.py .

#later will be changed to app.py
CMD ["uv", "run", "app_main.py"]  


# FROM python:3.12-slim-bookworm

# # Install curl, certificates, and pip (if needed)
# RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# # Download the latest installer for `uv`
# ADD https://astral.sh/uv/install.sh /uv-installer.sh

# # Run the installer and remove it after installation
# RUN sh /uv-installer.sh && rm /uv-installer.sh

# # Ensure the installed binary is on the `PATH`
# ENV PATH="/root/.local/bin/:$PATH"

# # Set the working directory
# WORKDIR /app

# # Copy your FastAPI app file
# COPY app_main.py /app/

# # Run the app using `uv` via the `app_main.py` entry point
# CMD ["uv", "run", "app_main.py"]