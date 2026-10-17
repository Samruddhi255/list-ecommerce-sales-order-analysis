# Methodology and Limitations

## Workflow
1. Obtain and extract the public Olist dataset.
2. Use the provided Colab notebook to inspect and combine selected source tables.
3. Export the consolidated CSV and connect it through Google Sheets.
4. Build scorecards, status/category charts, a time-series chart, and interactive controls in Looker Studio.
5. Run `src/analyze_dataset.py` to generate reproducible summary tables and local charts.

## Limitations
- The joined table contains item-level rows, so orders can occur on multiple rows.
- `SUM(price)` describes summed item prices, not automatically net revenue.
- `payment_value` may repeat across item rows because of joins; validate before drawing conclusions.
- Dashboard totals vary with selected filters. The supplied screenshot shows an active order-status exclusion filter.
- The dashboard is descriptive and does not establish why patterns occur.
