import json
import csv

# Load the JSON data
with open('order.json', 'r') as f:
    data = json.load(f)

# Prepare CSV data
csv_data = []
headers = ['customer_id', 'customer_name', 'total_pallets', 'eta', 'ready_date', 'packed_by', 'priority', 'box_size', 'grade', 'top_color', 'pallets', 'cases', 'notes']

for order in data['orders']:
    customer_id = order['customer_id']
    customer_name = order['customer_name']
    total_pallets = order['total_pallets']
    eta = order.get('eta')
    ready_date = order.get('ready_date')
    packed_by = order.get('packed_by')
    priority = order['priority']
    
    for item in order['items']:
        row = [
            customer_id,
            customer_name,
            total_pallets,
            eta,
            ready_date,
            packed_by,
            priority,
            item['box_size'],
            item['grade'],
            item.get('top_color'),
            item['pallets'],
            item.get('cases'),
            item.get('notes')
        ]
        csv_data.append(row)

# Write to CSV
with open('orders.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(csv_data)

print("CSV file 'orders.csv' has been created.")