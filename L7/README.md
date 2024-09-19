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
