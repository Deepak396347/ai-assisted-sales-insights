# AI-Assisted Sales Insights Automation

A Python script that reads a sales CSV and automatically produces a standardized executive report: key metrics, seven insights and four recommendations, saved as a text file.

## Problem

Weekly sales reviews usually mean re-calculating the same KPIs by hand from raw data. This is slow, and the wording and numbers can differ from one report to the next. This project automates that routine step so the same analysis can be re-run on fresh data in seconds.

## What the script does

1. Loads the sales CSV and cleans it (text encoding, comma-formatted numbers, day-first dates)
2. Calculates overall revenue, profit, profit margin and order count
3. Generates 7 insights
4. Generates 4 rule-based recommendations
5. Prints the report and saves it as a timestamped `.txt` file plus a "latest" copy

```
CSV data  ->  pandas cleaning  ->  metrics + insights  ->  recommendations  ->  text report
```

## Insights generated

1. **Overall performance**: revenue, profit, margin, unique order count
2. **Category performance**: best and worst category by profit
3. **Regional performance**: best and worst region by profit
4. **Discount impact**: average profit per order line, with 40%+ discount vs no discount
5. **Year-over-year growth**: sales growth between the last two years
6. **Top products**: top 3 products by sales
7. **Best month**: month with the highest sales

## Dataset

Superstore orders: 51,290 order lines, 25,035 unique orders, January 2011 to December 2014.

Data issues handled in the script:
- The file is not UTF-8, so it is read with `encoding='latin-1'`
- Column names are lowercase with underscores, so they are renamed to the format the script expects
- `sales` contains thousands separators (for example `1,106`), so commas are removed before converting to numbers
- Dates are in day-month-year format, so the format is set explicitly (`%d-%m-%Y`). Without this, about 60% of rows were silently dropped.

## Results from the actual run

| Metric | Value |
|---|---|
| Total sales | $12,642,905 |
| Total profit | $1,469,035 |
| Profit margin | 11.6% |
| Unique orders | 25,035 |
| Best category by profit | Technology ($663,779) |
| Lowest category by profit | Furniture ($286,782) |
| Best region by profit | Central ($311,404) |
| Sales growth 2013 to 2014 | 26.3% ($3.41M to $4.30M) |
| Best month | November 2014 ($555,312 sales) |

Discount finding: order lines with a 40%+ discount average **-$76.07 profit**, versus **$61.04** for lines with no discount.

## How to run

**Requirements:** Python 3.x and pandas (`pip install pandas`)

1. Put `SuperStore_Orders.csv` inside a folder named `data`
2. Open a terminal in the project folder
3. Run:

```bash
python automated_insights.py
```

The report appears in the terminal and is saved as `automated_insights_report.txt`.

## Project structure

```
ai_assisted_insights_project/
├── data/
│   └── SuperStore_Orders.csv
├── automated_insights.py
├── automated_insights_report.txt
└── README.md
```

## Limitations

- Region comparison uses **total profit**, so a small market (such as Canada) looks weak next to a large one. Comparing profit margin per region would be fairer.
- Recommendations are simple rules based on the numbers, not causal analysis. They are starting points for discussion.
- Discount analysis looks at average profit per order line and does not control for product category or region.
- Works on CSV files only, run manually.

## Future improvements

- [ ] Compare regions by profit margin instead of total profit
- [ ] Export the report as PDF
- [ ] Email the report automatically
- [ ] Schedule it with Windows Task Scheduler
- [ ] Read data from a SQL database instead of a CSV
- [ ] Use an LLM to write the narrative text

## Author

**Deepak Pandey**
[LinkedIn](https://linkedin.com/in/deepak-pandey-800188220) | [GitHub](https://github.com/Deepak396347)
