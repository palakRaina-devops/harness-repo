# Use lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose application port
EXPOSE 8080

# Run using gunicorn (recommended for production)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
