"""
AI Sentiment & Churn Driver Classifier
Author: Antigravity Pair-Programming
Purpose: Classifies unstructured customer reviews into sentiment and operational root causes
         (Shipping, Quality, Support, Billing) to identify revenue-at-risk drivers.
"""

import os
import re
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "retention_warehouse.db")
FEEDBACK_CSV = os.path.join(DATA_DIR, "customer_feedback.csv")
ENRICHED_CSV = os.path.join(DATA_DIR, "customer_feedback_enriched.csv")

print("[*] Starting AI Sentiment & Churn Driver Tagging pipeline...")

df_feedback = pd.read_csv(FEEDBACK_CSV)

# Operational Churn Driver Taxonomy (Corporate Rule Engine / Prompt Specs)
DRIVER_PATTERNS = {
    "Shipping & Delivery": [r"\bshipping\b", r"\bdelayed\b", r"\bdelivery\b", r"\btracking\b", r"\barrive\b"],
    "Product Quality & Defects": [r"\bquality\b", r"\bscratches\b", r"\bplastic\b", r"\bcheap\b", r"\bstopped working\b", r"\bdefective\b", r"\bconnection drops\b", r"\bbluetooth\b"],
    "Customer Support": [r"\bsupport\b", r"\bticket\b", r"\brespond\b", r"\bservice\b"],
    "Billing & Refunds": [r"\bbilling\b", r"\bcharged\b", r"\bcredit card\b", r"\brefund\b"],
    "Product Satisfaction & Praise": [r"\blove\b", r"\bbest purchase\b", r"\bexceeded\b", r"\bflawlessly\b", r"\bgreat product\b", r"\bsolid\b", r"\bpremium\b"]
}

def classify_sentiment(rating):
    if rating >= 4:
        return "Positive"
    elif rating == 3:
        return "Neutral"
    else:
        return "Negative"

def extract_primary_driver(text):
    text_lower = str(text).lower()
    for category, patterns in DRIVER_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return category
    return "Other / General"

# Apply tagging
df_feedback["sentiment"] = df_feedback["rating"].apply(classify_sentiment)
df_feedback["churn_driver_category"] = df_feedback["review_text"].apply(extract_primary_driver)

# Assign a numeric sentiment score: Positive = +1.0, Neutral = 0.0, Negative = -1.0
sentiment_score_map = {"Positive": 1.0, "Neutral": 0.0, "Negative": -1.0}
df_feedback["sentiment_score"] = df_feedback["sentiment"].map(sentiment_score_map)

# Save enriched data
df_feedback.to_csv(ENRICHED_CSV, index=False)

# Update SQLite Database
conn = sqlite3.connect(DB_PATH)
df_feedback.to_sql("customer_feedback_enriched", conn, if_exists="replace", index=False)
conn.close()

print("[SUCCESS] Feedback successfully classified and enriched!")
print(f" - Enriched CSV saved to: {ENRICHED_CSV}")
print("\n--- Sentiment Distribution ---")
print(df_feedback["sentiment"].value_counts())
print("\n--- Churn Driver Categories ---")
print(df_feedback["churn_driver_category"].value_counts())
