# Customer Consumption & Trend Analysis

A end-to-end data analysis project exploring customer behaviour, revenue trends, 
and consumption anomalies using a real-world retail dataset. Built using Python 
for analysis and segmentation, with outputs prepared for Power BI dashboarding.

---

## Project Overview

This project analyses transactional retail data to answer three core business questions:
- Which customer segments drive the most revenue?
- Where are the anomalies in daily consumption patterns?
- How does revenue trend across time, geography, and product categories?

The workflow covers data cleaning, exploratory analysis, RFM customer segmentation, 
anomaly detection, and KPI reporting — producing clean datasets ready for BI dashboarding.

---

## Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python (Pandas, NumPy) | Data cleaning, transformation, EDA |
| Matplotlib / Seaborn | Exploratory visualisations |
| Scikit-learn | Z-score anomaly detection |
| Power BI | Interactive dashboard (in progress) |
| Google Colab | Development environment |
| GitHub | Version control and portfolio hosting |

---

## Dataset

**Source:** UCI Machine Learning Repository — Online Retail II  
**Records:** 1M+ transactions across 2009–2011  
**Coverage:** UK-based online retailer with international customers  
**Link:** https://archive.ics.uci.edu/dataset/502/online+retail+ii

---

## Workflow

### 1. Data Cleaning
- Removed ~20% of records: missing Customer IDs, cancellations, zero-price and negative quantity rows
- Engineered date features: year, month, quarter, day of week, hour
- Created revenue column (Quantity × Price)
- Exported clean dataset for downstream use

### 2. KPI Summary
| KPI | Value |
|-----|-------|
| Total Revenue | calculated in notebook |
| Total Orders | calculated in notebook |
| Unique Customers | calculated in notebook |
| Avg Order Value | calculated in notebook |
| Avg Revenue per Customer | calculated in notebook |

> Update the table above with your actual output values from Cell 5

### 3. Revenue Trend Analysis
Analysed revenue across monthly, daily, quarterly, and geographic dimensions 
to identify seasonality patterns and key market concentrations.

![Revenue Trends](revenue_trends.png)

### 4. RFM Customer Segmentation
Segmented customers using Recency, Frequency, and Monetary scoring — 
a standard CRM and marketing analytics technique for identifying 
high-value customers and churn risk.

| Segment | Description |
|---------|-------------|
| Champions | Bought recently, buy often, spend the most |
| Loyal Customers | Regular buyers with strong spend |
| Potential Loyalists | Recent customers with growing frequency |
| At Risk | Previously good customers going quiet |
| Lost Customers | Haven't purchased in a long time |

![RFM Segmentation](rfm_segmentation.png)

### 5. Anomaly Detection
Applied z-score methodology to flag days where revenue deviated 
significantly from the mean — useful for identifying campaign spikes, 
data quality issues, or unexpected demand shifts.

![Anomaly Detection](anomaly_detection.png)

---

## Files in This Repository

| File | Description |
|------|-------------|
| `customer_analysis.py` | Full analysis script |
| `cleaned_retail_data.csv` | Cleaned transaction dataset |
| `rfm_segments.csv` | RFM scores and customer segments |
| `daily_revenue_anomalies.csv` | Daily revenue with anomaly flags |
| `revenue_trends.png` | Revenue trend visualisations |
| `rfm_segmentation.png` | RFM segment charts |
| `anomaly_detection.png` | Anomaly detection chart |

---

## Key Findings

- **[Fill in once you've reviewed your Cell 5 and Cell 9 outputs]**
- e.g. Champions segment (X% of customers) generated Y% of total revenue
- e.g. November 2011 showed the highest anomalous revenue spike — likely seasonal demand
- e.g. Thursday and Tuesday were the strongest revenue days

---

## Author

**Deepika Dhanola**  
BI & Data Analyst | PL-300 & DP-900 Certified  
[LinkedIn](https://www.linkedin.com/in/deepika-dhanola/) · deepikadhanola27@gmail.com
