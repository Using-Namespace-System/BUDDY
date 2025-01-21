# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /workspace

# Install system dependencies (e.g., for transformers, flask, and streamlit)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev

# Install dependencies for frontend
COPY ../ ./

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r ./frontend/requirements.txt

#Cache final pip layer
RUN echo "Complete"

# Expose ports for Streamlit (8501)
EXPOSE 8501

# Start both Streamlit frontend and
# Keepalive

CMD ["bash", "-c", "streamlit run /workspace/frontend/app.py --server.port 8501 & sleep infinity"]

