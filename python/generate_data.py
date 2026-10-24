"""
Data Generation Script: Enterprise Customer Retention & Churn Analytics
Author: Antigravity Pair-Programming
Purpose: Generates a realistic star-schema transactional dataset with customer profiles,
         repeat order cycles (cohorts), returns, and qualitative feedback text.
"""

import sqlite3
import random
import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Set seed for reproducible results
np.random.seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "retention_warehouse.db")

os.makedirs(DATA_DIR, exist_ok=True)

print(f"[*] Generating enterprise dataset in {DATA_DIR}...")

# ---------------------------------------------------------------------------
# 1. GENERATE DIM_CUSTOMERS (1,200 Customers)
# ---------------------------------------------------------------------------
NUM_CUSTOMERS = 1200
CHANNELS = ["Paid Search", "Organic SEO", "Social Ads", "Email Referral", "Affiliate"]
COUNTRIES = ["United States", "United Kingdom", "Germany", "Canada", "Australia"]
CUSTOMER_TYPES = ["Individual", "SMB", "Corporate"]

start_date = datetime(2024, 1, 1)
end_date = datetime(2026, 10, 1)
date_range_days = (end_date - start_date).days

customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    signup_offset = random.randint(0, date_range_days - 60)
    c_signup = start_date + timedelta(days=signup_offset)
    
    # Retention behavior profile assigned at creation
    # 40% One-time buyers, 35% Casual repeaters, 15% Loyal/Champions, 10% Churned after high spend
    persona = np.random.choice(
        ["one_time", "casual", "loyal", "churned_vip"],
        p=[0.40, 0.35, 0.15, 0.10]
    )
    
    customers.append({
        "customer_id": f"CUST-{i:05d}",
        "signup_date": c_signup.strftime("%Y-%m-%d"),
        "acquisition_channel": random.choices(CHANNELS, weights=[0.35, 0.25, 0.20, 0.12, 0.08])[0],
        "country": random.choices(COUNTRIES, weights=[0.45, 0.20, 0.15, 0.12, 0.08])[0],
        "customer_type": random.choices(CUSTOMER_TYPES, weights=[0.70, 0.20, 0.10])[0],
        "_persona": persona
    })

df_customers = pd.DataFrame(customers)

# ---------------------------------------------------------------------------
# 2. GENERATE DIM_PRODUCTS (50 Products across 4 Categories)
# ---------------------------------------------------------------------------
PRODUCTS_DATA = [
    # Electronics
    ("Noise-Cancelling Headphones Pro", "Electronics", 180.0, 75.0),
    ("Wireless Mechanical Keyboard", "Electronics", 95.0, 35.0),
    ("Ultra-HD 4K Monitor 27-inch", "Electronics", 320.0, 160.0),
    ("USB-C Multi-Port Docking Station", "Electronics", 65.0, 22.0),
    ("Smartwatch Fitness Tracker V2", "Electronics", 140.0, 50.0),
    ("Ergonomic Vertical Mouse", "Electronics", 45.0, 15.0),
    ("High-Speed Wireless Charger", "Electronics", 30.0, 9.0),
    # Office & Furniture
    ("Ergonomic Mesh Office Chair", "Office & Furniture", 250.0, 110.0),
    ("Adjustable Standing Desk 48x30", "Office & Furniture", 380.0, 180.0),
    ("Monitor Arm Heavy Duty", "Office & Furniture", 55.0, 18.0),
    ("Under-Desk Cable Management Tray", "Office & Furniture", 25.0, 7.0),
    ("Anti-Fatigue Standing Mat", "Office & Furniture", 40.0, 12.0),
    # Apparel & Lifestyle
    ("Tech Merino Wool Hoodie", "Apparel & Lifestyle", 85.0, 28.0),
    ("Commuter Waterproof Backpack", "Apparel & Lifestyle", 110.0, 38.0),
    ("All-Weather Running Jacket", "Apparel & Lifestyle", 95.0, 32.0),
    ("Insulated Stainless Water Bottle", "Apparel & Lifestyle", 28.0, 8.0),
    ("Polarized UV Sunglasses", "Apparel & Lifestyle", 60.0, 15.0),
    # Home & Smart Living
    ("Smart LED Ambient Light Bar", "Home & Smart Living", 45.0, 14.0),
    ("Aroma Essential Oil Diffuser", "Home & Smart Living", 35.0, 10.0),
    ("Smart Air Purifier HEPA H13", "Home & Smart Living", 160.0, 70.0),
    ("Robotic Vacuum Cleaner Slim", "Home & Smart Living", 280.0, 120.0),
    ("Ceramic Pour-Over Coffee Kit", "Home & Smart Living", 42.0, 12.0)
]

products = []
for idx, (p_name, p_cat, p_price, p_cost) in enumerate(PRODUCTS_DATA, 1):
    products.append({
        "product_id": f"PROD-{idx:04d}",
        "product_name": p_name,
        "category": p_cat,
        "unit_price": p_price,
        "unit_cost": p_cost
    })
df_products = pd.DataFrame(products)

# ---------------------------------------------------------------------------
# 3. GENERATE FACT_ORDERS (Realistic Repeat / Churn Purchase Behavior)
# ---------------------------------------------------------------------------
orders = []
order_counter = 1
PAYMENT_METHODS = ["Credit Card", "PayPal", "Apple Pay", "Klarna / Buy-Now-Pay-Later", "Direct Debit"]

for _, cust in df_customers.iterrows():
    c_id = cust["customer_id"]
    c_signup = datetime.strptime(cust["signup_date"], "%Y-%m-%d")
    persona = cust["_persona"]
    
    # Determine number of orders based on persona
    if persona == "one_time":
        num_orders = 1
    elif persona == "casual":
        num_orders = random.randint(2, 4)
    elif persona == "loyal":
        num_orders = random.randint(5, 12)
    else:  # churned_vip: purchased heavily early, then completely stopped
        num_orders = random.randint(4, 7)
    
    current_order_date = c_signup + timedelta(days=random.randint(0, 5))
    
    for o_idx in range(num_orders):
        if current_order_date > end_date:
            break
            
        # Select 1 to 3 items per order
        num_items = random.choices([1, 2, 3], weights=[0.65, 0.25, 0.10])[0]
        chosen_products = random.sample(products, num_items)
        
        for item in chosen_products:
            qty = random.choices([1, 2, 3], weights=[0.80, 0.15, 0.05])[0]
            unit_price = item["unit_price"]
            
            # 15% chance of discount
            has_discount = random.random() < 0.20
            discount_pct = random.choice([0.10, 0.15, 0.20]) if has_discount else 0.0
            discount_amount = round(unit_price * qty * discount_pct, 2)
            total_amount = round((unit_price * qty) - discount_amount, 2)
            
            # Status: Completed (91%), Returned (6%), Cancelled (3%)
            order_status = random.choices(["Completed", "Returned", "Cancelled"], weights=[0.91, 0.06, 0.03])[0]
            
            orders.append({
                "order_id": f"ORD-{order_counter:06d}",
                "customer_id": c_id,
                "order_date": current_order_date.strftime("%Y-%m-%d"),
                "product_id": item["product_id"],
                "quantity": qty,
                "unit_price": unit_price,
                "discount_amount": discount_amount,
                "total_amount": total_amount,
                "payment_method": random.choices(PAYMENT_METHODS, weights=[0.45, 0.25, 0.15, 0.10, 0.05])[0],
                "order_status": order_status
            })
            order_counter += 1
            
        # Spacing to next order
        if persona == "loyal":
            days_gap = random.randint(20, 60)
        elif persona == "churned_vip":
            # Rapid purchases early, then stops after 3-4 months
            days_gap = random.randint(15, 35) if o_idx < 3 else random.randint(250, 400)
        else: # casual
            days_gap = random.randint(60, 150)
            
        current_order_date += timedelta(days=days_gap)

df_orders = pd.DataFrame(orders)

# ---------------------------------------------------------------------------
# 4. GENERATE CUSTOMER_FEEDBACK (Qualitative Unstructured Data)
# ---------------------------------------------------------------------------
POSITIVE_REVIEWS = [
    "Absolutely love the build quality! Delivered within 2 days.",
    "Best purchase I made this year. Setup was effortless and customer support answered immediately.",
    "Exceeded expectations. Premium feel and battery life is stellar.",
    "Works flawlessly with my MacBook setup. High recommendation!",
    "Great product, fair price. Will definitely buy again from this store.",
    "Solid performance and looks great on my home office desk."
]

NEGATIVE_REVIEWS = [
    "Shipping delayed by over 10 days with zero tracking updates. Very disappointed.",
    "Item arrived with scratches on the frame. Packaging was damaged.",
    "Stopped working after 3 weeks. Customer service took 5 days to respond to my ticket.",
    "Quality is far below what was advertised. Plastic feels cheap and squeaky.",
    "Billing charged my credit card twice and refund process took 2 weeks.",
    "Bluetooth connection drops constantly. Expected much better at this price point."
]

NEUTRAL_REVIEWS = [
    "Decent product for the price. Does the job, but nothing extraordinary.",
    "Delivery was standard. Product matches description.",
    "Instructions were somewhat confusing, but figured it out eventually."
]

feedbacks = []
feedback_id = 1

# Sample 30% of completed or returned orders for reviews
sampled_orders = df_orders[df_orders["order_status"].isin(["Completed", "Returned"])].sample(
    n=min(2200, len(df_orders)), random_state=42
)

for _, o in sampled_orders.iterrows():
    # If order was returned, 80% negative review
    if o["order_status"] == "Returned":
        rating = random.choices([1, 2], weights=[0.70, 0.30])[0]
        review_text = random.choice(NEGATIVE_REVIEWS)
    else:
        # Completed orders
        rating = random.choices([1, 2, 3, 4, 5], weights=[0.08, 0.07, 0.15, 0.35, 0.35])[0]
        if rating <= 2:
            review_text = random.choice(NEGATIVE_REVIEWS)
        elif rating == 3:
            review_text = random.choice(NEUTRAL_REVIEWS)
        else:
            review_text = random.choice(POSITIVE_REVIEWS)
            
    f_date = datetime.strptime(o["order_date"], "%Y-%m-%d") + timedelta(days=random.randint(2, 7))
    
    feedbacks.append({
        "feedback_id": f"FB-{feedback_id:05d}",
        "order_id": o["order_id"],
        "customer_id": o["customer_id"],
        "rating": rating,
        "review_text": review_text,
        "feedback_date": f_date.strftime("%Y-%m-%d")
    })
    feedback_id += 1

df_feedbacks = pd.DataFrame(feedbacks)

# Clean temporary persona column
df_customers_clean = df_customers.drop(columns=["_persona"])

# ---------------------------------------------------------------------------
# 5. EXPORT TO SQLITE DATABASE & CSVs
# ---------------------------------------------------------------------------
# SQLite
conn = sqlite3.connect(DB_PATH)
df_customers_clean.to_sql("dim_customers", conn, if_exists="replace", index=False)
df_products.to_sql("dim_products", conn, if_exists="replace", index=False)
df_orders.to_sql("fact_orders", conn, if_exists="replace", index=False)
df_feedbacks.to_sql("customer_feedback", conn, if_exists="replace", index=False)
conn.close()

# CSV files for Power BI direct import
df_customers_clean.to_csv(os.path.join(DATA_DIR, "dim_customers.csv"), index=False)
df_products.to_csv(os.path.join(DATA_DIR, "dim_products.csv"), index=False)
df_orders.to_csv(os.path.join(DATA_DIR, "fact_orders.csv"), index=False)
df_feedbacks.to_csv(os.path.join(DATA_DIR, "customer_feedback.csv"), index=False)

print("\n[SUCCESS] Dataset generated successfully!")
print(f" - dim_customers: {len(df_customers_clean):,} records")
print(f" - dim_products:  {len(df_products):,} records")
print(f" - fact_orders:   {len(df_orders):,} records")
print(f" - feedback:      {len(df_feedbacks):,} records")
print(f" - Database:      {DB_PATH}")
