FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port (can keep 8000 or change if needed)
EXPOSE 8000

# Run the API using Sanic's built-in server
# Note: Cloud Run will inject a PORT environment variable. Sanic respects this.
# We specify the module path to the app instance.
CMD ["sanic", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
# Using --workers 1 is often recommended for container orchestrators like Cloud Run
# as they handle scaling by creating more container instances.
