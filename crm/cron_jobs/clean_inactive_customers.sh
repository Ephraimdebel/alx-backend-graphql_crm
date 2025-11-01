#!/bin/bash

# Cleanup inactive customers (customers with no orders in the past year)
timestamp=$(date "+%Y-%m-%d %H:%M:%S")

deleted_count=$(python3 manage.py shell <<EOF
from datetime import datetime, timedelta
from crm.models import Customer, Order

one_year_ago = datetime.now() - timedelta(days=365)

inactive_customers = Customer.objects.exclude(
    order__order_date__gte=one_year_ago
)

count = inactive_customers.count()
inactive_customers.delete()

print(count)
EOF
)

echo "$timestamp - Deleted customers: $deleted_count" >> /tmp/customer_cleanup_log.txt
