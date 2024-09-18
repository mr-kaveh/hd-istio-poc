#########
### Partial code to demonstrate how to handle retries, timeouts, and logging manually.
#########
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
