import datetime

from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client


def log_crm_heartbeat():
    # Log timestamp
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(log_message)

    # Optional GraphQL check
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )

        client = Client(transport=transport, fetch_schema_from_transport=False)

        query = gql("""
        {
            hello
        }
        """)

        result = client.execute(query)
        print("GraphQL Response:", result)

    except Exception as e:
        print("GraphQL Error:", str(e))

def update_low_stock():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Prepare GraphQL mutation
    mutation = gql("""
        mutation {
            updateLowStockProducts {
                message
                updatedProducts
            }
        }
    """)

    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        result = client.execute(mutation)

        updated_list = result["updateLowStockProducts"]["updatedProducts"]

        # Log output
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{timestamp} - Updated Products:\n")
            for item in updated_list:
                f.write(f" - {item}\n")

        print("Low stock update processed!")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{timestamp} - Error: {str(e)}\n")
        print("Error updating low stock:", str(e))