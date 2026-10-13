# Customer, Product & Profitability Analysis: APL Logistics

**Author:** Shivansh Mishra

## Overview
APL Logistics has detailed order data but limited visibility into which
customers, products and markets actually generate profit. This project
analyzes ~180K orders to find where value is created and lost.

## Business Questions
- Which customers, products and regions generate real profit?
- Do discounts erode profit margins?
- Which markets have strong revenue but weak profit?

## Dataset
- ~180,000 orders, 40 columns (sales, profit, discounts, customer, product, market)
- Source: [add where the dataset came from]
- File encoding is latin-1 (`pd.read_csv(..., encoding="latin-1")`)

## Data Cleaning
- Removed duplicate columns (`Order Profit Per Order`, `Sales per customer`)
- Removed canceled and suspected-fraud orders (not real revenue)
- Removed zero-profit records; **kept** loss-making orders for analysis
- Result: 171,649 orders, 20,210 customers

## Key Findings
- Overall net revenue ~31.4M, profit ~3.81M, **margin ~12.1%**
- Top 20% of customers generate **~79% of profit**
- ~20% of customers are loss-making, erasing ~28% of profit
- **No clear link between discount rate and margin** (correlation ≈ 0);
  discounts forgo ~10% of gross sales
- No loss-making category; losses are spread evenly (~1 in 5 orders)
- Markets and customer segments have very similar margins (~12%)

## Limitations
- No date column, so no time-trend analysis
- Some orders lose more than their sale value (possible data quirk)
- No cost data, so discount impact assumes costs stay constant
- Correlation does not prove causation

## Project Structure
```
apl-logistics-profitability/
├── data/
│   └── APL_Logistics.csv
├── notebooks/
│   └── eda.ipynb
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run
```bash
git clone <your-repo-link>
cd apl-logistics-profitability
pip install -r requirements.txt
jupyter notebook notebooks/eda.ipynb
streamlit run app.py      # once the dashboard is built
```

## Tools Used
Python, pandas, NumPy, Matplotlib, Streamlit

