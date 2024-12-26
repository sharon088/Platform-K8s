# Kubernetes Platform Management App

This project provides a simple web application that interacts with a Kubernetes cluster to manage namespaces, deployments, and services. It is built with **Flask** for the web interface, and it leverages the **Kubernetes Python client** to interact with the cluster. The app is designed to help manage Kubernetes resources through a user-friendly interface.

## Features

- View existing namespaces in the Kubernetes cluster.
- Create and destroy namespaces.
- Deploy and update applications in Kubernetes namespaces.
- Expose deployed applications via a NodePort service.
- Check the status of pods and containers within a namespace.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Kubernetes Setup](#kubernetes-setup)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12** or higher
- **Docker** (for containerization)
- **Kubernetes cluster** (can be local like Minikube or on a cloud provider)
- **kubectl** (Kubernetes command line tool)

You will also need access to a Kubernetes cluster and have the necessary permissions to create namespaces, deployments, and services.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/kubernetes-platform-app.git
cd kubernetes-platform-app
```

### 2. Clone the repository
Create a virtual environment (optional but recommended) and install the required Python packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### 3. Build the Docker Image
If you're planning to use Docker, you can build the application container:
```bash
docker build -t kubernetes-platform-app .
```

### 4. Run the Flask Application
To run the app locally with Flask:
```bash
python app.py
```

To run the app in a production setting (with Gunicorn), use the following command:
```bash
gunicorn app:app --bind 0.0.0.0:5000
```

### 5. Run the app in Kubernetes (Optional)
You can also deploy the app in your Kubernetes cluster using the provided Kubernetes manifests (in the k8s/ folder).

```bash
kubectl apply -f k8s/
```

This will create the necessary Kubernetes resources, including:
- Deployment
- ServiceAccount
- ClusterRole and ClusterRoleBinding
- Service

Once deployed,access the app via the NodePort service exposed by Kubernetes.

## Usage

### 1. View Namespaces
Visit the home page to view the list of existing namespaces in the Kubernetes cluster.

### 2. Create a Namespace
Use the form on the homepage to create a new namespace.

### 3. Destroy a Namespace
Delete a namespace from the system by selecting it from the list and submitting the delete form.

### 4. Deploy an Application
Deploy a new application by providing the namespace and the Docker image name (with tag).

### 5. Check Pod Status
View the status of pods running within a selected namespace, including details of each container (running, waiting, terminated).

## Kubernetes Setup
To interact with the Kubernetes cluster from this app, make sure the following configurations are in place:

### 1. ServiceAccount
The app is configured to run with a service account (platform-app-sa) that has the necessary permissions to manage Kubernetes resources (pods, services, namespaces, deployments).

### 2. RBAC
The app uses ClusterRole and ClusterRoleBinding for access control. The ClusterRole gives the service account access to the Kubernetes resources that the app manages.

### 3. Deployment
The app is deployed as a containerized Flask app in the Kubernetes cluster with the necessary environment to interact with the cluster's API.

### 4. NodePort Service
The app exposes the application on a NodePort to make it accessible from outside the Kubernetes cluster.

Example of Kubernetes YAML files:

You can find the Kubernetes deployment configuration and RBAC settings in the k8s/ directory.
Steps to deploy:

```bash
kubectl apply -f k8s/
```

This command applies all the necessary configurations, including the ClusterRole, ClusterRoleBinding, ServiceAccount, Deployment, and Service.

Once deployed, access the app through the NodePort service exposed by Kubernetes.

## API Endpoints
- GET /
Displays the list of namespaces in the cluster.

- POST /create_namespace
Create a new namespace in the Kubernetes cluster.

- POST /destroy_namespace
Destroy a namespace from the Kubernetes cluster.

- POST /deploy_app
Deploy a new app or update an existing app in a specified namespace.

- GET /check_status
Check the status of pods within a specific namespace.