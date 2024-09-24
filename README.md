# hd-istio-poc
implements istio Service Mesh Layer for Kubernetes Deployment

A  **service mesh**  is a dedicated infrastructure layer that manages service-to-service communication within a microservices architecture. It provides several key functionalities:

1.  **Traffic Management**: Controls the flow of traffic between services, enabling features like load balancing, traffic splitting, and retries.
2.  **Security**: Enhances security through mutual TLS (mTLS) for encrypted communication between services, and provides fine-grained access control.
3.  **Observability**: Offers detailed insights into service interactions, including metrics, logging, and tracing, which help in monitoring and debugging.
4.  **Service Discovery**: Automatically detects and keeps track of services within the mesh, simplifying the management of service endpoints

By abstracting these concerns away from the application code, a service mesh allows developers to focus on business logic while ensuring reliable and secure communication between services.


![service-mesh](https://github.com/user-attachments/assets/0ae1b8a9-7016-48db-8ff6-1a3d64365e98)


### Without Istio
#### Deployment

In a Kubernetes environment, a basic deployment of a microservice might look like this:

	apiVersion: apps/v1
	kind: Deployment
	metadata:
	  name: my-service
	spec:
	  replicas: 3
	  selector:
	    matchLabels:
	      app: my-service
	  template:
	    metadata:
	      labels:
	        app: my-service
	    spec:
	      containers:
	      - name: my-service
	        image: my-service:latest
	        ports:
	        - containerPort: 8080


#### Code Base

In the microservice code, you might handle retries, timeouts, and logging manually:

	import requests
	import logging

	logging.basicConfig(level=logging.INFO)

	def call_external_service():
	    try:
	        response = requests.get("http://external-service/api", timeout=5)
	        response.raise_for_status()
	        return response.json()
	    except requests.exceptions.RequestException as e:
	        logging.error(f"Request failed: {e}")
	        return None

	# Business logic
	def process_data():
	    data = call_external_service()
	    if data:
	        # Process data
	        pass

### With Istio

#### Deployment

With Istio, the deployment includes a sidecar proxy (Envoy) that handles traffic management, security, and observability:

	apiVersion: apps/v1
	kind: Deployment
	metadata:
	  name: my-service
	spec:
	  replicas: 3
	  selector:
	    matchLabels:
	      app: my-service
	  template:
	    metadata:
	      labels:
	        app: my-service
	    spec:
	      containers:
	      - name: my-service
	        image: my-service:latest
	        ports:
	        - containerPort: 8080
	      # Istio sidecar injection
	      annotations:
	        sidecar.istio.io/inject: "true"

#### Code Base

The microservice code can be simplified, as Istio handles retries, timeouts, and logging:
	
	import requests

	def call_external_service():
	    response = requests.get("http://external-service/api")
	    response.raise_for_status()
	    return response.json()

	# Business logic
	def process_data():
	    data = call_external_service()
	    if data:
	        # Process data
	        pass

### Key Differences

1.  **Deployment**: With Istio, the deployment includes annotations for sidecar injection, which automatically adds Envoy proxies to manage traffic.
2.  **Code Base**: The code is simplified as Istio handles cross-cutting concerns like retries, timeouts, and logging, reducing the need for boilerplate code.
3.  **Traffic Management**: Istio provides advanced traffic management features like traffic splitting, mirroring, and fault injection without changing the application code.
4.  **Security**: Istio manages service-to-service authentication, authorization, and encryption, enhancing security without modifying the microservice.
5.  **Observability**: Istio provides out-of-the-box metrics, logging, and tracing, improving observability and making it easier to monitor and debug services.

## Architecture

![arch](https://github.com/user-attachments/assets/32996eaf-6cb1-457b-ab51-3b81ff1146ba)
