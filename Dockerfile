FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]

