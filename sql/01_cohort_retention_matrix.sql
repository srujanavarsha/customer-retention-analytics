-- ==============================================================================
-- 01_COHORT_RETENTION_MATRIX.sql
-- Purpose: Calculate customer cohort retention rates on a monthly basis.
-- Corporate Concept:
--   Cohort Month = The calendar month when a customer made their first purchase.
--   Order Month  = The calendar month of subsequent purchases.
--   Cohort Index = The number of months elapsed between Cohort Month and Order Month (0, 1, 2, ...).
-- ==============================================================================

WITH customer_first_purchase AS (
    -- Step 1: Identify the cohort month (first completed order) for each customer
    SELECT 
        customer_id,
        MIN(order_date) AS first_order_date,
        strftime('%Y-%m-01', MIN(order_date)) AS cohort_month
    FROM fact_orders
    WHERE order_status = 'Completed'
    GROUP BY customer_id
),

customer_orders AS (
    -- Step 2: Extract distinct active months for each customer
    SELECT DISTINCT
        o.customer_id,
        strftime('%Y-%m-01', o.order_date) AS order_month
    FROM fact_orders o
    WHERE o.order_status = 'Completed'
),

cohort_activity AS (
    -- Step 3: Compute the Cohort Index (months difference)
    SELECT 
        c.cohort_month,
        c.customer_id,
        o.order_month,
        -- Calculate month offset: (Order Year - Cohort Year)*12 + (Order Month - Cohort Month)
        (
            (CAST(strftime('%Y', o.order_month) AS INTEGER) - CAST(strftime('%Y', c.cohort_month) AS INTEGER)) * 12 +
            (CAST(strftime('%m', o.order_month) AS INTEGER) - CAST(strftime('%m', c.cohort_month) AS INTEGER))
        ) AS cohort_index
    FROM customer_first_purchase c
    JOIN customer_orders o ON c.customer_id = o.customer_id
),

cohort_summary AS (
    -- Step 4: Aggregate number of active customers per cohort per month index
    SELECT 
        cohort_month,
        cohort_index,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM cohort_activity
    GROUP BY cohort_month, cohort_index
),

cohort_sizes AS (
    -- Step 5: Cohort size at Month 0 (Base cohort size)
    SELECT 
        cohort_month,
        active_customers AS cohort_size
    FROM cohort_summary
    WHERE cohort_index = 0
)

-- Final Output: Cohort Retention Rates
SELECT 
    s.cohort_month,
    b.cohort_size,
    s.cohort_index,
    s.active_customers,
    ROUND((CAST(s.active_customers AS REAL) / b.cohort_size) * 100, 2) AS retention_rate_pct
FROM cohort_summary s
JOIN cohort_sizes b ON s.cohort_month = b.cohort_month
ORDER BY s.cohort_month, s.cohort_index;
