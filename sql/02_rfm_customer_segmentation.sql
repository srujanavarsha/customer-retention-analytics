-- ==============================================================================
-- 02_RFM_CUSTOMER_SEGMENTATION.sql
-- Purpose: Classify customers into actionable behavioral segments using RFM Analysis:
--   Recency (R)   : Days elapsed since customer's last purchase.
--   Frequency (F) : Count of distinct orders placed.
--   Monetary (M)  : Total net revenue ($) spent by the customer.
-- ==============================================================================

WITH rfm_base AS (
    SELECT 
        o.customer_id,
        -- Reference snapshot date: 2026-10-01
        CAST(julianday('2026-10-01') - julianday(MAX(o.order_date)) AS INTEGER) AS recency_days,
        COUNT(DISTINCT o.order_id) AS frequency_orders,
        ROUND(SUM(o.total_amount), 2) AS monetary_spend
    FROM fact_orders o
    WHERE o.order_status = 'Completed'
    GROUP BY o.customer_id
),

rfm_quartiles AS (
    SELECT 
        customer_id,
        recency_days,
        frequency_orders,
        monetary_spend,
        -- Recency: Lower days is BETTER, so invert quartile (1 = highest days/worst, 4 = lowest days/best)
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,
        -- Frequency: Higher orders is better (1 = lowest, 4 = highest)
        NTILE(4) OVER (ORDER BY frequency_orders ASC) AS f_score,
        -- Monetary: Higher spend is better (1 = lowest, 4 = highest)
        NTILE(4) OVER (ORDER BY monetary_spend ASC) AS m_score
    FROM rfm_base
)

SELECT 
    r.customer_id,
    c.acquisition_channel,
    c.country,
    c.customer_type,
    r.recency_days,
    r.frequency_orders,
    r.monetary_spend,
    r.r_score,
    r.f_score,
    r.m_score,
    (CAST(r.r_score AS TEXT) || CAST(r.f_score AS TEXT) || CAST(r.m_score AS TEXT)) AS rfm_combined_score,
    CASE
        WHEN r.r_score >= 3 AND r.f_score >= 3 AND r.m_score >= 3 THEN 'Champions'
        WHEN r.r_score >= 3 AND r.f_score >= 2 THEN 'Loyal Customers'
        WHEN r.r_score >= 3 AND r.f_score = 1 THEN 'New & Promising'
        WHEN r.r_score <= 2 AND (r.f_score >= 3 OR r.m_score >= 3) THEN 'At Risk (High Value Churn)'
        WHEN r.r_score = 1 AND r.f_score = 1 THEN 'Lost / Dormant'
        ELSE 'Needs Nurturing'
    END AS customer_segment
FROM rfm_quartiles r
JOIN dim_customers c ON r.customer_id = c.customer_id
ORDER BY r.monetary_spend DESC;
