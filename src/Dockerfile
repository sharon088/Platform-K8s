# Stage 1: Install dependencies
FROM python:3.12-alpine AS build

WORKDIR /app

# Copy requirements and install dependencies
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-alpine AS runtime

WORKDIR /platform

# Copy only the installed dependencies (site-packages) from the build stage
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy application code (static files, templates, and main app file)
COPY --from=build /app /platform

# Expose Flask's default port
EXPOSE 5000

# Command to run the Flask app using Gunicorn (WSGI server)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]

