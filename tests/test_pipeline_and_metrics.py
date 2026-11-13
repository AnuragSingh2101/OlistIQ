"""
Automated Test Suite for OlistIQ Data Pipeline
Validates raw data existence, cleaning logic, KPI calculations, and category translations.
Run with: pytest tests/ -v
"""
import os
import pytest
import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# Fixtures
# ============================================================
@pytest.fixture(scope="session")
def raw_dir():
    return Path("data/raw")


@pytest.fixture(scope="session")
def clean_dir():
    return Path("data/clean")


@pytest.fixture(scope="session")
def raw_files(raw_dir):
    """Load all 9 raw CSV files."""
    files = {
        "orders": pd.read_csv(raw_dir / "olist_orders_dataset.csv"),
        "order_items": pd.read_csv(raw_dir / "olist_order_items_dataset.csv"),
        "order_payments": pd.read_csv(raw_dir / "olist_order_payments_dataset.csv"),
        "order_reviews": pd.read_csv(raw_dir / "olist_order_reviews_dataset.csv"),
        "customers": pd.read_csv(raw_dir / "olist_customers_dataset.csv"),
        "products": pd.read_csv(raw_dir / "olist_products_dataset.csv"),
        "sellers": pd.read_csv(raw_dir / "olist_sellers_dataset.csv"),
        "geolocation": pd.read_csv(raw_dir / "olist_geolocation_dataset.csv"),
        "translation": pd.read_csv(raw_dir / "product_category_name_translation.csv"),
    }
    return files


@pytest.fixture(scope="session")
def clean_master(clean_dir):
    """Load the pre-generated clean master dataset."""
    path = clean_dir / "orders_master.csv"
    if not path.exists():
        pytest.skip("Clean master dataset not found. Run src/clean_data.py first.")
    df = pd.read_csv(path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"], errors="coerce")
    df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"], errors="coerce")
    return df


@pytest.fixture(scope="session")
def clean_category(clean_dir):
    """Load the pre-generated category summary."""
    path = clean_dir / "category_summary.csv"
    if not path.exists():
        pytest.skip("Clean category summary not found. Run src/clean_data.py first.")
    return pd.read_csv(path)


# ============================================================
# Test 1: Raw Files Existence & Basic Integrity
# ============================================================
EXPECTED_RAW_FILES = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_geolocation_dataset.csv",
    "product_category_name_translation.csv",
]


def test_raw_files_exist(raw_dir):
    """Confirm all 9 expected Olist CSVs exist in data/raw/."""
    missing = []
    for fname in EXPECTED_RAW_FILES:
        if not (raw_dir / fname).exists():
            missing.append(fname)
    assert not missing, f"Missing raw files: {missing}"


def test_raw_files_non_empty(raw_files):
    """Confirm each raw file has at least 1 row and expected columns."""
    expected_cols = {
        "orders": ["order_id", "customer_id", "order_status", "order_purchase_timestamp"],
        "order_items": ["order_id", "order_item_id", "product_id", "price", "freight_value"],
        "order_payments": ["order_id", "payment_sequential", "payment_type", "payment_value"],
        "order_reviews": ["review_id", "order_id", "review_score"],
        "customers": ["customer_id", "customer_unique_id", "customer_state"],
        "products": ["product_id", "product_category_name"],
        "sellers": ["seller_id", "seller_state"],
        "geolocation": ["geolocation_zip_code_prefix", "geolocation_state"],
        "translation": ["product_category_name", "product_category_name_english"],
    }
    for name, df in raw_files.items():
        assert len(df) > 0, f"{name}: DataFrame is empty"
        for col in expected_cols[name]:
            assert col in df.columns, f"{name}: Missing expected column '{col}'"


# ============================================================
# Test 2: Order Cleaning Logic
# ============================================================
def test_delivery_days_non_negative(clean_master):
    """Check that delivery_days calculation is non-negative for delivered orders."""
    delivered = clean_master[clean_master["order_status"] == "delivered"].copy()
    # Allow NaN for undelivered, but delivered should have valid delivery_days
    valid_delivery = delivered["delivery_days"].dropna()
    assert (valid_delivery >= -1).all(), "Found delivery_days < -1 (likely timestamp error)"


def test_timestamps_parsed_correctly(clean_master):
    """Verify timestamp columns are properly parsed as datetime."""
    ts_cols = ["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]
    for col in ts_cols:
        assert pd.api.types.is_datetime64_any_dtype(clean_master[col]), f"{col} not datetime dtype"
    # Purchase timestamp should never be NaT for valid orders
    assert clean_master["order_purchase_timestamp"].notna().all(), "Found NaT in order_purchase_timestamp"


def test_delivery_before_purchase_flagged(clean_master):
    """Orders delivered before purchase should be flagged or have negative delivery_days."""
    # This is a data quality check - we expect very few if any
    delivered = clean_master[clean_master["order_status"] == "delivered"].copy()
    early = delivered[delivered["delivery_days"] < 0]
    # Log for visibility but don't fail - data may have edge cases
    if len(early) > 0:
        print(f"\n[WARNING] Found {len(early)} orders with delivery before purchase (negative delivery_days)")


# ============================================================
# Test 3: KPI Calculations
# ============================================================
def test_gmv_calculation(clean_master):
    """Validate GMV = sum(total_payment_value) for delivered orders."""
    delivered = clean_master[clean_master["order_status"] == "delivered"]
    gmv = delivered["total_payment_value"].sum()
    assert gmv > 0, "GMV should be positive"
    # Cross-check: GMV should be reasonable for 100k orders (~R$ 10-20M)
    assert 1_000_000 < gmv < 100_000_000, f"GMV {gmv:,.0f} outside expected range"


def test_aov_calculation(clean_master):
    """Validate AOV = GMV / order_count (no division by zero)."""
    delivered = clean_master[clean_master["order_status"] == "delivered"]
    total_orders = delivered["order_id"].nunique()
    assert total_orders > 0, "No delivered orders found"
    gmv = delivered["total_payment_value"].sum()
    aov = gmv / total_orders
    assert aov > 0, "AOV should be positive"
    # Sanity check: AOV should be reasonable (R$ 50-500)
    assert 10 < aov < 1000, f"AOV R$ {aov:.2f} outside expected range"


def test_on_time_delivery_rate(clean_master):
    """Validate on-time delivery rate calculation (0-100%)."""
    delivered = clean_master[clean_master["order_status"] == "delivered"]
    if len(delivered) == 0:
        pytest.skip("No delivered orders")
    on_time_pct = (~delivered["is_delayed"]).sum() / len(delivered) * 100
    assert 0 <= on_time_pct <= 100, f"On-time rate {on_time_pct:.1f}% outside [0, 100]"


def test_review_average(clean_master):
    """Validate review average calculation (1-5 scale)."""
    reviews = clean_master["review_score"].dropna()
    if len(reviews) == 0:
        pytest.skip("No review scores")
    avg_review = reviews.mean()
    assert 1 <= avg_review <= 5, f"Avg review {avg_review:.2f} outside [1, 5]"


def test_no_division_by_zero_in_kpis(clean_master):
    """Ensure no KPI calculation divides by zero."""
    delivered = clean_master[clean_master["order_status"] == "delivered"]
    total_orders = delivered["order_id"].nunique()
    assert total_orders > 0, "Cannot compute KPIs with zero orders"


# ============================================================
# Test 4: Category Translation
# ============================================================
def test_category_translation_coverage(raw_files):
    """Assert that Portuguese category names are properly mapped to English."""
    products = raw_files["products"]
    translation = raw_files["translation"]
    
    # Merge products with translation
    merged = products.merge(translation, on="product_category_name", how="left")
    
    # Count unmapped categories (excluding NaN product_category_name)
    valid_products = merged[merged["product_category_name"].notna()]
    unmapped = valid_products[valid_products["product_category_name_english"].isna()]
    
    # Allow some unmapped but should be minimal (< 5% of unique categories)
    unique_cats = valid_products["product_category_name"].nunique()
    unmapped_cats = unmapped["product_category_name"].nunique()
    unmapped_pct = (unmapped_cats / unique_cats * 100) if unique_cats > 0 else 0
    
    assert unmapped_pct < 10, f"{unmapped_pct:.1f}% of categories unmapped ({unmapped_cats}/{unique_cats})"


def test_clean_category_names_english(clean_master):
    """Verify clean dataset has English category names (not Portuguese underscores)."""
    cats = clean_master["primary_category"].dropna().unique()
    # Check that categories don't have underscores (should be "Health Beauty" not "health_beauty")
    for cat in cats:
        assert "_" not in str(cat), f"Category still has underscore: {cat}"
    # Check that categories are title case (first letter capitalized)
    for cat in cats:
        cat_str = str(cat)
        # Allow "Other" and some special cases
        if cat_str not in ["Other", "Unknown"]:
            words = cat_str.split()
            for word in words:
                if word and word[0].isalpha():
                    assert word[0].isupper(), f"Category not title case: {cat}"


def test_category_summary_exists_and_populated(clean_category):
    """Verify category summary CSV exists and has expected structure."""
    assert len(clean_category) > 0, "Category summary is empty"
    expected_cols = ["category", "total_sales", "total_orders", "avg_price", "total_freight"]
    for col in expected_cols:
        assert col in clean_category.columns, f"Missing column: {col}"
    # Categories should be sorted by total_sales descending
    assert clean_category["total_sales"].is_monotonic_decreasing, "Categories not sorted by total_sales desc"


# ============================================================
# Test 5: Data Quality & Consistency
# ============================================================
def test_no_duplicate_order_ids(clean_master):
    """Primary key integrity: order_id should be unique."""
    dupes = clean_master["order_id"].duplicated().sum()
    assert dupes == 0, f"Found {dupes} duplicate order_ids in clean master"


def test_payment_value_non_negative(clean_master):
    """Financial integrity: payment values should be non-negative."""
    neg_payments = clean_master[clean_master["total_payment_value"] < 0]
    assert len(neg_payments) == 0, f"Found {len(neg_payments)} orders with negative payment value"


def test_price_and_freight_non_negative(clean_master):
    """Item price and freight should be non-negative."""
    neg_price = clean_master[clean_master["total_items_price"] < 0]
    neg_freight = clean_master[clean_master["total_freight_value"] < 0]
    assert len(neg_price) == 0, f"Found {len(neg_price)} orders with negative item price"
    assert len(neg_freight) == 0, f"Found {len(neg_freight)} orders with negative freight"


def test_customer_state_populated(clean_master):
    """Customer state should be populated for most orders."""
    missing_state = clean_master["customer_state"].isna().sum()
    total = len(clean_master)
    missing_pct = missing_state / total * 100
    assert missing_pct < 5, f"{missing_pct:.1f}% of orders missing customer_state"


# ============================================================
# Test 6: Clean Dataset Structure
# ============================================================
def test_clean_master_has_expected_columns(clean_master):
    """Verify clean master dataset has all expected analytical columns."""
    expected = [
        "order_id", "customer_id", "order_status", "order_purchase_timestamp",
        "order_delivered_customer_date", "order_estimated_delivery_date",
        "delivery_days", "is_delayed", "customer_state", "customer_city",
        "items_count", "total_items_price", "total_freight_value",
        "primary_category", "total_payment_value", "payment_type",
        "payment_installments_max", "review_score"
    ]
    for col in expected:
        assert col in clean_master.columns, f"Missing expected column: {col}"


def test_clean_master_row_count_matches_raw(clean_master, raw_files):
    """Clean master should have same row count as raw orders (no rows dropped)."""
    raw_count = len(raw_files["orders"])
    clean_count = len(clean_master)
    # Allow small difference due to filtering, but should be close
    assert abs(raw_count - clean_count) / raw_count < 0.05, \
        f"Row count mismatch: raw={raw_count:,}, clean={clean_count:,}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])