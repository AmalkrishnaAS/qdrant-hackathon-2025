FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for video/audio processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libfontconfig1 \
    libxrender1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads static/processed

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONPATH=/app
ENV PORT=5000

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]

