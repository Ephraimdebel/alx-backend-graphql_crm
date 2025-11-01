import requests
from datetime import datetime

def log_crm_heartbeat():
    """Log CRM heartbeat every 5 minutes and check GraphQL hello response."""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Default heartbeat message
    message = f"{timestamp} CRM is alive\n"

    try:
        # Optional: Query GraphQL hello field
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            message = f"{timestamp} CRM is alive (GraphQL OK)\n"
        else:
            message = f"{timestamp} CRM heartbeat but GraphQL error\n"
    except Exception:
        message = f"{timestamp} CRM heartbeat but GraphQL unreachable\n"

    # Write to log
    with open("/tmp/crm_heartbeat_log.txt", "a") as file:
        file.write(message)