# ============================================
# AI-ASSISTED SALES INSIGHTS AUTOMATION
# Automatically generates executive insights from sales data
# Version 1.0
# Author: Deepak Pandey
# ============================================

# Import required libraries
import pandas as pd
from datetime import datetime
import os

# ============================================
# STEP 1: LOAD DATA
# ============================================

print("🔄 Loading sales data...")

# Load the CSV file
try:
    df = pd.read_csv('data/SuperStore_Orders.csv', encoding='latin-1')
    df.columns = [c.replace('_', ' ').title() for c in df.columns]
    df = df.rename(columns={'Sub Category': 'Sub-Category'})
    print(f"✅ Successfully loaded {len(df):,} records")
except FileNotFoundError:
    print("❌ Error: File 'data/SuperStore_Orders.csv' not found!")
    print("Please make sure the CSV file is in the 'data' folder.")
    exit()

# Convert date columns to datetime format
df['Sales'] = pd.to_numeric(df['Sales'].astype(str).str.replace(',', ''), errors='coerce')
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')

# Remove any rows with invalid dates
df = df.dropna(subset=['Order Date'])
print(f"✅ Data cleaned: {len(df):,} valid records after date conversion")

# ============================================
# STEP 2: CALCULATE KEY METRICS
# ============================================

print("\n📊 Calculating business metrics...")

# Overall Performance
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order Id'].nunique()
profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

print(f"   • Total Sales: ${total_sales:,.2f}")
print(f"   • Total Profit: ${total_profit:,.2f}")
print(f"   • Profit Margin: {profit_margin:.1f}%")

# ============================================
# STEP 3: GENERATE AUTOMATED INSIGHTS
# ============================================

print("\n🔍 Generating insights...")

# Create empty list to store insights
insights = []

# --- INSIGHT 1: Overall Performance ---
insights.append({
    'category': '📊 Overall Performance',
    'text': f"${total_sales:,.0f} revenue, ${total_profit:,.0f} profit ({profit_margin:.1f}% margin) across {total_orders:,} orders"
})

# --- INSIGHT 2: Best Category by Profit ---
category_profit = df.groupby('Category')['Profit'].sum()
best_category = category_profit.idxmax()
best_category_profit = category_profit.max()
worst_category = category_profit.idxmin()
worst_category_profit = category_profit.min()

insights.append({
    'category': '🏆 Category Performance',
    'text': f"{best_category} leads with ${best_category_profit:,.0f} profit; {worst_category} lowest at ${worst_category_profit:,.0f}"
})

# --- INSIGHT 3: Best Region ---
region_profit = df.groupby('Region')['Profit'].sum()
best_region = region_profit.idxmax()
best_region_profit = region_profit.max()
worst_region = region_profit.idxmin()
worst_region_profit = region_profit.min()

insights.append({
    'category': '🌍 Regional Performance',
    'text': f"{best_region} tops with ${best_region_profit:,.0f} profit; {worst_region} at ${worst_region_profit:,.0f}"
})

# --- INSIGHT 4: Discount Impact Analysis ---
# Segment orders by discount level
no_discount = df[df['Discount'] == 0]
low_discount = df[(df['Discount'] > 0) & (df['Discount'] < 0.2)]
medium_discount = df[(df['Discount'] >= 0.2) & (df['Discount'] < 0.4)]
high_discount = df[df['Discount'] >= 0.4]

# Calculate average profit for each segment
no_discount_avg = no_discount['Profit'].mean() if len(no_discount) > 0 else 0
high_discount_avg = high_discount['Profit'].mean() if len(high_discount) > 0 else 0

# Calculate impact percentage
if no_discount_avg != 0:
    discount_impact = ((high_discount_avg - no_discount_avg) / abs(no_discount_avg)) * 100
else:
    discount_impact = 0

insights.append({
    'category': '💰 Discount Impact',
            'text': f"Order lines with ≥40% discount average {'-' if high_discount_avg < 0 else ''}${abs(high_discount_avg):,.2f} profit vs {'-' if no_discount_avg < 0 else ''}${abs(no_discount_avg):,.2f} with no discount"
})

# --- INSIGHT 5: Year-over-Year Growth ---
yoy_sales = df.groupby(df['Order Date'].dt.year)['Sales'].sum()

if len(yoy_sales) >= 2:
    latest_year = yoy_sales.index[-1]
    previous_year = yoy_sales.index[-2]
    latest_sales = yoy_sales.iloc[-1]
    previous_sales = yoy_sales.iloc[-2]
    yoy_growth = ((latest_sales - previous_sales) / previous_sales) * 100
    
    insights.append({
        'category': '📈 Year-over-Year Growth',
        'text': f"{yoy_growth:.1f}% growth from {previous_year} (${previous_sales:,.0f}) to {latest_year} (${latest_sales:,.0f})"
    })
else:
    insights.append({
        'category': '📈 Year-over-Year Growth',
        'text': "Insufficient data for YoY analysis"
    })

# --- INSIGHT 6: Top 3 Products ---
top_products = df.groupby('Product Name')['Sales'].sum().nlargest(3)

top_products_text = "; ".join([f"'{prod}' (${sales:,.0f})" for prod, sales in top_products.items()])

insights.append({
    'category': '🎯 Top Products',
    'text': f"Top 3: {top_products_text}"
})

# --- INSIGHT 7: Best Month ---
monthly_sales = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum()
best_month = monthly_sales.idxmax()
best_month_sales = monthly_sales.max()

insights.append({
    'category': '📅 Best Month',
    'text': f"{best_month.strftime('%B %Y')} with ${best_month_sales:,.0f} sales"
})

# ============================================
# STEP 4: GENERATE RECOMMENDATIONS
# ============================================

print("\n💡 Generating recommendations...")

recommendations = []

# Recommendation 1: Focus on best category
recommendations.append(f"1. Increase marketing spend on {best_category} category (highest profit contributor)")

# Recommendation 2: Investigate worst region
if worst_region_profit < best_region_profit * 0.5:  # If worst is less than 50% of best
    recommendations.append(f"2. Investigate {worst_region} region performance—profit is {100 - (worst_region_profit/best_region_profit)*100:.0f}% below {best_region}")
else:
    recommendations.append(f"2. Monitor {worst_region} region—lowest profit but within acceptable range")

# Recommendation 3: Discount strategy
if discount_impact < -20:  # If high discount reduces profit by more than 20%
    recommendations.append("3. Review discount strategy—high discounts (≥40%) significantly reduce profitability")
else:
    recommendations.append("3. Current discount strategy appears balanced—continue monitoring")

# Recommendation 4: Top products
recommendations.append(f"4. Create bundle promotions featuring top products: {top_products.index[0]}")

# ============================================
# STEP 5: CREATE EXECUTIVE REPORT
# ============================================

print("\n📄 Generating executive report...")

# Create report header
report_header = f"""
{'='*70}
AI-ASSISTED SALES INSIGHTS REPORT
{'='*70}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Dataset: SuperStore Orders ({len(df):,} records)
Analysis Period: {df['Order Date'].min().strftime('%Y-%m-%d')} to {df['Order Date'].max().strftime('%Y-%m-%d')}
{'='*70}
"""

# Create insights section
insights_section = "\nKEY INSIGHTS:\n" + "-"*70 + "\n"
for i, insight in enumerate(insights, 1):
    insights_section += f"\n{i}. {insight['category']}\n"
    insights_section += f"   {insight['text']}\n"

# Create recommendations section
recommendations_section = "\n" + "="*70 + "\nSTRATEGIC RECOMMENDATIONS:\n" + "-"*70 + "\n"
for rec in recommendations:
    recommendations_section += f"\n{rec}\n"

# Create footer
footer = f"""
{'='*70}
Report generated automatically by AI-Assisted Analytics Workflow
Next steps: Review recommendations with stakeholders, prioritize actions
{'='*70}
"""

# Combine all sections
full_report = report_header + insights_section + recommendations_section + footer

# ============================================
# STEP 6: DISPLAY AND SAVE REPORT
# ============================================

print("\n")
print(full_report)

# Save to file
output_filename = f"automated_insights_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(full_report)

print(f"\n✅ Report saved to: {output_filename}")
print(f"✅ Report also saved to: automated_insights_report.txt (latest)")

# Save a copy as "latest" for easy access
with open('automated_insights_report.txt', 'w', encoding='utf-8') as f:
    f.write(full_report)

print("\n🎉 Analysis complete! Review the report and share with stakeholders.")