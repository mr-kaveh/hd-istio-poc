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
