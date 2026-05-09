# ── Cell 1 ──────────────────────────────────────────────────────────────────
!pip install openpyxl pandas numpy matplotlib seaborn scikit-learn --quiet

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)

print("All libraries loaded successfully")


# ── Cell 2 ──────────────────────────────────────────────────────────────────
# two sheets in the file, combining them into one
df_09 = pd.read_excel('online_retail_II.xlsx', sheet_name='Year 2009-2010')
df_10 = pd.read_excel('online_retail_II.xlsx', sheet_name='Year 2010-2011')

df = pd.concat([df_09, df_10], ignore_index=True)

print(f"Total records loaded: {len(df):,}")
print(f"Columns: {list(df.columns)}")
print(f"\nDate range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
df.head()


# ── Cell 3 ──────────────────────────────────────────────────────────────────
# quick look at the data before touching anything
print("=== DATASET SHAPE ===")
print(f"Rows: {len(df):,} | Columns: {df.shape[1]}")

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== MISSING VALUES ===")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
print(missing_df[missing_df['Missing Count'] > 0])

print("\n=== BASIC STATISTICS ===")
print(df.describe())

# flagging the obvious issues upfront
print("\n=== SAMPLE OF PROBLEM RECORDS ===")
print(f"Cancelled orders (negative qty): {len(df[df['Quantity'] < 0]):,}")
print(f"Zero price records: {len(df[df['Price'] == 0]):,}")
print(f"Missing Customer ID: {df['Customer ID'].isnull().sum():,}")


# ── Cell 4 ──────────────────────────────────────────────────────────────────
print("=== CLEANING START ===")
print(f"Records before cleaning: {len(df):,}")

# can't do customer-level analysis without an ID
df_clean = df.dropna(subset=['Customer ID'])
print(f"After removing missing Customer IDs: {len(df_clean):,}")

# invoices starting with C are cancellations
df_clean = df_clean[~df_clean['Invoice'].astype(str).str.startswith('C')]
print(f"After removing cancellations: {len(df_clean):,}")

# negative and zero quantities are returns or bad data
df_clean = df_clean[df_clean['Quantity'] > 0]
print(f"After removing negative/zero quantities: {len(df_clean):,}")

# zero price rows are likely data entry errors
df_clean = df_clean[df_clean['Price'] > 0]
print(f"After removing zero price items: {len(df_clean):,}")

# derived columns for analysis
df_clean['Revenue'] = df_clean['Quantity'] * df_clean['Price']

df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
df_clean['Year'] = df_clean['InvoiceDate'].dt.year
df_clean['Month'] = df_clean['InvoiceDate'].dt.month
df_clean['MonthName'] = df_clean['InvoiceDate'].dt.strftime('%b')
df_clean['Quarter'] = df_clean['InvoiceDate'].dt.quarter
df_clean['DayOfWeek'] = df_clean['InvoiceDate'].dt.day_name()
df_clean['Hour'] = df_clean['InvoiceDate'].dt.hour

df_clean['Customer ID'] = df_clean['Customer ID'].astype(int).astype(str)

print(f"\nRecords after cleaning: {len(df_clean):,}")
print(f"Records removed: {len(df) - len(df_clean):,} ({((len(df) - len(df_clean))/len(df)*100):.1f}%)")
print("\nCleaning complete ✓")


# ── Cell 5 ──────────────────────────────────────────────────────────────────
# top-level numbers before diving into segmentation
print("=== BUSINESS KPI SUMMARY ===\n")

total_revenue = df_clean['Revenue'].sum()
total_orders = df_clean['Invoice'].nunique()
total_customers = df_clean['Customer ID'].nunique()
total_products = df_clean['StockCode'].nunique()
avg_order_value = total_revenue / total_orders
avg_revenue_per_customer = total_revenue / total_customers

kpis = {
    'Total Revenue': f"£{total_revenue:,.2f}",
    'Total Orders': f"{total_orders:,}",
    'Unique Customers': f"{total_customers:,}",
    'Unique Products': f"{total_products:,}",
    'Avg Order Value': f"£{avg_order_value:,.2f}",
    'Avg Revenue per Customer': f"£{avg_revenue_per_customer:,.2f}"
}

for k, v in kpis.items():
    print(f"  {k:<30} {v}")


# ── Cell 6 ──────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Customer Consumption & Revenue Trends', fontsize=16, fontweight='bold', y=1.01)

# monthly trend — good for spotting seasonality
monthly_revenue = df_clean.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()
monthly_revenue['Period'] = monthly_revenue['Year'].astype(str) + '-' + monthly_revenue['Month'].astype(str).str.zfill(2)
monthly_revenue = monthly_revenue.sort_values('Period')

axes[0,0].plot(monthly_revenue['Period'], monthly_revenue['Revenue'],
               marker='o', linewidth=2, color='#1D6A72', markersize=4)
axes[0,0].fill_between(range(len(monthly_revenue)), monthly_revenue['Revenue'],
                        alpha=0.15, color='#1D6A72')
axes[0,0].set_title('Monthly Revenue Trend', fontweight='bold')
axes[0,0].set_xlabel('Period')
axes[0,0].set_ylabel('Revenue (£)')
axes[0,0].tick_params(axis='x', rotation=45)
axes[0,0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:,.0f}'))

# which days drive the most sales
dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
dow_revenue = df_clean.groupby('DayOfWeek')['Revenue'].sum().reindex(dow_order)

axes[0,1].bar(dow_revenue.index, dow_revenue.values, color='#4A90C4', alpha=0.85, edgecolor='white')
axes[0,1].set_title('Revenue by Day of Week', fontweight='bold')
axes[0,1].set_xlabel('Day')
axes[0,1].set_ylabel('Revenue (£)')
axes[0,1].tick_params(axis='x', rotation=45)
axes[0,1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:,.0f}'))

# UK dominates but good to see the international spread
country_revenue = df_clean.groupby('Country')['Revenue'].sum().sort_values(ascending=True).tail(10)
axes[1,0].barh(country_revenue.index, country_revenue.values, color='#E8834A', alpha=0.85, edgecolor='white')
axes[1,0].set_title('Top 10 Countries by Revenue', fontweight='bold')
axes[1,0].set_xlabel('Revenue (£)')
axes[1,0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:,.0f}'))

# quarterly view for exec-level reporting
quarterly = df_clean.groupby(['Year','Quarter'])['Revenue'].sum().reset_index()
quarterly['Label'] = 'Q' + quarterly['Quarter'].astype(str) + ' ' + quarterly['Year'].astype(str)
axes[1,1].bar(quarterly['Label'], quarterly['Revenue'], color='#7B5EA7', alpha=0.85, edgecolor='white')
axes[1,1].set_title('Revenue by Quarter', fontweight='bold')
axes[1,1].set_xlabel('Quarter')
axes[1,1].set_ylabel('Revenue (£)')
axes[1,1].tick_params(axis='x', rotation=45)
axes[1,1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:,.0f}'))

plt.tight_layout()
plt.savefig('revenue_trends.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved as revenue_trends.png")


# ── Cell 7 ──────────────────────────────────────────────────────────────────
# RFM — standard segmentation approach, scores customers on recency, frequency, spend

snapshot_date = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df_clean.groupby('Customer ID').agg(
    Recency   = ('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
    Frequency = ('Invoice', 'nunique'),
    Monetary  = ('Revenue', 'sum')
).reset_index()

# score 1-5, higher is better across all three dimensions
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1,2,3,4,5])

rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
rfm['Total_Score'] = rfm['R_Score'].astype(int) + rfm['F_Score'].astype(int) + rfm['M_Score'].astype(int)

def segment_customer(score):
    if score >= 13:
        return 'Champions'
    elif score >= 10:
        return 'Loyal Customers'
    elif score >= 7:
        return 'Potential Loyalists'
    elif score >= 5:
        return 'At Risk'
    else:
        return 'Lost Customers'

rfm['Segment'] = rfm['Total_Score'].apply(segment_customer)

print("=== RFM SEGMENTATION RESULTS ===\n")
segment_summary = rfm.groupby('Segment').agg(
    Customer_Count = ('Customer ID', 'count'),
    Avg_Recency    = ('Recency', 'mean'),
    Avg_Frequency  = ('Frequency', 'mean'),
    Avg_Monetary   = ('Monetary', 'mean'),
    Total_Revenue  = ('Monetary', 'sum')
).round(2)
print(segment_summary)

# export for Power BI
rfm.to_csv('rfm_segments.csv', index=False)
df_clean.to_csv('cleaned_retail_data.csv', index=False)
print("\nFiles saved for Power BI import ✓")


# ── Cell 8 ──────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('RFM Customer Segmentation Analysis', fontsize=14, fontweight='bold')

segment_colours = {
    'Champions': '#1D9E75',
    'Loyal Customers': '#4A90C4',
    'Potential Loyalists': '#7B5EA7',
    'At Risk': '#EF9F27',
    'Lost Customers': '#D85A30'
}

# how many customers in each bucket
seg_counts = rfm['Segment'].value_counts()
colours = [segment_colours[s] for s in seg_counts.index]
axes[0].bar(seg_counts.index, seg_counts.values, color=colours, edgecolor='white', alpha=0.9)
axes[0].set_title('Customers per Segment', fontweight='bold')
axes[0].set_ylabel('Number of Customers')
axes[0].tick_params(axis='x', rotation=30)

# revenue contribution by segment — champions usually drive the bulk of it
seg_revenue = rfm.groupby('Segment')['Monetary'].sum().reindex(seg_counts.index)
colours2 = [segment_colours[s] for s in seg_revenue.index]
axes[1].bar(seg_revenue.index, seg_revenue.values, color=colours2, edgecolor='white', alpha=0.9)
axes[1].set_title('Total Revenue by Segment', fontweight='bold')
axes[1].set_ylabel('Revenue (£)')
axes[1].tick_params(axis='x', rotation=30)
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:,.0f}'))

# scatter helps visualise the recency vs spend relationship
scatter_colours = [segment_colours[s] for s in rfm['Segment']]
scatter = axes[2].scatter(rfm['Recency'], rfm['Monetary'],
                          c=scatter_colours, alpha=0.4, s=15)
axes[2].set_title('Recency vs Revenue (by Segment)', fontweight='bold')
axes[2].set_xlabel('Recency (days since last purchase)')
axes[2].set_ylabel('Total Revenue (£)')

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=v, label=k) for k, v in segment_colours.items()]
axes[2].legend(handles=legend_elements, loc='upper right', fontsize=8)

plt.tight_layout()
plt.savefig('rfm_segmentation.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved as rfm_segmentation.png")


# ── Cell 9 ──────────────────────────────────────────────────────────────────
# flag days where revenue was unusually high or low using z-score
print("=== CONSUMPTION ANOMALY DETECTION ===\n")

daily_revenue = df_clean.groupby(df_clean['InvoiceDate'].dt.date)['Revenue'].sum().reset_index()
daily_revenue.columns = ['Date', 'Revenue']

mean_rev = daily_revenue['Revenue'].mean()
std_rev  = daily_revenue['Revenue'].std()
daily_revenue['Z_Score'] = (daily_revenue['Revenue'] - mean_rev) / std_rev

# anything beyond 2 std deviations is worth investigating
daily_revenue['Anomaly'] = daily_revenue['Z_Score'].abs() > 2

anomalies = daily_revenue[daily_revenue['Anomaly']]
print(f"Mean daily revenue: £{mean_rev:,.2f}")
print(f"Std deviation: £{std_rev:,.2f}")
print(f"\nAnomalous days detected: {len(anomalies)}")
print("\nTop anomalous days:")
print(anomalies.sort_values('Z_Score', ascending=False).head(10).to_string(index=False))

plt.figure(figsize=(16, 6))
plt.plot(daily_revenue['Date'], daily_revenue['Revenue'],
         color='#1D6A72', linewidth=1, alpha=0.7, label='Daily Revenue')
plt.scatter(anomalies['Date'], anomalies['Revenue'],
            color='#D85A30', s=60, zorder=5, label='Anomaly', alpha=0.9)
plt.axhline(y=mean_rev + 2*std_rev, color='orange', linestyle='--', alpha=0.6, label='+2 Std Dev')
plt.axhline(y=mean_rev - 2*std_rev, color='orange', linestyle='--', alpha=0.6, label='-2 Std Dev')
plt.title('Daily Revenue with Anomaly Detection', fontweight='bold', fontsize=13)
plt.xlabel('Date')
plt.ylabel('Revenue (£)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('anomaly_detection.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved ✓")

daily_revenue.to_csv('daily_revenue_anomalies.csv', index=False)


# ── Cell 10 ─────────────────────────────────────────────────────────────────
print("=" * 55)
print("   PROJECT COMPLETE — FILES READY FOR POWER BI")
print("=" * 55)

files = {
    'cleaned_retail_data.csv':      'Main cleaned transaction dataset',
    'rfm_segments.csv':             'Customer RFM scores and segments',
    'daily_revenue_anomalies.csv':  'Daily revenue with anomaly flags',
    'revenue_trends.png':           'Revenue trend charts',
    'rfm_segmentation.png':         'RFM segmentation charts',
    'anomaly_detection.png':        'Anomaly detection chart'
}

for f, desc in files.items():
    print(f"  ✓  {f:<38} {desc}")

print("\nNext step: Download all CSV files and import into Power BI")
