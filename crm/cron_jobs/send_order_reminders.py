#!/usr/bin/env python3
"""
Scheduled script to check pending orders (last 7 days)
using a GraphQL query and log reminders.
"""

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

import sys

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

def main():
    try:
        # Create GraphQL client
        transport = RequestsHTTPTransport(
            url=GRAPHQL_URL,
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        # Calculate date 7 days ago
        one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        # GraphQL query
        query = gql(
            """
            query GetRecentOrders($date: Date!) {
                allOrders(orderDateGte: $date) {
                    edges {
                        node {
                            id
                            orderDate
                            customer {
                                email
                            }
                        }
                    }
                }
            }
            """
        )

        # Execute query
        result = client.execute(query, variable_values={"date": one_week_ago})

        # Log file
        log_path = "/tmp/order_reminders_log.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_path, "a") as log_file:
            for edge in result["allOrders"]["edges"]:
                node = edge["node"]
                line = f"{timestamp} - Reminder for Order {node['id']} -> {node['customer']['email']}\n"
                log_file.write(line)

        print("Order reminders processed!")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()