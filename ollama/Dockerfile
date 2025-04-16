# Use an official Python runtime as a parent image
FROM ollama/ollama

# Set the working directory in the container
WORKDIR /workspace

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
CMD ["bash", "-c", "sleep infinity"]
