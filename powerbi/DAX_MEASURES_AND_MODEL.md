# Power BI Data Model & DAX Measures Guide
**Project:** Enterprise Customer Retention & Churn Driver Engine  
**Author:** Corporate Analytics Architecture  

---

## 1. Data Model Architecture (Star Schema)

In corporate Power BI development, avoiding bidirectional relationships and flat denormalized tables is crucial for performance and measure integrity.

### Tables & Relationships:
1. **`fact_orders`** (Central Fact Table)
   - `order_id` (Grain: Order line item)
   - `customer_id` $\rightarrow$ relates to `dim_customers[customer_id]` (Many-to-One `*:1`, Single direction)
   - `product_id` $\rightarrow$ relates to `dim_products[product_id]` (Many-to-One `*:1`, Single direction)
   - `order_date` $\rightarrow$ relates to `dim_calendar[Date]` (Many-to-One `*:1`, Single direction)

2. **`customer_feedback_enriched`** (Secondary Fact / Dimension)
   - `order_id` $\rightarrow$ relates to `fact_orders[order_id]` (Many-to-One `*:1`, Single direction)
   - `customer_id` $\rightarrow$ relates to `dim_customers[customer_id]` (Inactive relationship, activated via `USERELATIONSHIP`)

3. **`dim_calendar`** (Date Dimension - Recommended DAX generation):
```dax
dim_calendar = 
VAR MinDate = MIN(fact_orders[order_date])
VAR MaxDate = MAX(fact_orders[order_date])
RETURN
ADDCOLUMNS(
    CALENDAR(MinDate, MaxDate),
    "Year", YEAR([Date]),
    "YearMonth", FORMAT([Date], "YYYY-MM"),
    "MonthName", FORMAT([Date], "MMM"),
    "MonthNumber", MONTH([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q")
)
```

---

## 2. Production DAX Measures Dictionary

Create a dedicated blank table named **`_Measures`** to keep your measures organized in folders.

### Folder: `01 - Financial & Core KPIs`

#### [Total Net Revenue]
```dax
Total Net Revenue = 
CALCULATE(
    SUM(fact_orders[total_amount]),
    fact_orders[order_status] = "Completed"
)
```

#### [Completed Orders]
```dax
Completed Orders = 
CALCULATE(
    DISTINCTCOUNT(fact_orders[order_id]),
    fact_orders[order_status] = "Completed"
)
```

#### [Average Order Value (AOV)]
```dax
Average Order Value = 
DIVIDE([Total Net Revenue], [Completed Orders], 0)
```

#### [Gross Margin %]
```dax
Gross Margin % = 
VAR TotalRevenue = [Total Net Revenue]
VAR TotalCost = 
    CALCULATE(
        SUMX(
            fact_orders,
            fact_orders[quantity] * RELATED(dim_products[unit_cost])
        ),
        fact_orders[order_status] = "Completed"
    )
RETURN
DIVIDE(TotalRevenue - TotalCost, TotalRevenue, 0)
```

---

### Folder: `02 - Retention & Churn Dynamics`

#### [Active Customers (Total)]
```dax
Active Customers = 
CALCULATE(
    DISTINCTCOUNT(fact_orders[customer_id]),
    fact_orders[order_status] = "Completed"
)
```

#### [Active Customers (Last 90 Days)]
```dax
Active Customers (Last 90 Days) = 
VAR SnapshotDate = MAX(dim_calendar[Date])
RETURN
CALCULATE(
    DISTINCTCOUNT(fact_orders[customer_id]),
    fact_orders[order_status] = "Completed",
    DATESBETWEEN(dim_calendar[Date], SnapshotDate - 90, SnapshotDate)
)
```

#### [Dormant / Churned Customers (>180 Days Inactive)]
```dax
Churned Customers = 
VAR SnapshotDate = MAX(dim_calendar[Date])
VAR ActivePast180 = 
    CALCULATETABLE(
        VALUES(fact_orders[customer_id]),
        fact_orders[order_status] = "Completed",
        DATESBETWEEN(dim_calendar[Date], SnapshotDate - 180, SnapshotDate)
    )
VAR AllHistoricalCustomers = 
    CALCULATETABLE(
        VALUES(fact_orders[customer_id]),
        fact_orders[order_status] = "Completed",
        dim_calendar[Date] < SnapshotDate - 180
    )
RETURN
COUNTROWS(EXCEPT(AllHistoricalCustomers, ActivePast180))
```

#### [Revenue at Risk (At-Risk RFM Segment)]
```dax
Revenue at Risk = 
CALCULATE(
    [Total Net Revenue],
    FILTER(
        VALUES(dim_customers[customer_id]),
        -- Evaluates spend from users in high-risk categories
        [Active Customers (Last 90 Days)] = 0
    )
)
```

---

### Folder: `03 - Cohort Retention Matrix`

#### [Cohort Size (Month 0)]
```dax
Cohort Base Size = 
VAR FirstOrderDate = 
    CALCULATE(
        MIN(fact_orders[order_date]),
        ALLEXCEPT(fact_orders, fact_orders[customer_id])
    )
RETURN
CALCULATE(
    DISTINCTCOUNT(fact_orders[customer_id]),
    ALLSELECTED(dim_calendar),
    fact_orders[order_status] = "Completed"
)
```

#### [Cohort Retention Rate %]
```dax
Cohort Retention % = 
DIVIDE(
    [Active Customers],
    [Cohort Base Size],
    0
)
```

---

### Folder: `04 - AI Sentiment & Churn Drivers`

#### [Negative Feedback Rate %]
```dax
Negative Feedback Rate % = 
VAR NegativeReviews = 
    CALCULATE(
        COUNTROWS(customer_feedback_enriched),
        customer_feedback_enriched[sentiment] = "Negative"
    )
VAR TotalReviews = COUNTROWS(customer_feedback_enriched)
RETURN
DIVIDE(NegativeReviews, TotalReviews, 0)
```

#### [Net Sentiment Score]
```dax
Net Sentiment Score = 
VAR Pos = CALCULATE(COUNTROWS(customer_feedback_enriched), customer_feedback_enriched[sentiment] = "Positive")
VAR Neg = CALCULATE(COUNTROWS(customer_feedback_enriched), customer_feedback_enriched[sentiment] = "Negative")
VAR Total = COUNTROWS(customer_feedback_enriched)
RETURN
DIVIDE(Pos - Neg, Total, 0)
```

---

## 3. Recommended 3-Page Executive Dashboard Layout

### Page 1: Executive Retention & Financial Health
* **Header Cards:** Total Net Revenue, Active Customer Count, 90-Day Churn Rate, Gross Margin %.
* **Visual 1 (Area Chart):** Monthly Revenue with Prior Year Pacing.
* **Visual 2 (Bar Chart):** Revenue by Customer Segment (Champions vs. At Risk vs. New).
* **Visual 3 (Donut Chart):** Customer Acquisition Channel ROI.

### Page 2: Cohort Retention Heatmap
* **Matrix Visual:**
  * Rows: `Cohort Month` (e.g. 2024-01, 2024-02...)
  * Columns: `Cohort Index (Months Elapsed: 0, 1, 2, ... 12)`
  * Values: `[Cohort Retention %]`
  * Conditional Formatting: Gradient color scale (Green for high retention, White for 0%).

### Page 3: Voice-of-Customer & AI Churn Driver Matrix
* **Visual 1 (Treemap / Bar Chart):** Feedback count by `churn_driver_category` (Product Defects vs. Shipping vs. Support).
* **Visual 2 (Scatter Plot):** X-axis = `Negative Feedback Rate %`, Y-axis = `Total Net Revenue`, Size = `Order Volume` (Bubble per Product Category).
* **Visual 3 (Drill-through Table):** Review details (`review_text`, `customer_id`, `rating`, `order_status`) with interactive slicer on `churn_driver_category`.
