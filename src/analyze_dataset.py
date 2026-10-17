"""Generate descriptive summaries and charts for the Olist dashboard project."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "olist_combined_dataset.csv"
TABLES = ROOT / "reports" / "tables"
CHARTS = ROOT / "reports" / "charts"


def main():
    TABLES.mkdir(parents=True, exist_ok=True)
    CHARTS.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA, low_memory=False)

    # Parse timestamps used in the time-series summary.
    if "order_purchase_timestamp" in df.columns:
        df["order_purchase_timestamp"] = pd.to_datetime(
            df["order_purchase_timestamp"], errors="coerce"
        )

    overview = pd.DataFrame({
        "metric": ["joined_rows", "columns", "unique_orders", "unique_customers", "missing_cells"],
        "value": [len(df), len(df.columns),
                  df["order_id"].nunique() if "order_id" in df else None,
                  df["customer_id"].nunique() if "customer_id" in df else None,
                  int(df.isna().sum().sum())]
    })
    overview.to_csv(TABLES / "dataset_overview.csv", index=False)
    df.isna().sum().rename("missing_count").to_csv(TABLES / "missing_values_by_column.csv")

    if {"order_status", "price"}.issubset(df.columns):
        status = (df.groupby("order_status", dropna=False)
                  .agg(sum_item_price=("price", "sum"),
                       unique_orders=("order_id", "nunique"))
                  .reset_index().sort_values("sum_item_price", ascending=False))
        status.to_csv(TABLES / "price_and_orders_by_status.csv", index=False)
        plot = status.sort_values("sum_item_price")
        plt.figure(figsize=(9, 5))
        plt.barh(plot["order_status"].fillna("Unknown").astype(str), plot["sum_item_price"])
        plt.xlabel("Sum of item prices")
        plt.ylabel("Order status")
        plt.title("Sum of Item Prices by Order Status")
        plt.tight_layout()
        plt.savefig(CHARTS / "item_price_by_status.png", dpi=160)
        plt.close()

    if {"product_category_name", "price"}.issubset(df.columns):
        category = (df.assign(product_category_name=df["product_category_name"].fillna("Unknown"))
                    .groupby("product_category_name", dropna=False)
                    .agg(sum_item_price=("price", "sum"),
                         unique_orders=("order_id", "nunique"))
                    .reset_index().sort_values("sum_item_price", ascending=False))
        category.to_csv(TABLES / "price_by_category.csv", index=False)
        top = category.head(15).sort_values("sum_item_price")
        plt.figure(figsize=(10, 7))
        plt.barh(top["product_category_name"].astype(str), top["sum_item_price"])
        plt.xlabel("Sum of item prices")
        plt.ylabel("Product category")
        plt.title("Top 15 Categories by Sum of Item Prices")
        plt.tight_layout()
        plt.savefig(CHARTS / "item_price_by_category_top15.png", dpi=160)
        plt.close()

    if {"order_purchase_timestamp", "price"}.issubset(df.columns):
        valid = df.dropna(subset=["order_purchase_timestamp"]).copy()
        valid["purchase_month"] = valid["order_purchase_timestamp"].dt.to_period("M").astype(str)
        monthly = (valid.groupby("purchase_month")
                   .agg(sum_item_price=("price", "sum"),
                        unique_orders=("order_id", "nunique"))
                   .reset_index().sort_values("purchase_month"))
        monthly.to_csv(TABLES / "monthly_item_price_trend.csv", index=False)
        plt.figure(figsize=(11, 5))
        plt.plot(monthly["purchase_month"], monthly["sum_item_price"], marker="o", linewidth=1.5)
        plt.xticks(rotation=60, ha="right")
        plt.xlabel("Purchase month")
        plt.ylabel("Sum of item prices")
        plt.title("Monthly Product-Price Trend")
        plt.tight_layout()
        plt.savefig(CHARTS / "monthly_item_price_trend.png", dpi=160)
        plt.close()

    print(f"Analysis complete. Outputs saved under: {ROOT / 'reports'}")
    print(f"Rows: {len(df):,} | Columns: {len(df.columns)}")
    print("Caution: payment_value can be duplicated in the joined item-level dataset; validate before aggregating it.")

if __name__ == "__main__":
    main()
