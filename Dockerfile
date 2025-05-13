# Using official Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY backend/requirements.txt .
COPY backend/ .

# Install dependencies (only standard library packages)
# Note: WebContainer can't actually run this but it's good practice
RUN pip install --no-cache-dir -r requirements.txt || echo "Skipping pip install in WebContainer"

# Expose port
EXPOSE 8000

# Start the server using standard library http.server
CMD ["python3", "main.py"]
