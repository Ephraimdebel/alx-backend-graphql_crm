from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    # Setup GraphQL client
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query to fetch totals
    query = gql('''
    query {
        totalCustomers: allCustomers {
            totalCount
        }
        totalOrders: allOrders {
            totalCount
            edges {
                node {
                    totalAmount
                }
            }
        }
    }
    ''')

    result = client.execute(query)
    
    total_customers = result['totalCustomers']['totalCount']
    total_orders = result['totalOrders']['totalCount']
    total_revenue = sum(order['node']['totalAmount'] for order in result['totalOrders']['edges'])

    # Log to file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('/tmp/crm_report_log.txt', 'a') as f:
        f.write(f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n")
