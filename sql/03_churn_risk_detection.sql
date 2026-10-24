-- ==============================================================================
-- 03_CHURN_RISK_DETECTION.sql
-- Purpose: Identify customers who have broken their individual historical purchase
--          cadence (Days Since Last Order > 2x their average repurchase cycle).
-- Corporate Concept:
--   Static thresholds (e.g. 90 days) fail because frequent buyers churn much faster
--   than seasonal buyers. Personalized cadence anomaly detection is industry best-practice.
-- ==============================================================================

WITH ordered_purchases AS (
    -- Step 1: Window function to get previous order date per customer
    SELECT 
        customer_id,
        order_id,
        order_date,
        LAG(order_date, 1) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date ASC
        ) AS prev_order_date
    FROM fact_orders
    WHERE order_status = 'Completed'
),

order_intervals AS (
    -- Step 2: Calculate days between consecutive orders
    SELECT 
        customer_id,
        order_date,
        prev_order_date,
        CAST(julianday(order_date) - julianday(prev_order_date) AS INTEGER) AS days_between_orders
    FROM ordered_purchases
    WHERE prev_order_date IS NOT NULL
),

customer_cadence AS (
    -- Step 3: Compute customer's historical average repurchase cycle
    SELECT 
        customer_id,
        COUNT(days_between_orders) AS repeat_cycles_count,
        ROUND(AVG(days_between_orders), 1) AS avg_days_between_orders,
        MAX(order_date) AS last_order_date
    FROM order_intervals
    GROUP BY customer_id
)

SELECT 
    c.customer_id,
    cust.acquisition_channel,
    cust.country,
    c.repeat_cycles_count,
    c.avg_days_between_orders,
    c.last_order_date,
    CAST(julianday('2026-10-01') - julianday(c.last_order_date) AS INTEGER) AS days_since_last_order,
    ROUND(
        (CAST(julianday('2026-10-01') - julianday(c.last_order_date) AS REAL) / c.avg_days_between_orders), 
        2
    ) AS churn_risk_multiplier,
    CASE 
        WHEN (julianday('2026-10-01') - julianday(c.last_order_date)) > (2.5 * c.avg_days_between_orders) THEN 'Critical Churn Alert'
        WHEN (julianday('2026-10-01') - julianday(c.last_order_date)) > (1.5 * c.avg_days_between_orders) THEN 'Moderate Risk'
        ELSE 'Active / On Cadence'
    END AS retention_status
FROM customer_cadence c
JOIN dim_customers cust ON c.customer_id = cust.customer_id
WHERE c.repeat_cycles_count >= 2 -- Only evaluate customers with proven repeat pattern
ORDER BY churn_risk_multiplier DESC;
