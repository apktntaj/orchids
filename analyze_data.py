import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
df = pd.read_csv('final_task.csv')

# Basic statistics
print("Total records:", len(df))
print("Unique products:", df['product_name'].nunique())
print("Unique bill_to:", df['bill_to'].nunique())
print("Date range:", df['date'].min(), "to", df['date'].max())

# Total quantity by product
product_qty = df.groupby('product_name')['qty'].sum().sort_values(ascending=False)
print("\nTop 5 products by quantity:")
print(product_qty.head(5))

# Total quantity by bill_to
bill_to_qty = df.groupby('bill_to')['qty'].sum().sort_values(ascending=False)
print("\nTop 5 bill_to by quantity:")
print(bill_to_qty.head(5))

# Quantity over time
df['date'] = pd.to_datetime(df['date'])
monthly_qty = df.groupby(df['date'].dt.to_period('M'))['qty'].sum()
print("\nMonthly quantity:")
print(monthly_qty)