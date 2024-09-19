## Traffic Management Components

1.  **DestinationRule**:
    
    ```yaml
    apiVersion: networking.istio.io/v1alpha3
    kind: DestinationRule
    metadata:
      name: my-tcp-destination-rule
      namespace: your-namespace
    spec:
      host: my-tcp-service
      trafficPolicy:
        loadBalancer:
          simple: ROUND_ROBIN
    
    ```
    
    -   **DestinationRule**  defines policies that apply to traffic intended for a service after routing has occurred.
    -   **host**: Specifies the service to which the rule applies (`my-tcp-service`).
    -   **trafficPolicy**: Contains the traffic management policies.
        -   **loadBalancer**: Specifies the load balancing strategy. In this case,  `ROUND_ROBIN`  is used, which distributes traffic evenly across all instances of the service.
2.  **VirtualService**:
    
    ```yaml
    apiVersion: networking.istio.io/v1alpha3
    kind: VirtualService
    metadata:
      name: my-tcp-virtual-service
      namespace: your-namespace
    spec:
      hosts:
      - my-tcp-service
      tcp:
      - match:
        - port: 9000
        route:
        - destination:
            host: my-tcp-service
            port:
              number: 9000
    
    ```
    
    -   **VirtualService**  defines the rules that control how requests for a service are routed within the mesh.
    -   **hosts**: Specifies the service to which the virtual service applies (`my-tcp-service`).
    -   **tcp**: Defines the routing rules for TCP traffic.
        -   **match**: Specifies the criteria for matching traffic. Here, it matches traffic on port  `9000`.
        -   **route**: Defines the routing destination.
            -   **destination**: Specifies the service (`my-tcp-service`) and port (`9000`) to which the traffic should be routed.
