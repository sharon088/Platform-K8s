# Stage 1: Install dependencies
FROM python:3.12-slim AS build

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /platform

# Copy only the installed dependencies (site-packages) from the build stage
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy application code (static files, templates, and main app file)
COPY static ./static
COPY templates ./templates
COPY app.py .

# Expose Flask's default port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]

