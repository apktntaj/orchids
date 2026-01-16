# Orchids Supply Chain Management

This repository contains data and scripts for managing the supply chain operations of Orchids, a supplier of dates. It includes order processing, shipment calculations, invoice tracking, bills of lading, and supplier partnership information.

## Repository Structure

- **bls/**: Bills of Lading (B/L) documents in PDF format, organized by shipment numbers and suppliers.
- **invoices/**: Invoice PDFs, organized by month (e.g., `dec-2025/`, `jan-2026/`).
- **shipments/**: Order data and analysis scripts.
  - `order.json`: JSON file containing order details (customers, items, pallets, etc.).
  - `orders.csv`: CSV export of order data.
  - `calculate.py`: Python script to aggregate shipment metrics (pallets by customer/box size, pounds by grade).
  - `transform_to_csv.py`: Python script to convert `order.json` to `orders.csv`.
  - Additional files: Excel/ODS spreadsheets and PDFs related to orders and sales.
- **supplier/**: Information on supplier partnerships.
  - `suply.md`: Markdown guide on becoming a supplier to grocery chains for dates.
  - `supply.csv`: CSV version of supplier data.

## Setup

1. Ensure Python 3 is installed on your system.
2. Clone or download this repository to your local machine.
3. Navigate to the `shipments/` directory in your terminal.
4. Run scripts as needed (see Usage below).

## Usage

### Running Calculations
To analyze order data and generate summaries:
```bash
cd shipments
python calculate.py
```
This will output totals for pallets and pounds based on the data in `order.json`.

### Converting Data Formats
To update the CSV from JSON:
```bash
cd shipments
python transform_to_csv.py
```
This regenerates `orders.csv` from `order.json`.

### Viewing Data
- Open CSV/Excel files in VS Code or a spreadsheet application for manual review.
- PDFs can be viewed directly in VS Code or a PDF reader.

## Notes
- Order data includes details like customer names, box sizes (in pounds), grades (e.g., Fancy, Choice), and top colors (e.g., Red Orchid).
- Supplier information focuses on partnerships with grocery chains for dates supply.
- Current date context: January 16, 2026.

## Contributing
This is a personal repository for data analysis and accounting tasks. Update files as needed and commit changes to track versions.

## License
None specified.