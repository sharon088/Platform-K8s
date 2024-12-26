from flask import Flask, render_template, request, jsonify
from kubernetes import client, config
import logging
import re

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

namespaces = {} 
#config.load_kube_config()
config.load_incluster_config()

@app.route('/')
def home():
    # Fetch existing namespaces from the Kubernetes cluster
    v1 = client.CoreV1Api()
    try:
        namespaces = v1.list_namespace()
        namespace_names = [ns.metadata.name for ns in namespaces.items]
    except client.exceptions.ApiException as e:
        logging.error(f"Error fetching namespaces: {e}")
        namespace_names = []
    return render_template('index.html', namespaces=namespace_names)


@app.route('/create_namespace', methods=['POST'])
def create_namespace():
    namespace_name = request.form.get('namespace')
    if namespace_name:
        v1 = client.CoreV1Api()
        namespace = client.V1Namespace(
            metadata=client.V1ObjectMeta(name=namespace_name)
        )
        try:
            v1.create_namespace(namespace)
            return jsonify({'message': f'Namespace "{namespace_name}" created successfully!'})
        except client.exceptions.ApiException as e:
            logging.error(f"Error creating namespace: {e}")
            return jsonify({'error': e.body}), 400
    return jsonify({'error': 'Invalid namespace name!'}), 400

@app.route('/destroy_namespace', methods=['POST'])
def destroy_namespace():
    namespace_name = request.form.get('namespace')
    if namespace_name:
        v1 = client.CoreV1Api()
        try:
            v1.delete_namespace(namespace_name)
            return jsonify({'message': f'Namespace "{namespace_name}" destroyed successfully!'})
        except client.exceptions.ApiException as e:
            logging.error(f"Error deleting namespace: {e}")
            return jsonify({'error': e.body}), 404
    return jsonify({'error': 'Namespace not found!'}), 404

@app.route('/deploy_app', methods=['POST'])
def deploy_app():
    namespace = request.form.get('namespace')
    image = request.form.get('image')

    if not namespace or not image:
        return jsonify({'error': 'Namespace and image are required!'}), 400

    # Extract the app name from the image (before the colon)
    app_name = image.split(":")[0].split("/")[-1]  # Extract the last part of the image name (after /)

    # Sanitize the app name to make it Kubernetes-friendly (lowercase, replace underscores with dashes)
    app_name = re.sub(r'[^a-z0-9-]', '-', app_name.lower())

    apps_v1 = client.AppsV1Api()
    v1 = client.CoreV1Api()

    # Check if the deployment already exists in the given namespace
    try:
        # Try to read the existing deployment
        deployment = apps_v1.read_namespaced_deployment(app_name, namespace)
        # Deployment exists, so we update it with the new image version
        deployment.spec.template.spec.containers[0].image = image
        apps_v1.replace_namespaced_deployment(name=app_name, namespace=namespace, body=deployment)
        action = 'updated'
    except client.exceptions.ApiException as e:
        if e.status == 404:
            # If deployment doesn't exist, create a new one
            deployment = client.V1Deployment(
                metadata=client.V1ObjectMeta(name=app_name),
                spec=client.V1DeploymentSpec(
                    replicas=1,
                    selector={'matchLabels': {'app': app_name}},
                    template=client.V1PodTemplateSpec(
                        metadata=client.V1ObjectMeta(labels={'app': app_name}),
                        spec=client.V1PodSpec(containers=[
                            client.V1Container(
                                name=app_name,
                                image=image,
                                ports=[client.V1ContainerPort(container_port=8000)]
                            )
                        ])
                    )
                )
            )
            apps_v1.create_namespaced_deployment(namespace=namespace, body=deployment)
            action = 'created'

            # Create NodePort Service only if it's a new deployment
            node_port = get_available_nodeport(v1)

            service = client.V1Service(
                metadata=client.V1ObjectMeta(name=f'{app_name}-service'),
                spec=client.V1ServiceSpec(
                    type='NodePort',
                    selector={'app': app_name},
                    ports=[
                        client.V1ServicePort(
                            port=8000,               # Internal port
                            target_port=8000,        # Pod port
                            node_port=node_port      # External NodePort (dynamically assigned)
                        )
                    ]
                )
            )

            try:
                v1.create_namespaced_service(namespace=namespace, body=service)
            except client.exceptions.ApiException as e:
                return jsonify({'error': f'Service creation failed: {e.body}'}), 400
        else:
            return jsonify({'error': f'Deployment update failed: {e.body}'}), 400

    return jsonify({
        'message': f'App "{app_name}" {action} and exposed at NodePort {get_nodeport_for_deployment(v1, app_name,namespace)} in namespace "{namespace}".'
    })


def get_available_nodeport(v1):
    # Define the NodePort range (typically 30000-32767)
    node_port_range = range(30000, 32768)

    # List all existing services to check for available NodePort
    services = v1.list_service_for_all_namespaces()
    used_ports = {service.spec.ports[0].node_port for service in services.items if service.spec.type == 'NodePort'}

    # Find the first available NodePort
    for port in node_port_range:
        if port not in used_ports:
            return port
    
    # If no available NodePort is found, raise an error (or you could handle this differently)
    raise Exception("No available NodePort in the range 30000-32767")

def get_nodeport_for_deployment(v1, app_name, namespace):
    # Try to get the service associated with the app_name and get its NodePort
    try:
        service = v1.read_namespaced_service(f"{app_name}-service", namespace)
        node_port = service.spec.ports[0].node_port
        return node_port
    except client.exceptions.ApiException as e:
        return None  # Service doesn't exist or some other error


@app.route('/check_status', methods=['GET'])
def check_status():
    namespace = request.args.get('namespace')
    if not namespace:
        return jsonify({'error': 'Namespace is required!'}), 400

    v1 = client.CoreV1Api()
    try:
        pods = v1.list_namespaced_pod(namespace=namespace).items
        pod_details = []
        for pod in pods:
            containers = [
                {
                    'name': container.name,
                    'image': container.image,
                    'state': container.state.running and "Running" or container.state.waiting and "Waiting" or container.state.terminated and "Terminated"
                }
                for container in pod.status.container_statuses or []
            ]
            pod_details.append({
                'pod_name': pod.metadata.name,
                'phase': pod.status.phase,
                'containers': containers
            })
        return jsonify({'pods': pod_details})
    except client.exceptions.ApiException as e:
        return jsonify({'error': e.body}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
