Kubernetes Platform App:

This project is a web application built using Flask and Kubernetes Python Client that allows users to manage Kubernetes namespaces, deploy applications, and monitor pod statuses. The app is packaged as a Docker container and deployed to Kubernetes using a set of manifests for managing access, services, and deployments.

Prerequisites:
Before setting up this project, ensure you have the following installed:

Docker for containerizing the application.
Kubernetes cluster (e.g., Minikube, or a cloud provider like AWS, GCP, Azure).
Kubectl for interacting with the Kubernetes cluster.
Helm (optional) for managing Kubernetes charts.

Features:
Namespace Management: Create and delete Kubernetes namespaces.
App Deployment: Deploy and update applications in Kubernetes.
Service Exposure: Expose applications via NodePort.
Pod Monitoring: Check the status of pods in a specific namespace.

Installation:
1. Clone the Repository
   git clone https://github.com/sharon088/Platform-K8s.git
   cd Platform-K8s

2. Build and Run the Docker Container
  The application is packaged using Docker to ensure consistency across environments. The Dockerfile uses     
  Gunicorn as the WSGI server to serve the Flask application.
  
  Build the Docker Image
  docker build -t sharon088/k8s-platform-app:v1.0.0 .

  Run the Docker Image Locally
  docker run -p 5000:5000 sharon088/k8s-platform-app:v1.0.0
  Visit http://localhost:5000 in your browser to access the application.


Kubernetes Deployment
1. Kubernetes Configuration
Ensure you have a Kubernetes cluster running and that kubectl is configured to access the cluster.

You can use Minikube for local development or any cloud provider for production deployment.

2. Apply Kubernetes Manifests
The project includes Kubernetes manifests for deploying the app, setting up the required permissions, and exposing the app through a service.

Apply the Kubernetes Manifests
kubectl apply -f k8s/clusterrole.yaml
kubectl apply -f k8s/clusterrolebinding.yaml
kubectl apply -f k8s/serviceaccount.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

This will:

  Create a ClusterRole that grants the necessary permissions (namespace management, pods, services, etc.).
  Bind the ClusterRole to a ServiceAccount.
  Deploy the app using the Deployment manifest.
  Expose the app using a NodePort service.

3. Access the Application
Once the application is deployed, you can access it via the NodePort on your Kubernetes cluster. The service will expose the app on port 30000 by default.

To access the app, navigate to:
  http://<Node_IP>:30000


Dockerfile Explanation
The Dockerfile is structured in two stages:

Build Stage: Installs dependencies from requirements.txt and prepares the app for deployment.
Runtime Stage: Copies the dependencies from the build stage, application code, and starts the Flask app using Gunicorn.

# Stage 1: Install dependencies
FROM python:3.12-slim AS build

WORKDIR /app

# Copy requirements and install dependencies
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /platform

# Copy only the installed dependencies (site-packages) from the build stage
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy application code (static files, templates, and main app file)
COPY --from=build /app /platform

# Expose Flask's default port
EXPOSE 5000

# Command to run the Flask app using Gunicorn (WSGI server)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]


Gunicorn Usage
In production environments, Gunicorn is used to serve the Flask app due to its better performance and scalability compared to Flask's built-in server.

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]: Starts the Flask app using Gunicorn, binding it to all available network interfaces on port 5000.
Requirements
Flask==3.1.0
kubernetes==31.0.0
gunicorn==23.0.0

These dependencies are listed in the requirements.txt file. You can install them by running:

pip install -r requirements.txt

Kubernetes YAML Manifests
1. clusterrole.yaml
Defines the ClusterRole with permissions to manage namespaces, pods, services, and deployments.
2. clusterrolebinding.yaml
Binds the ClusterRole to the platform-app-sa service account.
3. deployment.yaml
Deploys the app to Kubernetes.
4. service.yaml
Defines a NodePort service for exposing the app.
5. serviceaccount.yaml
Defines the ServiceAccount used by the app.

Conclusion
This project is a simple Kubernetes platform management tool built with Flask. By following this README, you can easily set up the project locally and on a Kubernetes cluster for production use.


