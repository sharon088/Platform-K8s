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

