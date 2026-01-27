import csv

# Read orders.csv
with open('shipments/orders.csv', 'r') as f:
    reader = csv.DictReader(f)
    orders_rows = list(reader)

# Read new-shipments-parsed.csv
with open('shipments/new-shipments-parsed.csv', 'r') as f:
    reader = csv.DictReader(f)
    new_rows = list(reader)

# Add missing fields to new_rows
for row in new_rows:
    row['customer_id'] = ''
    row['total_pallets'] = ''
    row['eta'] = ''
    row['ready_date'] = ''
    row['packed_by'] = ''
    row['priority'] = ''

# Combine all rows
all_rows = orders_rows + new_rows

# Remove any None keys that might exist
for row in all_rows:
    if None in row:
        del row[None]

# Write to merge.csv
with open('merge.csv', 'w', newline='') as f:
    fieldnames = ['customer_id', 'customer_name', 'total_pallets', 'eta', 'ready_date', 'packed_by', 'priority', 'box_size', 'grade', 'top_color', 'pallets', 'cases', 'notes']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_rows)