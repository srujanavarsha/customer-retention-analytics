"""
Generate Two Professional PDF Guides for Interview Preparation:
1. Data_Analyst_Interview_Cracker_Guide.pdf
2. Project_Explanation_and_Defense_Guide.pdf
Author: Antigravity Pair-Programming
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

PDF_INTERVIEW = os.path.join(DOCS_DIR, "Data_Analyst_Interview_Cracker_Guide.pdf")
PDF_PROJECT = os.path.join(DOCS_DIR, "Project_Explanation_and_Defense_Guide.pdf")

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=26,
    textColor=colors.HexColor('#0F172A'),
    spaceAfter=6
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=11,
    leading=15,
    textColor=colors.HexColor('#475569'),
    spaceAfter=15
)

h1_style = ParagraphStyle(
    'Heading1_Custom',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    textColor=colors.HexColor('#1E3A8A'),
    spaceBefore=14,
    spaceAfter=6
)

h2_style = ParagraphStyle(
    'Heading2_Custom',
    parent=styles['Heading3'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=14,
    textColor=colors.HexColor('#0F766E'),
    spaceBefore=8,
    spaceAfter=4
)

body_style = ParagraphStyle(
    'Body_Custom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor('#1E293B'),
    spaceAfter=6
)

code_style = ParagraphStyle(
    'Code_Custom',
    parent=styles['Code'],
    fontName='Courier',
    fontSize=8.5,
    leading=11,
    textColor=colors.HexColor('#0F172A'),
    backColor=colors.HexColor('#F1F5F9'),
    spaceAfter=6,
    leftIndent=8,
    rightIndent=8
)

callout_style = ParagraphStyle(
    'Callout_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor('#1E3A8A'),
    backColor=colors.HexColor('#EFF6FF'),
    spaceBefore=4,
    spaceAfter=8,
    leftIndent=8,
    rightIndent=8
)

# ==============================================================================
# PDF 1: DATA ANALYST INTERVIEW CRACKER GUIDE (DELOITTE, COGNIZANT, CAPGEMINI)
# ==============================================================================
def build_interview_guide():
    doc = SimpleDocTemplate(
        PDF_INTERVIEW,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    story = []

    # Header
    story.append(Paragraph("Data Analyst Fresher Interview Cheat Sheet", title_style))
    story.append(Paragraph("Target Companies: Deloitte, Cognizant, Capgemini | Core: SQL, Power BI, Python, Business Analytics", subtitle_style))
    story.append(Spacer(1, 8))

    # Section 1: Intro
    story.append(Paragraph("1. The 90-Second Winning Self-Introduction", h1_style))
    story.append(Paragraph(
        "<b>Script to memorize:</b><br/>"
        "<i>'Good morning/afternoon [Interviewer]. Thank you for this opportunity. I am Srujan, an aspiring Data Analyst with strong technical skills in <b>SQL, Python, and Power BI</b>.<br/>"
        "Recently, I designed and deployed an end-to-end <b>Customer Retention & Churn Risk Analytics Engine</b>. In that project, I designed a star-schema warehouse, wrote advanced SQL CTEs for cohort retention and RFM segmentation, built an automated AI sentiment pipeline in Python, and published an interactive executive cockpit in Power BI.<br/>"
        "I am eager to join [Deloitte / Cognizant / Capgemini] because of your high-impact analytics consulting practice, where I can apply my data modeling, problem-solving, and storytelling skills to deliver measurable business value.'</i>",
        callout_style
    ))

    # Section 2: SQL Must-Knows
    story.append(Paragraph("2. Top Core SQL Questions & Exact Answers", h1_style))
    
    story.append(Paragraph("Q1: WHERE vs HAVING", h2_style))
    story.append(Paragraph("• <b>WHERE:</b> Filters individual rows <i>before</i> any aggregation happens. Cannot contain aggregate functions (like SUM/AVG).<br/>"
                           "• <b>HAVING:</b> Filters grouped records <i>after</i> `GROUP BY` has executed.", body_style))
    story.append(Paragraph("SELECT department, AVG(salary) FROM employees WHERE status = 'Active' GROUP BY department HAVING AVG(salary) > 75000;", code_style))

    story.append(Paragraph("Q2: INNER JOIN vs LEFT JOIN", h2_style))
    story.append(Paragraph("• <b>INNER JOIN:</b> Returns only matching records from both tables.<br/>"
                           "• <b>LEFT JOIN:</b> Returns ALL records from the left table, plus matched rows from the right table. Non-matching right rows become NULL.<br/>"
                           "• <i>Interview Hook:</i> 'I use LEFT JOIN when identifying inactive records (e.g. `WHERE Orders.order_id IS NULL` to find customers who never bought).' ", body_style))

    story.append(Paragraph("Q3: RANK() vs DENSE_RANK() vs ROW_NUMBER()", h2_style))
    story.append(Paragraph("When ranking identical values (e.g., scores 90, 90, 80):<br/>"
                           "• <b>ROW_NUMBER():</b> Assigns strictly unique sequential numbers: <b>1, 2, 3</b>.<br/>"
                           "• <b>RANK():</b> Leaves gaps after ties: <b>1, 1, 3</b>.<br/>"
                           "• <b>DENSE_RANK():</b> Does NOT leave gaps: <b>1, 1, 2</b>.", body_style))

    story.append(Paragraph("Q4: Find the 2nd Highest Salary (2 Methods)", h2_style))
    story.append(Paragraph("<b>Method A (Subquery):</b><br/>"
                           "<code>SELECT MAX(salary) FROM employees WHERE salary &lt; (SELECT MAX(salary) FROM employees);</code><br/>"
                           "<b>Method B (Window Function):</b><br/>"
                           "<code>WITH Ranked AS (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as r FROM employees) SELECT DISTINCT salary FROM Ranked WHERE r = 2;</code>", body_style))

    story.append(Paragraph("Q5: Top 3 Spenders per Customer (Aggregates & Grouping)", h2_style))
    story.append(Paragraph("SELECT customer_id, SUM(amount) AS total_spent FROM Orders GROUP BY customer_id ORDER BY total_spent DESC LIMIT 3;", code_style))
    story.append(Paragraph("<i>Golden Rule:</i> Any non-aggregated column in `SELECT` must appear in the `GROUP BY` clause.", body_style))

    story.append(Paragraph("Q6: UNION vs UNION ALL", h2_style))
    story.append(Paragraph("• <b>UNION:</b> Merges datasets, removes duplicate rows, and sorts the output (slower).<br/>"
                           "• <b>UNION ALL:</b> Merges datasets while keeping all rows including duplicates (faster).", body_style))

    story.append(PageBreak())

    # Section 3: Power BI
    story.append(Paragraph("3. Top Power BI & DAX Essentials", h1_style))

    story.append(Paragraph("Q1: Calculated Column vs Measure (CRITICAL)", h2_style))
    data_calc = [
        [Paragraph("<b>Feature</b>", body_style), Paragraph("<b>Calculated Column</b>", body_style), Paragraph("<b>Measure</b>", body_style)],
        [Paragraph("<b>Evaluation</b>", body_style), Paragraph("Row-by-row during data refresh", body_style), Paragraph("Dynamically on-the-fly at query time", body_style)],
        [Paragraph("<b>Storage & RAM</b>", body_style), Paragraph("Stored permanently in RAM / file", body_style), Paragraph("Uses CPU memory on the fly (almost 0 RAM)", body_style)],
        [Paragraph("<b>Filter Context</b>", body_style), Paragraph("Static (does not respond to slicers)", body_style), Paragraph("Dynamic (changes when user clicks slicers)", body_style)],
        [Paragraph("<b>Best For</b>", body_style), Paragraph("Slicers, chart axes, row categorizations", body_style), Paragraph("KPI cards, aggregated numerical totals", body_style)]
    ]
    t_calc = Table(data_calc, colWidths=[100, 210, 210])
    t_calc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_calc)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Q2: Why Star Schema over Snowflake Schema in Power BI?", h2_style))
    story.append(Paragraph("• <b>Star Schema:</b> Fact table in the center directly connected to single-level dimension tables ($1:*$). Delivers faster DAX performance, uses simpler relationship paths, and optimizes Power BI's VertiPaq engine.<br/>"
                           "• <b>Snowflake Schema:</b> Dimension tables are normalized into sub-dimensions, requiring multiple table hops and slower joins.", body_style))

    story.append(Paragraph("Q3: What does the CALCULATE() function do in DAX?", h2_style))
    story.append(Paragraph("• `CALCULATE()` evaluates an expression while modifying, overriding, or adding new filter context. It is the most powerful function in DAX.", body_style))

    # Section 4: Python
    story.append(Paragraph("4. Python for Analytics Basics", h1_style))
    story.append(Paragraph("• <b>Handling Missing Data:</b> `df.isna().sum()` (detect), `df.dropna()` (drop), `df.fillna(value)` (impute with mean/median).<br/>"
                           "• <b>Merging Data:</b> `pd.merge(df1, df2, on='customer_id', how='left')`.<br/>"
                           "• <b>Aggregation:</b> `df.groupby('channel')['amount'].sum().reset_index()`.", body_style))

    # Section 5: Behavioral
    story.append(Paragraph("5. Behavioral & Closing Strategy (The STAR Method)", h1_style))
    story.append(Paragraph("When answering scenario questions (e.g. 'Tell me about a challenge with data'):<br/>"
                           "• <b>S (Situation):</b> Set the background in 1 sentence.<br/>"
                           "• <b>T (Task):</b> The goal you needed to achieve.<br/>"
                           "• <b>A (Action):</b> The specific technical action you took (SQL/Power BI/Python).<br/>"
                           "• <b>R (Result):</b> The measurable outcome (% improvement, time saved).", body_style))

    story.append(Paragraph("Smart Questions to Ask the Interviewer at the End:", h2_style))
    story.append(Paragraph("1. <i>'What does the typical analytics tech stack and data maturity look like on the engagements I would support?'</i><br/>"
                           "2. <i>'What qualities differentiate a good fresher analyst from a great one on your team?'</i>", body_style))

    doc.build(story)
    print(f"[SUCCESS] Built: {PDF_INTERVIEW}")


# ==============================================================================
# PDF 2: PROJECT EXPLANATION AND DEFENSE GUIDE
# ==============================================================================
def build_project_guide():
    doc = SimpleDocTemplate(
        PDF_PROJECT,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    story = []

    # Title
    story.append(Paragraph("Customer Retention & Churn Risk Analytics Engine", title_style))
    story.append(Paragraph("End-to-End Project Defense Guide | GitHub: github.com/srujanavarsha/customer-retention-analytics", subtitle_style))
    story.append(Spacer(1, 8))

    # Section 1: The 2-Minute Project Pitch
    story.append(Paragraph("1. The 2-Minute Perfect Project Pitch", h1_style))
    story.append(Paragraph(
        "<i>'In this project, I addressed a critical e-commerce retention problem: top-of-funnel customer acquisition was growing 18% YoY, but net revenue remained flat due to hidden churn.<br/><br/>"
        "To solve this, I designed an end-to-end analytics engine across 1,200 accounts and 5,100+ orders:<br/>"
        "1. <b>Data Modeling:</b> Implemented a clean Star Schema in SQLite with a central Fact Orders table and dimension tables.<br/>"
        "2. <b>Advanced SQL:</b> Wrote modular CTEs for monthly cohort retention curves, NTILE-based RFM segmentation, and LAG window functions to detect repurchase cadence anomalies.<br/>"
        "3. <b>AI Sentiment Layer:</b> Used a Python NLP script to classify 2,200 unstructured customer reviews into sentiment scores and operational churn categories.<br/>"
        "4. <b>Power BI Cockpit:</b> Built an executive dashboard with time-intelligence DAX measures and semantic color alerts.<br/><br/>"
        "<b>The Key Business Result:</b> We discovered an 81.5% drop-off in Month 1, flagged 276 high-value accounts at risk ($180K revenue exposure), and proved that hardware defects in Electronics drove 52% of negative reviews.'</i>",
        callout_style
    ))

    # Section 2: Architecture & Star Schema
    story.append(Paragraph("2. Data Architecture & Schema Breakdown", h1_style))
    story.append(Paragraph("You modeled the data using a strict <b>Star Schema</b> to avoid bidirectional joins and optimize query speed:", body_style))
    
    schema_data = [
        [Paragraph("<b>Table</b>", body_style), Paragraph("<b>Type</b>", body_style), Paragraph("<b>Key Columns & Purpose</b>", body_style)],
        [Paragraph("`fact_orders`", body_style), Paragraph("Central Fact", body_style), Paragraph("5,147 rows. Grain: 1 row per order line. Contains `total_amount`, `order_date`, `status`.", body_style)],
        [Paragraph("`dim_customers`", body_style), Paragraph("Dimension (1:*)", body_style), Paragraph("1,200 profiles. `customer_id` (PK), `acquisition_channel`, `country`, `customer_type`.", body_style)],
        [Paragraph("`dim_products`", body_style), Paragraph("Dimension (1:*)", body_style), Paragraph("22 product items. `product_id` (PK), `category`, `unit_price`, `unit_cost`.", body_style)],
        [Paragraph("`dim_calendar`", body_style), Paragraph("Dimension (1:*)", body_style), Paragraph("Created via DAX (`ADDCOLUMNS(CALENDAR(...))`) for time-intelligence filtering.", body_style)],
        [Paragraph("`customer_feedback_enriched`", body_style), Paragraph("Secondary Fact", body_style), Paragraph("2,200 reviews enriched with `sentiment` and `churn_driver_category`.", body_style)]
    ]
    t_schema = Table(schema_data, colWidths=[120, 90, 310])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 10))

    # Section 3: The 3 SQL Queries
    story.append(Paragraph("3. The 3 Technical SQL Queries in Your Portfolio", h1_style))
    story.append(Paragraph("<b>1. Monthly Cohort Decay Matrix (`01_cohort_retention_matrix.sql`):</b><br/>"
                           "• Uses CTEs to compute customer's first purchase month (`MIN(order_date)`).<br/>"
                           "• Calculates `cohort_index` = elapsed calendar months since Month 0.<br/>"
                           "• Divides returning active buyers by Month 0 cohort size to derive retention %.", body_style))

    story.append(Paragraph("<b>2. RFM Customer Segmentation (`02_rfm_customer_segmentation.sql`):</b><br/>"
                           "• Computes Recency (days since last order), Frequency (order count), and Monetary (spend).<br/>"
                           "• Applies `NTILE(4) OVER (...)` across all 3 dimensions to classify users into: <i>Champions, Loyal, Needs Nurturing, At Risk, and Lost</i>.", body_style))

    story.append(Paragraph("<b>3. Repurchase Cadence Churn Detection (`03_churn_risk_detection.sql`):</b><br/>"
                           "• Uses `LAG(order_date, 1) OVER (PARTITION BY customer_id ORDER BY order_date)` to calculate each customer's personal average order cycle.<br/>"
                           "• If days since last order exceeds <b>2.5x their historical average</b>, SQL flags a <i>Critical Churn Alert</i>.", body_style))

    story.append(PageBreak())

    # Section 4: Power BI & AI
    story.append(Paragraph("4. The Power BI Executive Dashboard & DAX Measures", h1_style))
    story.append(Paragraph("• <b>[Total Net Revenue]:</b> `CALCULATE(SUM(fact_orders[total_amount]), fact_orders[order_status] = 'Completed')`<br/>"
                           "• <b>[Completed Orders]:</b> `CALCULATE(DISTINCTCOUNT(fact_orders[order_id]), fact_orders[order_status] = 'Completed')`<br/>"
                           "• <b>[Active Customers (Last 90 Days)]:</b> Uses `DATESBETWEEN` on the date dimension to track active accounts.<br/>"
                           "• <b>Visual Design Philosophy:</b> Used card-on-canvas containers, rounded corners (8px), data labels on horizontal bars, and semantic color alerting (Red for hardware defects, Green for positive praise).", body_style))

    # Section 5: Top 5 Tough Interview Questions on this Project
    story.append(Paragraph("5. Top 5 Tough Follow-Up Questions (And How to Answer Them)", h1_style))

    story.append(Paragraph("Q1: 'Why did you use a Star Schema instead of one big flat CSV table?'", h2_style))
    story.append(Paragraph("<b>Answer:</b> <i>'A flat denormalized table creates data redundancy, increases file size, and slows down DAX measures. A Star Schema ensures a clean 1-to-many relationship, optimizes Power BI's columnar engine, and makes time intelligence seamless.'</i>", body_style))

    story.append(Paragraph("Q2: 'Why did you evaluate Churn using personal repurchase cadence instead of a fixed 90-day rule?'", h2_style))
    story.append(Paragraph("<b>Answer:</b> <i>'Static thresholds fail because buying behaviors differ. A loyal customer who usually orders every 10 days has likely churned if 40 days pass, while a seasonal buyer ordering every 180 days is completely normal. Personalized cadence anomaly detection with LAG() is industry best practice.'</i>", body_style))

    story.append(Paragraph("Q3: 'How did you classify unstructured reviews into churn categories?'", h2_style))
    story.append(Paragraph("<b>Answer:</b> <i>'I built a Python script that processed 2,200 qualitative comments against an operational taxonomy covering Shipping, Defects, Support, and Billing, generating sentiment scores and category tags which were fed directly into Power BI.'</i>", body_style))

    story.append(Paragraph("Q4: 'What was the single most actionable business recommendation you made?'", h2_style))
    story.append(Paragraph("<b>Answer:</b> <i>'Because Month 1 drop-off was 81.5%, we recommended an automated 30-day second-purchase incentive for new buyers, as our data proved that customers who place a second order within 45 days generate 4.2x higher 12-month LTV ($820 vs $195).'</i>", body_style))

    story.append(Paragraph("Q5: 'What would you do differently if the dataset was 100 million rows?'", h2_style))
    story.append(Paragraph("<b>Answer:</b> <i>'I would migrate from SQLite to an enterprise data warehouse like Snowflake or BigQuery, use dbt for data transformation models, and configure Power BI in DirectQuery or Composite Mode with aggregations.'</i>", body_style))

    doc.build(story)
    print(f"[SUCCESS] Built: {PDF_PROJECT}")

if __name__ == "__main__":
    build_interview_guide()
    build_project_guide()
