import json

# Load the JSON data
with open('order.json', 'r') as f:
    data = json.load(f)

# Initialize dictionaries for aggregations
total_pallets_by_customer = {}
total_pallets_by_box_size = {}
total_pounds_by_grade = {}

# Function to extract pounds per box from box_size
def get_pounds_per_box(box_size):
    if box_size:
        return int(box_size[:-2])  # Remove 'lb' and convert to int
    return 0

# Calculate average cases per pallet from items with cases not null
cases_per_pallet_list = []
for order in data['orders']:
    for item in order['items']:
        pallets = item.get('pallets', 0)
        cases = item.get('cases')
        if cases is not None and pallets > 0:
            cases_per_pallet_list.append(cases / pallets)

average_cases_per_pallet = sum(cases_per_pallet_list) / len(cases_per_pallet_list) if cases_per_pallet_list else 100  # Default to 100 if no data
average_cases_per_pallet = round(average_cases_per_pallet)

# Process each order for pallets
for order in data['orders']:
    customer_name = order['customer_name']
    total_pallets_customer = order.get('total_pallets', 0)
    total_pallets_by_customer[customer_name] = total_pallets_customer
    
    for item in order['items']:
        box_size = item['box_size']
        pallets = item.get('pallets', 0)
        
        # Total pallets by box_size
        if box_size not in total_pallets_by_box_size:
            total_pallets_by_box_size[box_size] = 0
        total_pallets_by_box_size[box_size] += pallets

# Process each order for pounds
for order in data['orders']:
    for item in order['items']:
        box_size = item['box_size']
        grade = item['grade']
        pallets = item.get('pallets', 0)
        cases = item.get('cases')
        
        pounds_per_box = get_pounds_per_box(box_size)
        
        if cases is not None:
            total_cases = cases
        else:
            total_cases = pallets * average_cases_per_pallet
        
        pounds = total_cases * pounds_per_box
        
        if grade not in total_pounds_by_grade:
            total_pounds_by_grade[grade] = 0
        total_pounds_by_grade[grade] += pounds

# Print results
print("Total Pallets by Customer:")
for customer, pallets in total_pallets_by_customer.items():
    print(f"  {customer}: {pallets}")

print("\nTotal Pallets by Box Size:")
for box_size, pallets in total_pallets_by_box_size.items():
    print(f"  {box_size}: {pallets}")

print("\nTotal Pounds by Grade (using cases data and average cases per pallet for missing cases):")
for grade, pounds in total_pounds_by_grade.items():
    print(f"  {grade}: {pounds}")

# Also print the logic explanation
print("\nLogic Explanation:")
print("1. Total Pallets by Customer: Directly taken from 'total_pallets' in each order.")
print("2. Total Pallets by Box Size: Sum of 'pallets' for each item grouped by 'box_size'.")
print(f"3. Total Pounds by Grade: Calculated as pounds = total_cases * pounds_per_box, where pounds_per_box = int(box_size[:-2]).")
print(f"   - If 'cases' is provided, total_cases = cases.")
print(f"   - If 'cases' is null, total_cases = pallets * average_cases_per_pallet (average calculated from items with cases: {average_cases_per_pallet}).")
print("   This assumes 'cases' represents the number of boxes/master cartons, and box_size is pounds per box.")