"""
OlistIQ - Data Cleaning and Transformation Pipeline
Loads raw Olist CSVs, processes timestamps, calculates delivery & financial KPIs,
merges product translations, and outputs an optimized clean master dataset.
"""

from pathlib import Path
import pandas as pd
import numpy as np


RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")


def process_olistiq_data():
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    print("Loading raw CSV files...")

    # Load core tables
    orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
    order_items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
    order_payments = pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv")
    order_reviews = pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv")
    customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
    products = pd.read_csv(RAW_DIR / "olist_products_dataset.csv")
    translation = pd.read_csv(RAW_DIR / "product_category_name_translation.csv")

    print(f"Total raw orders: {len(orders):,}")

    # 1. Parse Timestamps
    timestamp_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in timestamp_cols:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    # Filter to delivered orders with purchase and delivery timestamps
    orders = orders.dropna(subset=["order_purchase_timestamp"]).copy()

    # Derived time & delivery metrics
    orders["order_year"] = orders["order_purchase_timestamp"].dt.year
    orders["order_year_month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)
    orders["order_date"] = orders["order_purchase_timestamp"].dt.date

    # Delivery performance metrics (in calendar days)
    orders["delivery_days"] = (
        orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / (24 * 3600)

    orders["estimated_days"] = (
        orders["order_estimated_delivery_date"] - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / (24 * 3600)

    # Delay flag: delivered after estimated delivery date
    orders["is_delayed"] = orders["order_delivered_customer_date"] > orders["order_estimated_delivery_date"]

    # 2. Process Product Categories with English Translation
    products = products.merge(translation, on="product_category_name", how="left")
    products["product_category_name_english"] = products[
        "product_category_name_english"
    ].fillna(products["product_category_name"]).fillna("other")
    products["product_category_name_english"] = (
        products["product_category_name_english"].str.replace("_", " ").str.title()
    )

    # 3. Aggregate Order Items (Item count, Total Price, Total Freight)
    items_with_prod = order_items.merge(
        products[["product_id", "product_category_name_english"]],
        on="product_id",
        how="left"
    )

    # Find dominant category per order
    def get_mode_or_default(x):
        if x.empty or x.mode().empty:
            return "Other"
        return x.mode().iloc[0]
    
    category_per_order = (
        items_with_prod.groupby("order_id")["product_category_name_english"]
        .agg(get_mode_or_default)
        .reset_index()
        .rename(columns={"product_category_name_english": "primary_category"})
    )

    items_agg = items_with_prod.groupby("order_id").agg(
        items_count=("order_item_id", "count"),
        total_items_price=("price", "sum"),
        total_freight_value=("freight_value", "sum")
    ).reset_index()

    items_agg = items_agg.merge(category_per_order, on="order_id", how="left")

    # 4. Aggregate Payments (Total Payment Value, Dominant Payment Type)
    payments_agg = order_payments.groupby("order_id").agg(
        total_payment_value=("payment_value", "sum"),
        payment_installments_max=("payment_installments", "max"),
        payment_type=("payment_type", lambda x: x.mode().iloc[0] if not x.empty else "unknown")
    ).reset_index()

    # 5. Aggregate Reviews (Mean Review Score)
    reviews_agg = order_reviews.groupby("order_id").agg(
        review_score=("review_score", "mean")
    ).reset_index()

    # 6. Merge Everything into Master Orders Dataset
    master_df = orders.merge(customers[["customer_id", "customer_unique_id", "customer_city", "customer_state"]], on="customer_id", how="left")
    master_df = master_df.merge(items_agg, on="order_id", how="left")
    master_df = master_df.merge(payments_agg, on="order_id", how="left")
    master_df = master_df.merge(reviews_agg, on="order_id", how="left")

    # Fill defaults
    master_df["total_payment_value"] = master_df["total_payment_value"].fillna(
        master_df["total_items_price"].fillna(0) + master_df["total_freight_value"].fillna(0)
    )
    master_df["primary_category"] = master_df["primary_category"].fillna("Other")
    master_df["payment_type"] = master_df["payment_type"].fillna("unknown").str.replace("_", " ").str.title()
    master_df["items_count"] = master_df["items_count"].fillna(1).astype(int)

    # Save to clean directory
    out_csv = CLEAN_DIR / "orders_master.csv"
    master_df.to_csv(out_csv, index=False)
    print(f"[SUCCESS] Clean master dataset saved: {out_csv} ({len(master_df):,} records)")

    # Also generate category summary table for ultra-fast dashboard queries
    cat_summary = items_with_prod.groupby("product_category_name_english").agg(
        total_sales=("price", "sum"),
        total_orders=("order_id", "nunique"),
        avg_price=("price", "mean"),
        total_freight=("freight_value", "sum")
    ).reset_index().rename(columns={"product_category_name_english": "category"})
    cat_summary = cat_summary.sort_values(by="total_sales", ascending=False)
    cat_summary.to_csv(CLEAN_DIR / "category_summary.csv", index=False)
    print(f"[SUCCESS] Category summary saved ({len(cat_summary):,} categories)")

    return master_df


if __name__ == "__main__":
    process_olistiq_data()

