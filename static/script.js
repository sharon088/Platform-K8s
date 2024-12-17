document.addEventListener('DOMContentLoaded', () => {
    const namespaceSelect = document.getElementById('namespaceSelect');

    // Handle Create Namespace
    document.getElementById('createForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const namespace = document.getElementById('namespaceInput').value;
        const response = await fetch('/create_namespace', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `namespace=${namespace}`
        });
        const result = await response.json();
        document.getElementById('createMessage').innerText = result.message || result.error;
    });

    // Handle Deploy App
    document.getElementById('deployButton').addEventListener('click', async () => {
        const namespace = namespaceSelect.value;
        const image = document.getElementById('imageInput').value;
        if (namespace && image) {
            const response = await fetch('/deploy_app', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `namespace=${namespace}&image=${encodeURIComponent(image)}`
            });
            const result = await response.json();
            alert(result.message || result.error);
        } else {
            alert('Please select a namespace and enter an image to deploy.');
        }
    });

    // Handle Destroy Namespace
    document.getElementById('destroyButton').addEventListener('click', async () => {
        const namespace = namespaceSelect.value;
        if (namespace) {
            const response = await fetch('/destroy_namespace', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `namespace=${namespace}`
            });
            const result = await response.json();
            alert(result.message || result.error);
        }
    });

    // Handle Check Status
    document.getElementById('statusButton').addEventListener('click', () => {
        const namespace = document.getElementById('namespaceSelectStatus').value;
    
        fetch(`/check_status?namespace=${namespace}`)
            .then(response => response.json())
            .then(data => {
                const resultsDiv = document.getElementById('statusResults');
                resultsDiv.innerHTML = ''; // Clear previous results
    
                if (data.pods) {
                    data.pods.forEach(pod => {
                        const podInfo = `
                            <div class="pod-info">
                                <h3>Pod: ${pod.pod_name}</h3>
                                <p>Phase: ${pod.phase}</p>
                                <h4>Containers:</h4>
                                <ul>
                                    ${pod.containers.map(container => `
                                        <li>
                                            <strong>Name:</strong> ${container.name}<br>
                                            <strong>Image:</strong> ${container.image}<br>
                                            <strong>Status:</strong> ${container.state}
                                        </li>
                                    `).join('')}
                                </ul>
                            </div>
                        `;
                        resultsDiv.innerHTML += podInfo;
                    });
                } else if (data.error) {
                    resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
                }
            })
            .catch(error => console.error('Error fetching status:', error));
    });
    
});
