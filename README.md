# APL Logistics: Customer, Product and Profit Analysis

**Made by:** Shivansh Mishra

## About the Project
APL Logistics is a logistics company. It has a lot of order data, but it mostly looks
at sales and delivery speed. High sales do not always mean high profit, so in this
project I looked at the data to find out:

- Which customers, products and markets really make money?
- Do discounts reduce profit?
- Which markets sell a lot but earn little profit?

I did the analysis in a Jupyter notebook and then built a dashboard with Streamlit.

## What is in This Repository
| File / Folder | What it is |
|---|---|
| `notebooks/eda.ipynb` | My data analysis (cleaning, charts, findings) |
| `app.py` | The Streamlit dashboard |
| `reports/research_paper.md` | Research paper |
| `reports/executive_summary.md` | One-page summary |
| `data/APL_Logistics.csv` | The dataset |
| `requirements.txt` | Python libraries needed |

## Dataset
- About 180,000 orders and 40 columns (sales, profit, discount, customer, product, market, shipping, etc.)
- Source: [add where you got the dataset]
- Note: the file must be read with `encoding="latin-1"` in pandas.

## How I Cleaned the Data
1. Removed 2 duplicate columns (they had the same values as other columns).
2. Removed canceled orders and suspected-fraud orders, because they are not real sales.
3. Removed orders with zero profit.
4. Kept the loss-making orders, because I wanted to study them.

After cleaning I had 171,649 orders from 20,210 customers.

## Main Findings
- Total sales were about 31.4 million and total profit about 3.81 million.
  The profit margin is about **12.1%**.
- The top 20% of customers give about **79% of the profit**.
- About 20% of customers (around 4,000) lose money. Together they lose about 1.05 million.
- Discounts do not seem to change the margin. Orders with big discounts earn about
  the same margin as orders with small discounts.
- Still, discounts reduce total sales by about 10%.
- No product category loses money overall.
- Markets, customer types and shipping modes all have similar margins (around 12%).

## Dashboard
The dashboard has 4 tabs and filters on the left side (customer segment, market,
region, category, product and discount range).

1. **Overview:** total sales, profit and margin, and market comparison
2. **Customer Value:** best and worst customers, customer groups
3. **Product & Category:** margin of each category and product, heatmap
4. **Discount Impact:** discount vs margin, and a "what if we limit discounts" tool

[Add one screenshot of each tab here]

## Limitations
- The data has no dates, so I could not study trends over time.
- The data has no cost columns, so the discount "what if" tool assumes costs stay the same.
- Some orders lose more money than they sold for. This could be a mistake in the data.
- A link between two things does not always mean one causes the other.

## How to Run
1. Download or clone this repository.
2. Install the libraries:
```bash
pip install -r requirements.txt
```
3. Open the notebook:
```bash
jupyter notebook notebooks/eda.ipynb
```
4. Run the dashboard:
```bash
python -m streamlit run app.py
```

## Tools Used
Python, pandas, NumPy, Matplotlib, Streamlit

 