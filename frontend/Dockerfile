# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system-level dependencies required for some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port (Streamlit usually runs on 8501, we’ll map it to 80 in docker-compose)
EXPOSE 80

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0"]