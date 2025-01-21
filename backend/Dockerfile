# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /workspace

# Install system dependencies (e.g., for transformers, flask, and streamlit)
RUN apt-get update && apt-get install -y wget \
    && wget https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/cuda-keyring_1.1-1_all.deb \
    && dpkg -i cuda-keyring_1.1-1_all.deb \
    && apt install software-properties-common -y \
    && add-apt-repository contrib \
    && apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    libsndfile1 \
    curl \
    ca-certificates \
    gnupg \
    cmake \
    cuda-toolkit=12.6.*


# Install Rust using rustup (Rust toolchain installer)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# Add Rust to the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy backend source files (including requirements.txt)
COPY ../ ./

# Install Python dependencies (make sure to upgrade pip first)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /workspace/backend/requirements.txt

#Cache final pip layer
RUN echo "Complete"

# Expose ports for Flask (5000)
EXPOSE 5000

# Start Flask backend and keep container alive
CMD ["bash", "-c", "python /workspace/backend/inference_service.py & sleep infinity"]
