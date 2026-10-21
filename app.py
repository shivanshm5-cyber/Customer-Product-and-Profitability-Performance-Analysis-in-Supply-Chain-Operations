import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="APL Logistics Profitability", layout="wide")
st.title("APL Logistics: Customer, Product & Profitability Analysis")


# ---------- Load and clean the data ----------
@st.cache_data
def load_data():
    df = pd.read_csv("data/APL_Logistics.csv", encoding="latin-1")

    # same cleaning steps as the notebook
    df = df.drop(columns=["Order Profit Per Order", "Sales per customer"])
    df = df[~df["Order Status"].isin(["CANCELED", "SUSPECTED_FRAUD"])]
    df = df[df["Benefit per order"] != 0]

    # new columns
    df["Net Sales"] = df["Order Item Total"]
    df["Loss Order"] = df["Benefit per order"] < 0
    return df


df = load_data()


# ---------- Sidebar filters ----------
st.sidebar.header("Filters")

# customer segment
segment_list = sorted(df["Customer Segment"].unique())
selected_segment = st.sidebar.multiselect("Customer Segment", segment_list, default=segment_list)

# market
market_list = ["All"] + sorted(df["Market"].unique())
selected_market = st.sidebar.selectbox("Market", market_list)

# order region (depends on the market chosen)
if selected_market == "All":
    region_options = sorted(df["Order Region"].unique())
else:
    region_options = sorted(df[df["Market"] == selected_market]["Order Region"].unique())
selected_region = st.sidebar.selectbox("Order Region", ["All"] + region_options)

# category
category_list = sorted(df["Category Name"].unique())
selected_category = st.sidebar.multiselect("Category", category_list, default=category_list)

# product (only products from the chosen categories)
product_list = sorted(df[df["Category Name"].isin(selected_category)]["Product Name"].unique())
selected_product = st.sidebar.multiselect("Product", product_list, default=product_list)

# discount rate range
min_rate, max_rate = st.sidebar.slider("Discount Rate", 0.0, 0.25, (0.0, 0.25), step=0.01)


# ---------- Apply the filters ----------
filtered = df[df["Customer Segment"].isin(selected_segment)]
filtered = filtered[filtered["Category Name"].isin(selected_category)]
filtered = filtered[filtered["Product Name"].isin(selected_product)]
filtered = filtered[(filtered["Order Item Discount Rate"] >= min_rate) &
                    (filtered["Order Item Discount Rate"] <= max_rate)]

if selected_market != "All":
    filtered = filtered[filtered["Market"] == selected_market]

if selected_region != "All":
    filtered = filtered[filtered["Order Region"] == selected_region]

# stop if the filters remove every row
if len(filtered) == 0:
    st.warning("No data for these filters. Please change them.")
    st.stop()


# ---------- KPI cards ----------
total_sales = filtered["Net Sales"].sum()
total_profit = filtered["Benefit per order"].sum()
margin = total_profit / total_sales * 100
total_orders = len(filtered)
customers = filtered["Customer Id"].nunique()
loss_share = filtered["Loss Order"].mean() * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Revenue", f"{total_sales:,.0f}")
col2.metric("Total Profit", f"{total_profit:,.0f}")
col3.metric("Profit Margin", f"{margin:.2f}%")
col4.metric("Customers", f"{customers:,}")
col5.metric("Loss-making Orders", f"{loss_share:.1f}%")

import matplotlib.pyplot as plt

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Customer Value", "Product & Category", "Discount Impact"])


# ---------- Tab 1: Revenue & Profit Overview ----------
with tab1:
    st.subheader("Revenue and Profit Overview")

    left, right = st.columns(2)

    # --- Chart 1: revenue share vs profit share by market ---
    with left:
        market_table = filtered.groupby("Market")[["Net Sales", "Benefit per order"]].sum()
        market_table["Margin %"] = market_table["Benefit per order"] / market_table["Net Sales"] * 100
        market_table["Revenue Share %"] = market_table["Net Sales"] / market_table["Net Sales"].sum() * 100
        market_table["Profit Share %"] = market_table["Benefit per order"] / market_table["Benefit per order"].sum() * 100

        positions = np.arange(len(market_table))

        fig1, ax1 = plt.subplots(figsize=(7, 4))
        ax1.bar(positions - 0.2, market_table["Revenue Share %"], width=0.4, label="Revenue share")
        ax1.bar(positions + 0.2, market_table["Profit Share %"], width=0.4, label="Profit share")
        ax1.set_xticks(positions)
        ax1.set_xticklabels(market_table.index)
        ax1.set_ylabel("Share (%)")
        ax1.set_title("Revenue Share vs Profit Share by Market")
        ax1.legend()
        st.pyplot(fig1)

    # --- Chart 2: margin by customer segment ---
    with right:
        segment_table = filtered.groupby("Customer Segment")[["Net Sales", "Benefit per order"]].sum()
        segment_table["Margin %"] = segment_table["Benefit per order"] / segment_table["Net Sales"] * 100

        fig2, ax2 = plt.subplots(figsize=(7, 4))
        ax2.bar(segment_table.index, segment_table["Margin %"])
        ax2.axhline(margin, color="red", linestyle="--", label="Overall margin")
        ax2.set_ylabel("Margin (%)")
        ax2.set_title("Profit Margin by Customer Segment")
        ax2.legend()
        st.pyplot(fig2)

    # --- Table: market numbers ---
    st.write("Market summary")
    st.dataframe(market_table.round(2))

    # --- Chart 3: profit concentration (Pareto curve) ---
    st.subheader("Profit Concentration")

    customer_profit = filtered.groupby("Customer Id")["Benefit per order"].sum()
    customer_profit = customer_profit.sort_values(ascending=False)

    cumulative_profit = customer_profit.cumsum() / customer_profit.sum() * 100
    customer_percent = np.arange(1, len(customer_profit) + 1) / len(customer_profit) * 100

    fig3, ax3 = plt.subplots(figsize=(10, 4))
    ax3.plot(customer_percent, cumulative_profit.values)
    ax3.axhline(100, color="grey", linestyle="--")
    ax3.set_xlabel("Customers, best to worst (%)")
    ax3.set_ylabel("Cumulative profit (%)")
    ax3.set_title("Cumulative Profit Share of Customers")
    st.pyplot(fig3)


# ---------- Tab 2: Customer Value ----------
with tab2:
    st.subheader("Customer Value Dashboard")

    # --- one row per customer ---
    customer_table = filtered.groupby("Customer Id")[["Net Sales", "Benefit per order"]].sum()
    customer_table = customer_table.rename(columns={"Benefit per order": "Profit"})
    customer_table["Orders"] = filtered.groupby("Customer Id")["Benefit per order"].count()
    customer_table["Margin %"] = customer_table["Profit"] / customer_table["Net Sales"] * 100

    # add customer names
    names = filtered.drop_duplicates("Customer Id").set_index("Customer Id")
    customer_table["Name"] = names["Customer Fname"] + " " + names["Customer Lname"].fillna("")

    # --- customer KPIs ---
    loss_customers = customer_table[customer_table["Profit"] < 0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Customers", f"{len(customer_table):,}")
    c2.metric("Loss-making Customers", f"{len(loss_customers):,}")
    c3.metric("Loss from Them", f"{loss_customers['Profit'].sum():,.0f}")

    # --- top and bottom customers ---
    st.subheader("Top and Bottom Customers by Profit")
    how_many = st.slider("Number of customers to show", 5, 20, 10)

    sorted_customers = customer_table.sort_values("Profit", ascending=False)
    show_cols = ["Name", "Net Sales", "Profit", "Orders", "Margin %"]

    left, right = st.columns(2)
    with left:
        st.write("Top customers")
        st.dataframe(sorted_customers.head(how_many)[show_cols].round(1))
    with right:
        st.write("Bottom customers")
        st.dataframe(sorted_customers.tail(how_many)[show_cols].round(1))

    # --- value tiers ---
    st.subheader("Customer Value Tiers")

    profitable = customer_table[customer_table["Profit"] > 0]

    if len(profitable) < 4:
        st.info("Too few profitable customers for tiers. Widen the filters.")
    else:
        low_limit = profitable["Profit"].quantile(0.25)
        high_limit = profitable["Profit"].quantile(0.75)

        customer_table["Tier"] = pd.cut(
            customer_table["Profit"],
            bins=[-float("inf"), 0, low_limit, high_limit, float("inf")],
            labels=["Loss-making", "Low value", "Medium value", "High value"]
        )

        tier_table = customer_table.groupby("Tier", observed=True)[["Net Sales", "Profit"]].sum()
        tier_table["Customers"] = customer_table["Tier"].value_counts()
        tier_table["Margin %"] = tier_table["Profit"] / tier_table["Net Sales"] * 100
        tier_table["Profit Share %"] = tier_table["Profit"] / tier_table["Profit"].sum() * 100

        left, right = st.columns(2)
        with left:
            st.dataframe(tier_table.round(1))
        with right:
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            bar_colors = ["green" if p > 0 else "red" for p in tier_table["Profit"]]
            ax4.bar(tier_table.index.astype(str), tier_table["Profit"], color=bar_colors)
            ax4.axhline(0, color="black", linewidth=0.8)
            ax4.set_ylabel("Total profit")
            ax4.set_title("Profit by Customer Tier")
            st.pyplot(fig4)

    # --- segment contribution ---
    st.subheader("Customer Segment Contribution")

    seg_profit = filtered.groupby("Customer Segment")["Benefit per order"].sum()
    seg_customers = filtered.groupby("Customer Segment")["Customer Id"].nunique()
    seg_table = pd.DataFrame({"Profit": seg_profit, "Customers": seg_customers})
    seg_table["Customer Value Index"] = seg_table["Profit"] / seg_table["Customers"]
    seg_table["Profit Share %"] = seg_table["Profit"] / seg_table["Profit"].sum() * 100

    left, right = st.columns(2)
    with left:
        st.dataframe(seg_table.round(1))
    with right:
        fig5, ax5 = plt.subplots(figsize=(6, 4))
        ax5.bar(seg_table.index, seg_table["Customer Value Index"])
        ax5.set_ylabel("Profit per customer")
        ax5.set_title("Customer Value Index by Segment")
        st.pyplot(fig5)
# ---------- Tab 3: Product & Category ----------
with tab3:
    st.subheader("Product and Category Performance")

    # ===== Category table =====
    category_table = filtered.groupby("Category Name")[["Net Sales", "Benefit per order"]].sum()
    category_table = category_table.rename(columns={"Benefit per order": "Profit"})
    category_table["Orders"] = filtered.groupby("Category Name")["Benefit per order"].count()
    category_table["Margin %"] = category_table["Profit"] / category_table["Net Sales"] * 100
    category_table["Loss Orders %"] = filtered.groupby("Category Name")["Loss Order"].mean() * 100

    # --- category KPIs ---
    loss_categories = category_table[category_table["Profit"] < 0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Categories", len(category_table))
    c2.metric("Loss-making Categories", len(loss_categories))
    c3.metric("Lowest Category Margin", f"{category_table['Margin %'].min():.1f}%")
    st.caption("Lowest margin: " + category_table["Margin %"].idxmin() +
               " | Highest margin: " + category_table["Margin %"].idxmax())

    # --- category margin chart ---
    st.subheader("Category Margin")
    sort_by = st.radio("Sort categories by", ["Margin %", "Net Sales"], horizontal=True)
    sorted_categories = category_table.sort_values(sort_by)

    # green = at or above overall margin, red = below
    bar_colors = ["green" if m >= margin else "red" for m in sorted_categories["Margin %"]]

    fig6, ax6 = plt.subplots(figsize=(9, max(4, len(sorted_categories) * 0.3)))
    ax6.barh(sorted_categories.index, sorted_categories["Margin %"], color=bar_colors)
    ax6.axvline(margin, color="black", linestyle="--", label="Overall margin")
    ax6.set_xlabel("Margin (%)")
    ax6.set_title("Margin by Category (red = below overall margin)")
    ax6.legend()
    st.pyplot(fig6)

    # ===== Heatmap =====
    st.subheader("Category Profitability Heatmap")
    heat_col = st.selectbox("Compare categories across", ["Market", "Customer Segment"])

    heat_sales = filtered.pivot_table(index="Category Name", columns=heat_col,
                                      values="Net Sales", aggfunc="sum")
    heat_profit = filtered.pivot_table(index="Category Name", columns=heat_col,
                                       values="Benefit per order", aggfunc="sum")
    heatmap = heat_profit / heat_sales * 100

    fig7, ax7 = plt.subplots(figsize=(8, max(4, len(heatmap) * 0.3)))
    picture = ax7.imshow(heatmap.values, cmap="RdYlGn", aspect="auto")
    fig7.colorbar(picture, label="Margin (%)")
    ax7.set_xticks(range(heatmap.shape[1]))
    ax7.set_xticklabels(heatmap.columns)
    ax7.set_yticks(range(heatmap.shape[0]))
    ax7.set_yticklabels(heatmap.index)

    # write the number inside each cell
    for row in range(heatmap.shape[0]):
        for col in range(heatmap.shape[1]):
            value = heatmap.values[row, col]
            if not np.isnan(value):
                ax7.text(col, row, f"{value:.0f}", ha="center", va="center", fontsize=7)

    ax7.set_title("Margin % by Category and " + heat_col)
    st.pyplot(fig7)
    st.caption("Blank cells mean that category has no orders in that column. "
               "Cells based on very few orders can look extreme.")

    # ===== Product analysis =====
    st.subheader("Product Margin Analysis")

    product_table = filtered.groupby("Product Name")[["Net Sales", "Benefit per order"]].sum()
    product_table = product_table.rename(columns={"Benefit per order": "Profit"})
    product_table["Orders"] = filtered.groupby("Product Name")["Benefit per order"].count()
    product_table["Margin %"] = product_table["Profit"] / product_table["Net Sales"] * 100

    # --- top products by sales ---
    product_count = st.slider("Number of top-selling products to show", 5, 30, 10)
    st.write("Top products by sales")
    top_products = product_table.sort_values("Net Sales", ascending=False).head(product_count)
    st.dataframe(top_products.round(1))

    # --- scatter: sales vs margin ---
    high_sales_limit = product_table["Net Sales"].quantile(0.75)
    is_problem = (product_table["Net Sales"] >= high_sales_limit) & (product_table["Margin %"] < margin)

    normal = product_table[~is_problem]
    problem = product_table[is_problem]

    fig8, ax8 = plt.subplots(figsize=(10, 5))
    ax8.scatter(normal["Net Sales"], normal["Margin %"], alpha=0.6, label="Other products")
    ax8.scatter(problem["Net Sales"], problem["Margin %"], color="red", label="High sales, below-average margin")
    ax8.axhline(margin, color="black", linestyle="--", label="Overall margin")
    ax8.set_xscale("log")
    ax8.set_xlabel("Net Sales (log scale)")
    ax8.set_ylabel("Margin (%)")
    ax8.set_title("Product Sales vs Margin")
    ax8.legend()
    st.pyplot(fig8)

    # --- problem products table ---
    st.write("High-revenue but below-average-margin products (top 25% by sales)")
    if len(problem) == 0:
        st.success("No such products with the current filters.")
    else:
        st.dataframe(problem.sort_values("Margin %").round(1))

    # --- loss-making products ---
    st.write("Loss-making products")
    loss_products = product_table[product_table["Profit"] < 0]
    if len(loss_products) == 0:
        st.success("No loss-making products with the current filters.")
    else:
        st.dataframe(loss_products.sort_values("Profit").round(1))   
             
# ---------- Tab 4: Discount Impact Analyzer ----------
with tab4:
    st.subheader("Discount Impact Analyzer")

    # work on a copy so the main data is not changed
    discount_data = filtered.copy()
    discount_data["Discounted"] = np.where(discount_data["Order Item Discount"] > 0, "Yes", "No")
    discount_data["Discount Band"] = pd.cut(
        discount_data["Order Item Discount Rate"],
        bins=[-0.01, 0, 0.05, 0.10, 0.15, 0.20, 0.25],
        labels=["0%", "0-5%", "5-10%", "10-15%", "15-20%", "20-25%"]
    )

    current_sales = discount_data["Net Sales"].sum()
    current_profit = discount_data["Benefit per order"].sum()
    current_margin = current_profit / current_sales * 100

    # ===== Discount KPIs =====
    total_discount = discount_data["Order Item Discount"].sum()
    gross_sales = discount_data["Sales"].sum()
    discounted_share = (discount_data["Discounted"] == "Yes").mean() * 100
    correlation = discount_data["Order Item Discount Rate"].corr(discount_data["Order Item Profit Ratio"])

    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Total Discount Given", f"{total_discount:,.0f}")
    d2.metric("Discount as % of Gross Sales", f"{total_discount / gross_sales * 100:.1f}%")
    d3.metric("Orders with a Discount", f"{discounted_share:.1f}%")
    if np.isnan(correlation):
        d4.metric("Discount vs Profit Ratio Correlation", "n/a")
    else:
        d4.metric("Discount vs Profit Ratio Correlation", f"{correlation:.4f}")
    st.caption("A correlation near 0 means the discount rate has almost no linear link with the profit ratio.")

    # ===== Discounted vs not discounted =====
    st.subheader("With and Without Discounts")
    yes_no = discount_data.groupby("Discounted")[["Net Sales", "Benefit per order"]].sum()
    yes_no["Orders"] = discount_data["Discounted"].value_counts()
    yes_no["Margin %"] = yes_no["Benefit per order"] / yes_no["Net Sales"] * 100
    st.dataframe(yes_no.round(2))

    # ===== Margin and loss share by discount band =====
    st.subheader("Discount vs Margin")

    band_table = discount_data.groupby("Discount Band", observed=True)[["Net Sales", "Benefit per order"]].sum()
    band_table["Orders"] = discount_data["Discount Band"].value_counts()
    band_table["Margin %"] = band_table["Benefit per order"] / band_table["Net Sales"] * 100
    band_table["Loss Orders %"] = discount_data.groupby("Discount Band", observed=True)["Loss Order"].mean() * 100

    left, right = st.columns(2)
    with left:
        fig9, ax9 = plt.subplots(figsize=(6, 4))
        ax9.bar(band_table.index.astype(str), band_table["Margin %"])
        ax9.axhline(current_margin, color="red", linestyle="--", label="Overall margin")
        ax9.set_xlabel("Discount band")
        ax9.set_ylabel("Margin (%)")
        ax9.set_title("Margin by Discount Band")
        ax9.legend()
        st.pyplot(fig9)

    with right:
        fig10, ax10 = plt.subplots(figsize=(6, 4))
        ax10.bar(band_table.index.astype(str), band_table["Loss Orders %"], color="orange")
        ax10.set_xlabel("Discount band")
        ax10.set_ylabel("Loss-making orders (%)")
        ax10.set_title("Share of Loss-Making Orders by Discount Band")
        st.pyplot(fig10)

    st.dataframe(band_table.round(2))

    # --- exact discount rate vs margin ---
    rate_table = discount_data.groupby("Order Item Discount Rate")[["Net Sales", "Benefit per order"]].sum()
    rate_table["Margin %"] = rate_table["Benefit per order"] / rate_table["Net Sales"] * 100

    fig11, ax11 = plt.subplots(figsize=(10, 4))
    ax11.plot(rate_table.index * 100, rate_table["Margin %"], marker="o")
    ax11.axhline(current_margin, color="red", linestyle="--", label="Overall margin")
    ax11.set_xlabel("Discount rate (%)")
    ax11.set_ylabel("Margin (%)")
    ax11.set_title("Margin at Each Exact Discount Rate")
    ax11.legend()
    st.pyplot(fig11)

    # ===== Discount Impact Ratio =====
    st.subheader("Discount Impact Ratio")
    margin_without_discount = (current_profit + total_discount) / gross_sales * 100

    i1, i2, i3 = st.columns(3)
    i1.metric("Actual Margin", f"{current_margin:.2f}%")
    i2.metric("Margin if No Discounts", f"{margin_without_discount:.2f}%")
    i3.metric("Margin Lost to Discounts", f"{margin_without_discount - current_margin:.2f} points")
    st.caption("Theoretical upper limit: assumes costs stay the same and every order would still be placed at full price.")

    # ===== What-if scenario =====
    st.subheader("What-if: Cap the Maximum Discount")
    st.write("If no order could get a discount above the cap, how would profit change?")

    w1, w2 = st.columns(2)
    with w1:
        cap = st.slider("Maximum discount allowed (%)", 0, 25, 10) / 100
    with w2:
        lost_share = st.slider("Share of affected orders lost because of the cap (%)", 0, 100, 0) / 100

    rate = discount_data["Order Item Discount Rate"]
    affected = rate > cap + 0.0001

    # extra money collected on affected orders: the part of the discount above the cap
    safe_rate = rate.where(rate > 0, 1)    # avoids dividing by zero
    extra_money = (discount_data["Order Item Discount"] * (rate - cap) / safe_rate).where(affected, 0)

    extra_total = extra_money.sum()
    affected_sales = discount_data.loc[affected, "Net Sales"].sum()
    affected_profit = discount_data.loc[affected, "Benefit per order"].sum()

    # keep unaffected orders, and keep only the surviving share of affected orders
    new_sales = (current_sales - affected_sales) + (1 - lost_share) * (affected_sales + extra_total)
    new_profit = (current_profit - affected_profit) + (1 - lost_share) * (affected_profit + extra_total)
    new_margin = new_profit / new_sales * 100

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Orders Affected", f"{affected.sum():,}", f"{affected.mean() * 100:.1f}% of orders", delta_color="off")
    s2.metric("New Profit", f"{new_profit:,.0f}", f"{new_profit - current_profit:,.0f}")
    s3.metric("New Margin", f"{new_margin:.2f}%", f"{new_margin - current_margin:.2f} points")
    s4.metric("New Revenue", f"{new_sales:,.0f}", f"{new_sales - current_sales:,.0f}")

    # --- break-even: how many affected orders can we lose before profit falls? ---
    if extra_total > 0 and (affected_profit + extra_total) > 0:
        break_even = min(1 - affected_profit / (affected_profit + extra_total), 1)
        st.info(f"Break-even: profit stays higher than today as long as fewer than "
                f"{break_even * 100:.0f}% of the affected orders are lost.")

        shares = np.linspace(0, 1, 101)
        profit_change = (1 - shares) * (affected_profit + extra_total) - affected_profit

        fig12, ax12 = plt.subplots(figsize=(10, 4))
        ax12.plot(shares * 100, profit_change)
        ax12.axhline(0, color="black", linewidth=0.8)
        ax12.axvline(lost_share * 100, color="red", linestyle="--", label="Your selection")
        ax12.set_xlabel("Share of affected orders lost (%)")
        ax12.set_ylabel("Change in total profit")
        ax12.set_title(f"Profit Change if Discounts Are Capped at {cap * 100:.0f}%")
        ax12.legend()
        st.pyplot(fig12)
    else:
        st.info("No orders are affected at this cap, so nothing changes.")

    st.caption("This is an accounting scenario, not a forecast. It assumes costs stay the same. "
               "The data contains no information on how customers would react, so the lost-orders slider is an assumption.")        