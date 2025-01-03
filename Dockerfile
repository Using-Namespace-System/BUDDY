# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (e.g., for transformers, flask, and streamlit)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    libsndfile1

# Install dependencies for both backend and frontend
COPY backend/requirements.txt ./backend/requirements.txt
COPY frontend/requirements.txt ./frontend/requirements.txt

RUN pip install --no-cache-dir -r ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./frontend/requirements.txt

# Copy the backend and frontend files into the container
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/

# Expose ports for Flask (5000) and Streamlit (8501)
EXPOSE 5000
EXPOSE 8501

# Start both Flask backend and Streamlit frontend with a single command
CMD ["bash", "-c", "python /app/backend/inference_service.py & streamlit run /app/frontend/app.py --server.port 8501"]
