"""
Load and verify all 9 Olist CSV files.
Run this script to confirm all files exist and can be read.
"""
import os
import pandas as pd
from pathlib import Path

# 9 expected Olist CSV files
EXPECTED_FILES = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_geolocation_dataset.csv",
    "product_category_name_translation.csv"
]

RAW_DIR = Path("data/raw")


def check_file_exists(filename: str) -> bool:
    """Check if a file exists in data/raw/"""
    path = RAW_DIR / filename
    return path.exists()


def get_file_info(filename: str) -> dict:
    """Get basic file info: size, rows, columns"""
    path = RAW_DIR / filename
    if not path.exists():
        return {"exists": False}
    
    # File size in MB
    size_mb = path.stat().st_size / (1024 * 1024)
    
    # Try reading with pandas (peek first 5 rows)
    try:
        df = pd.read_csv(path, nrows=5)
        # Get full row count (may be slow for large files)
        full_df = pd.read_csv(path)
        rows, cols = full_df.shape
        dtypes = full_df.dtypes.to_dict()
        missing = full_df.isnull().sum().to_dict()
        
        return {
            "exists": True,
            "size_mb": round(size_mb, 2),
            "rows": rows,
            "cols": cols,
            "columns": list(full_df.columns),
            "dtypes": {k: str(v) for k, v in dtypes.items()},
            "missing_counts": missing,
            "sample": df.head().to_dict()
        }
    except Exception as e:
        return {"exists": True, "error": str(e)}


def main():
    print("=" * 70)
    print("OLIST DATASET VERIFICATION")
    print("=" * 70)
    
    all_exist = True
    results = {}
    
    for fname in EXPECTED_FILES:
        print(f"\n[FILE] Checking: {fname}")
        info = get_file_info(fname)
        results[fname] = info
        
        if not info.get("exists"):
            print(f"   [MISSING]")
            all_exist = False
        else:
            if "error" in info:
                print(f"   [ERROR] reading: {info['error']}")
            else:
                print(f"   [OK] Found ({info['size_mb']} MB, {info['rows']:,} rows, {info['cols']} cols)")
                print(f"      Columns: {info['columns']}")
    
    print("\n" + "=" * 70)
    if all_exist:
        print("[SUCCESS] ALL 9 FILES PRESENT AND READABLE")
    else:
        print("[FAIL] SOME FILES MISSING - Download from Kaggle and place in data/raw/")
        print("   https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    main()