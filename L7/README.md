## Traffic Management Components

#### 1. DestinationRule

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: hd-http-destination-rule
  namespace: hd-namespace
spec:
  host: hd-http-service
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN

```

-   **DestinationRule**: This resource defines policies that apply to traffic intended for a service after routing has occurred.
-   **host**: Specifies the service to which the rule applies (`hd-http-service`).
-   **trafficPolicy**: Contains the traffic management policies.
    -   **loadBalancer**: Specifies the load balancing strategy.
        -   **simple: ROUND_ROBIN**: Distributes traffic evenly across all instances of the service. This helps in balancing the load and ensuring that no single instance is overwhelmed with requests.

#### 2. VirtualService

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: hd-http-virtual-service
  namespace: hd-namespace
spec:
  hosts:
  - hd-http-service
  gateways:
  - hd-gateway
  http:
  - match:
    - uri:
        prefix: "/v1"
    route:
    - destination:
        host: hd-http-service
        subset: v1
  - match:
    - uri:
        prefix: "/v2"
    route:
    - destination:
        host: hd-http-service
        subset: v2

```

-   **VirtualService**: This resource defines the rules that control how requests for a service are routed within the mesh.
-   **hosts**: Specifies the service to which the virtual service applies (`hd-http-service`).
-   **gateways**: Specifies the gateway through which the traffic will be routed (`hd-gateway`).
-   **http**: Defines the routing rules for HTTP traffic.
    -   **match**: Specifies the criteria for matching traffic.
        -   **uri.prefix**: Matches traffic based on the URI prefix. In this example, traffic with the prefix  `/v1`  is routed differently from traffic with the prefix  `/v2`.
    -   **route**: Defines the routing destination.
        -   **destination**: Specifies the service and subset to which the traffic should be routed.
            -   **host**: The service to route the traffic to (`hd-http-service`).
            -   **subset**: The subset of the service to route the traffic to (`v1`  or  `v2`). Subsets are typically used to route traffic to different versions of a service.

#### 3. Gateway

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: hd-gateway
  namespace: hd-namespace
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"

```

-   **Gateway**: This resource defines a load balancer for HTTP/TCP traffic. It manages inbound traffic to the mesh.
-   **selector**: Selects the ingress gateway.
    -   **istio: ingressgateway**: Specifies that the Istio ingress gateway should handle the traffic.
-   **servers**: Configures the server settings.
    -   **port**: Defines the port and protocol for the server.
        -   **number: 80**: The port number on which the gateway listens for incoming traffic.
        -   **name: http**: The name of the port.
        -   **protocol: HTTP**: The protocol used by the server.
    -   **hosts**: Specifies the hosts for which the gateway will accept traffic. In this example,  `*`  means the gateway will accept traffic for any host
 
## Security Components

#### 1. PeerAuthentication

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: hd-namespace
spec:
  mtls:
    mode: STRICT

```

-   **PeerAuthentication**: This resource defines the mutual TLS (mTLS) mode for a namespace or specific workloads.
-   **metadata**: Contains metadata about the resource, including its name and namespace.
-   **spec**: Defines the desired state of the PeerAuthentication resource.
    -   **mtls**: Configures mutual TLS settings.
        -   **mode: STRICT**: Enforces strict mTLS, meaning all traffic within the namespace must use mTLS. This ensures that all communication between services is encrypted and authenticated, preventing unauthorized access and ensuring data integrity.

#### 2. DestinationRule

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: hd-http-destination-rule
  namespace: hd-namespace
spec:
  host: hd-http-service
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
    tls:
      mode: ISTIO_MUTUAL

```

-   **DestinationRule**: This resource defines policies that apply to traffic intended for a service after routing has occurred.
-   **host**: Specifies the service to which the rule applies (`hd-http-service`).
-   **trafficPolicy**: Contains the traffic management policies.
    -   **loadBalancer**: Specifies the load balancing strategy.
        -   **simple: ROUND_ROBIN**: Distributes traffic evenly across all instances of the service.
    -   **tls**: Configures the TLS settings for the service.
        -   **mode: ISTIO_MUTUAL**: Enables mutual TLS (mTLS) for traffic to  `hd-http-service`. This means that both the client and the server must present certificates to authenticate each other, ensuring secure communication.

#### 3. AuthorizationPolicy

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: hd-authorization-policy
  namespace: hd-namespace
spec:
  selector:
    matchLabels:
      app: hd-http-app
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/hd-namespace/sa/hd-service-account"]
  - to:
    - operation:
        methods: ["GET", "POST"]

```

-   **AuthorizationPolicy**: This resource defines access control policies for services.
-   **metadata**: Contains metadata about the resource, including its name and namespace.
-   **spec**: Defines the desired state of the AuthorizationPolicy resource.
    -   **selector**: Specifies the workloads to which the policy applies.
        -   **matchLabels**: Applies the policy to pods with the specified labels (`app: hd-http-app`).
    -   **action: ALLOW**: Specifies that the policy allows traffic.
    -   **rules**: Defines the rules for the policy.
        -   **from**: Specifies the source of the traffic.
            -   **source.principals**: Specifies the allowed source principals (service accounts). In this example, only traffic from the service account  `hd-service-account`  in the namespace  `hd-namespace`  is allowed.
        -   **to**: Specifies the destination of the traffic.
            -   **operation.methods**: Specifies the allowed HTTP methods (`GET`  and  `POST`). This means that only  `GET`  and  `POST`  requests are allowed to the service.
