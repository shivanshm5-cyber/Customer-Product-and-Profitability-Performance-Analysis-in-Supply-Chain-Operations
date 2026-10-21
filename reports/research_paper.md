# Customer, Product and Profit Analysis for APL Logistics

**Name:** Shivansh Mishra

---

## 1. Summary

In this project I studied about 180,000 orders of APL Logistics to find out which
customers, products and markets make profit and where money is being lost. After
cleaning the data, I had 171,649 orders from 20,210 customers.

The company made about 31.4 million in sales and 3.81 million in profit, which is a
profit margin of 12.1%. A small group of customers makes most of the profit: the top
20% of customers give about 79% of it. At the same time, about 20% of customers lose
money. I also found that bigger discounts did not lead to lower margins in this data.
Markets, customer types and shipping modes were all quite similar.

## 2. Objective

APL Logistics mainly looks at sales, but high sales do not always mean high profit.
The goals of this project were to:

1. Find the total sales, profit and margin of the company.
2. Find which products and categories earn low margins or lose money.
3. Find the best and worst customers.
4. Check whether discounts reduce profit.
5. Compare the markets and regions.
6. Build a dashboard to show these results.

## 3. About the Data

The dataset has 180,519 rows and 40 columns. It includes information about the
customer, product, category, market, region, discount, shipping, sales and profit.
It does not have a date column or any cost columns. All money values are in one
currency, so I did not have to convert anything.

## 4. How I Did the Analysis

### 4.1 Cleaning the data
- I read the file using `latin-1` encoding because the normal encoding gave an error.
- I removed two columns that were exact copies of other columns.
- I removed canceled orders and suspected-fraud orders because they are not real sales.
- I removed rows with zero profit, as the project guide says.
- I **kept** the loss-making orders, because they are what I wanted to study.
- I checked for duplicate rows (none) and missing values (very few).

After cleaning, 171,649 orders and 20,210 customers were left.

### 4.2 Measures I used
- **Profit margin (%)** = total profit / total sales x 100. For a group, I add up the
  profit and sales of the group first and then divide. I did not average the
  percentages of single orders, because that treats small and big orders the same.
- **Customer groups:** customers with zero or negative profit are "Loss-making". Among
  the profitable customers, the bottom 25% are "Low value", the middle 50% are
  "Medium value" and the top 25% are "High value".
- **Discount bands:** I put discounts into ranges (0%, 0-5%, 5-10% and so on) to compare them.

### 4.3 Method
I grouped the data by customer, product, category, discount, market, region and shipping
mode. For each group I found the total sales, profit and margin and compared it with the
overall margin of 12.1%. I also checked correlation between profit and other columns.

## 5. Results

### 5.1 Overall picture
| Measure | Value |
|---|---|
| Orders | 171,649 |
| Customers | 20,210 |
| Total sales (after discount) | about 31.4 million |
| Total profit | about 3.81 million |
| Profit margin | 12.1% |
| Orders that lose money | about 19% |

About 1 out of every 5 orders loses money. A few orders have very big losses (72 orders
lost more than 1,000 each), but together they are only about 2.9% of all losses. So the
losses are spread across many orders.

### 5.2 Customers
The top 20% of customers give about 79% of all profit. I divided customers into groups:

| Group | Customers | Margin | Share of profit |
|---|---|---|---|
| High value | 4,052 | 23.6% | about 79% |
| Medium value | 8,104 | 15.7% | about 46% |
| Low value | 4,053 | 6.3% | about 2% |
| Loss-making | 4,001 | -17.1% | about -28% |

The shares add up to more than 100% because the loss-making group has negative profit.

About 4,000 customers (around 20%) lose money. Together they lose about 1.05 million,
even though they bring in about 6.1 million in sales. So they look good if we only look
at sales, but they are bad for profit. Some customers made just one order and lost more
than the value of that order.

When I compared customer types (Consumer, Corporate, Home Office), the profit per
customer was almost the same (about 190, 190 and 183). So the customer type does not
decide whether a customer is good or bad.

### 5.3 Products and categories
- None of the 50 categories loses money overall. Margins go from about 0.5%
  (Strength Training) to about 19.6% (Golf Bags and Carts), and most are near 12%.
- The weakest categories (Strength Training, Men's Clothing, Books) are small in
  sales, so they do not affect the total profit much.
- Out of 118 products, only two lose money: SOLE E35 Elliptical and SOLE E25 Elliptical.
  The losses are small.
- Twelve products are in the top 25% by sales but have a margin below average. Most are
  only slightly below 12.1%.
- One product, the Field & Stream Sportsman 16 Gun Fire Safe, gives about 19% of the
  total profit. This means the company depends a lot on it.

### 5.4 Discounts
| Measure | Result |
|---|---|
| Orders with a discount | about 94% |
| Total discount given | about 3.55 million (about 10.1% of gross sales) |
| Margin with discount | 12.04% |
| Margin without discount | 13.04% |
| Correlation of discount rate and profit ratio | about -0.002 (almost zero) |

I expected that bigger discounts would lower the margin. But the margin stayed between
about 11.8% and 13% in all discount ranges, and the share of loss-making orders stayed
at about 18% to 19%. Orders that lose money and orders that make profit have almost the
same average discount (about 10.2%). So in this data, **discounts do not seem to cause
the losses.** Still, discounts reduce total sales by about 10%.

**What-if: limiting the maximum discount.** I calculated how much extra profit the company
would get if no order could have a discount above a limit. This assumes costs stay the
same and no customer leaves.

| Maximum discount | Orders affected | Extra profit | New margin |
|---|---|---|---|
| 20% | 9,521 | about 97 thousand | 12.4% |
| 15% | 47,700 | about 408 thousand | 13.2% |
| 10% | 76,260 | about 1.09 million | 15.1% |
| 5% | 114,416 | about 2.10 million | 17.6% |

With a 10% limit, the company still gains profit unless about 40% of the affected
orders are lost. These numbers are the best case, because I do not know how customers
would react.

### 5.5 Markets and regions
- All markets have similar margins, from about 11.7% (Pacific Asia) to about 12.5% (USCA).
  For every market, the share of sales is almost equal to the share of profit.
- North Africa (about 10.9%) and Eastern Asia (about 11.1%) have the lowest margins among
  regions. Southern Africa (about 15.1%) and Canada (about 14.2%) are the highest, but
  they are small.
- Some small countries show very high or very low margins, but they have very few
  orders, so I do not trust those numbers much.

### 5.6 Shipping
The margin is almost the same for all shipping modes (about 11.7% for Same Day to about
12.8% for First Class). Late deliveries have a margin of about 11.9% and on-time ones
about 12.5%, which is a small difference.

### 5.7 A problem in the data
About 6,017 orders (3.5%) lose more money than the value of the sale. Together they lose
about 1.97 million on about 1.12 million of sales. This may be due to real costs like
returns or shipping, or it may be a mistake in the data. The dataset has no cost
columns, so I could not check. Also, profit had almost no relation (correlation near 0)
with discount, quantity, price, sales or delivery delay.

## 6. What I Learned

1. **Profit depends on the customer,** not on the customer type, market or shipping
   mode. A small group of customers brings most of the profit, and another group loses it.
2. **Discounts are given on almost every order.** They do not lower the margin in this
   data, but they reduce total sales by about 10%.
3. **About 1 in 5 orders loses money in almost every group.** The reason is probably in
   costs that are not in this dataset.

## 7. Recommendations

1. **Check the loss-making customers.** About 4,000 customers lose about 1.05 million.
   Look at their prices, discounts and costs and change their terms if needed.
2. **Keep the high-value customers happy.** They give about 79% of the profit.
3. **Try a discount limit on a small group first.** A limit of 15% to 20% affects fewer
   orders and is safer. A 10% limit can give more profit but only works if fewer than
   about 40% of affected orders are lost.
4. **Check the orders that lose more than they sold for.** There are about 6,000 of them.
   Find out if it is returns, shipping costs or wrong data.
5. **Watch the products that give a lot of profit,** like the Gun Fire Safe.
6. **Do not change prices by customer type, market or shipping mode** only because of this
   data, since the differences are small.
7. **Collect more data,** like order dates, product cost, shipping cost and returns.

## 8. Limitations

- There is no date column, so I could not look at trends over time.
- There are no cost columns, so the discount what-if assumes the costs stay the same and
  that customers do not leave.
- Some orders lose more than their sale value, which may be a data problem.
- If two things move together, it does not prove that one causes the other.
- Results for small categories and small countries are based on very few orders.
- Removing canceled and fraud orders was my own decision, and it changes all the numbers a little.

## 9. Conclusion

APL Logistics earns a healthy margin of 12.1% overall, but this hides a big difference
between customers. About a fifth of the customers give most of the profit and another
fifth lose money. Discounts are very common but do not seem to affect margin in this
data, and markets, customer types and shipping modes look similar. The best next steps
are to manage loss-making customers, to control discounts carefully and to collect cost
data so the real reasons for losses can be found.

## 10. Tools Used
Python (pandas, NumPy, Matplotlib) for analysis and Streamlit for the dashboard.