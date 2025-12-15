"""
Data Loader - Loads YOUR real products from Excel files
Updated with duplicate prevention and better error handling
"""
import pandas as pd
import os
from datetime import timedelta

# Get paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

PRODUCTS_PATH = os.path.join(DATA_DIR, "ProductLibrary.xlsx")
COMPETITOR_PATH = os.path.join(DATA_DIR, "Competitor_Prices.xlsx")
ORDERS_PATH = os.path.join(DATA_DIR, "OrderProcessing.xlsx")


def compute_demand_index(orders_df, min_index=0.5, max_index=1.5):
    """Compute demand index from orders (simplified)."""
    if orders_df.empty:
        return pd.DataFrame(columns=["SKU", "demand_index"])
    
    df = orders_df.copy()
    df["SKU"] = df["SKU"].astype(str)
    df["quantity"] = df["Quantity"].fillna(0).astype(float)
    
    # Sum quantity per SKU
    demand = df.groupby("SKU")["quantity"].sum().reset_index()
    demand.columns = ["SKU", "total_qty"]
    
    # Normalize to 0.5-1.5 range
    if demand["total_qty"].max() > 0:
        demand["demand_index"] = 0.5 + (demand["total_qty"] / demand["total_qty"].max())
        demand["demand_index"] = demand["demand_index"].clip(min_index, max_index)
    else:
        demand["demand_index"] = 1.0
    
    return demand[["SKU", "demand_index"]]


def load_all_data():
    """Load all product data from Excel files."""
    
    # Load products and remove duplicates
    products_df = pd.read_excel(PRODUCTS_PATH, engine="openpyxl")
    products_df["SKU"] = products_df["SKU"].astype(str)
    
    # CRITICAL: Remove duplicate SKUs, keep first occurrence
    products_df = products_df.drop_duplicates(subset=['SKU'], keep='first')
    print(f"✓ Loaded {len(products_df)} unique products from ProductLibrary")
    
    # Load competitors and remove duplicates
    competitor_df = pd.read_excel(COMPETITOR_PATH, engine="openpyxl")
    competitor_df["SKU"] = competitor_df["SKU"].astype(str)
    competitor_df = competitor_df.drop_duplicates(subset=['SKU'], keep='first')
    print(f"✓ Loaded {len(competitor_df)} unique competitor records")
    
    # Load orders and compute demand
    try:
        orders_df = pd.read_excel(ORDERS_PATH, engine="openpyxl")
        orders_df["SKU"] = orders_df["SKU"].astype(str)
        demand_df = compute_demand_index(orders_df)
        print(f"✓ Calculated demand for {len(demand_df)} SKUs from orders")
    except Exception as e:
        print(f"⚠ Warning: Could not load orders - {e}")
        demand_df = pd.DataFrame(columns=["SKU", "demand_index"])
    
    # Merge competitor data (left join - keeps all products)
    comp_cols = ["SKU", "competitor1_price", "competitor2_price", "competitor3_price", "market_out_of_stock"]
    comp_cols = [c for c in comp_cols if c in competitor_df.columns]
    merged_df = products_df.merge(competitor_df[comp_cols], on="SKU", how="left")
    
    # Verify no duplicates after merge
    if merged_df['SKU'].duplicated().any():
        print(f"⚠ WARNING: Duplicates found after competitor merge!")
        merged_df = merged_df.drop_duplicates(subset=['SKU'], keep='first')
        print(f"✓ Removed duplicates, now have {len(merged_df)} products")
    
    # Merge demand (left join)
    merged_df = merged_df.merge(demand_df, on="SKU", how="left")
    merged_df["demand_index"] = merged_df["demand_index"].fillna(1.0)
    
    # Verify no duplicates after demand merge
    if merged_df['SKU'].duplicated().any():
        print(f"⚠ WARNING: Duplicates found after demand merge!")
        merged_df = merged_df.drop_duplicates(subset=['SKU'], keep='first')
        print(f"✓ Removed duplicates, now have {len(merged_df)} products")
    
    # Fill missing competitor data
    for col in ["competitor1_price", "competitor2_price", "competitor3_price"]:
        if col in merged_df.columns:
            merged_df[col] = merged_df[col].fillna(merged_df["Base_Price"])
    
    merged_df["market_out_of_stock"] = merged_df.get("market_out_of_stock", False).fillna(False)
    
    # Calculate competitor average
    price_cols = [c for c in ["competitor1_price", "competitor2_price", "competitor3_price"] if c in merged_df.columns]
    if price_cols:
        merged_df["competitor_avg"] = merged_df[price_cols].mean(axis=1)
    else:
        merged_df["competitor_avg"] = merged_df["Base_Price"]
    
    # Estimate cost (70% of base price)
    merged_df["cost"] = merged_df["Base_Price"] * 0.70
    
    # Final verification
    print(f"✓ Final dataset: {len(merged_df)} unique products")
    print(f"✓ Duplicate check: {merged_df['SKU'].duplicated().sum()} duplicates found")
    
    return merged_df


# Cache the data
_cached_data = None

def get_product_data(force_reload=False):
    """Get cached product data."""
    global _cached_data
    if _cached_data is None or force_reload:
        _cached_data = load_all_data()
    return _cached_data.copy()  # Return a copy to prevent modification