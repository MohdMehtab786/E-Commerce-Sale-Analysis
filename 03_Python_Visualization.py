import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_excel("Cleaned_data.xlsx")
print(df.shape)

fig, axes=plt.subplots(2,2, figsize=(12,8 ))
sns.set_style("ticks")

# Revenue Distribution
sns.histplot(df["revenue"], kde=True, color="blue",
             ax=axes[0,0])
axes[0,0].set_title("Revenue Distribution")
axes[0,0].set_xlabel("Revenue")
axes[0,0].set_ylabel("Frequency")

# Quantity Dsitribution
sns.histplot(df["quantity"], kde=True, color="blue", ax=axes[0,1])
axes[0,1].set_title("Quantity Distribution")
axes[0,1].set_xlabel("Quantity")
axes[0,1].set_ylabel("Frequency")

# discount Distribution
sns.histplot(df["discount"], kde=True, color="blue", ax=axes[1,0])
axes[1,0].set_title("Discount Distribution")
axes[1,0].set_xlabel("Discount")
axes[1,0].set_ylabel("Frequency")

# Rating Distribution 

sns.histplot(df["customer_rating"], kde=True, color="blue", ax=axes[1,1])
axes[1,1].set_title("Rating Distribution")
axes[1,1].set_xlabel("Customer Rating")
axes[1,1].set_ylabel("Frequency")

plt.tight_layout()
fig.savefig(
    "visualization/distribution.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# BOXPLOT(useful for seeing median, spread and potential outliers)
fig, axes=plt.subplots(2,2, figsize=(12,8 ))
sns.set_style("ticks")

# Revenue
sns.boxplot(data=df,
            x="revenue", color="blue",
            ax=axes[0,0])
axes[0,0].set_title("Revenue Boxplot")
axes[0,0].set_xlabel("Revenue")

# Quantity Boxplot
sns.boxplot(data=df,
            x="quantity", color="blue",
            ax=axes[0,1])
axes[0,1].set_title("Quantity Boxplot")
axes[0,1].set_xlabel("Quantity")

# Discount Boxplot
sns.boxplot(data=df,
            x="discount",
            color="blue",
            ax=axes[1,0])
axes[1,0].set_title("Discount Boxplot")
axes[1,0].set_xlabel("Discount")

# Rating BoxPLot
sns.boxplot(data=df,
            x="customer_rating", color="blue",
            ax=axes[1,1])
axes[1,1].set_title("Customer Rating Boxplot")
axes[1,1].set_xlabel("Cistomer Rating")

plt.tight_layout()
fig.savefig(
    "visualization/boxplot.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# Categorical Analysis Visualization
# revenue by product
fig, axes=plt.subplots(2,2, figsize=(12,8))
rev_by_product=(df.groupby("product_category")["revenue"].sum())
sns.barplot(
            x=rev_by_product.index,
            y=rev_by_product.values,
            ax=axes[0,0],
            )
for container in axes[0,0].containers:
    axes[0,0].bar_label(container, fmt="%.0f", padding=1)
axes[0,0].set_title("Revenue By Product")
axes[0,0].set_xlabel("Product")
axes[0,0].set_ylabel("Revenue")


# Revenue by Region
rev_by_region=(df.groupby("region")["revenue"].sum().sort_values(ascending=False))

sns.barplot(
    x=rev_by_region.index,
    y=rev_by_region.values,
    ax=axes[0,1]
)
for container in axes[0,1].containers:
    axes[0,1].bar_label(container, fmt="%.0f", padding=1)
axes[0,1].set_title("Sales By Region")
axes[0,1].set_xlabel("Region")
axes[0,1].set_ylabel("Revenue")

# Order by Payment Method
order_by_payment=(df.groupby("payment_method")["order_id"].nunique())
sns.barplot(
    x=order_by_payment.index,
    y=order_by_payment.values,
    ax=axes[1,0]
)
for container in axes[1,0].containers:
    axes[1,0].bar_label(container, fmt="%.0f", padding=2)
axes[1,0].set_title("Order BY Payment  Method")
axes[1,0].set_xlabel("Payemnt Method")
axes[1,0].set_ylabel("Total Orders")


# Quantity BY Product
quantity_by_product=(df.groupby("product_category")["quantity"].sum().sort_values(ascending=False))
sns.barplot(
    x=quantity_by_product.index,
    y=quantity_by_product.values,
    ax=axes[1,1]
)
for container in axes[1,1].containers:
    axes[1,1].bar_label(container, fmt="%.0f", padding=1)
axes[1,1].set_title("Quantity Sold By Product")
axes[1,1].set_xlabel("Product")
axes[1,1].set_ylabel("Quantity")

plt.tight_layout()
fig.savefig(
    "visualization/categorical_analysis.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

#  TIME SERIES ANALYSIS

fig, axes=plt.subplots(2,2, figsize=(12,6))


yearly_revenue=(df.groupby("year")["revenue"].sum().sort_values(ascending=False))
sns.lineplot(
    x=yearly_revenue.index,
    y=yearly_revenue.values,
    ax=axes[0,0],
    marker="o"
)
axes[0,0].set_title("Yearly Revenue")
axes[0,0].set_xlabel("years")
axes[0,0].set_ylabel("revenue ")

monthly_revenue=(df.groupby("month_name")["revenue"].sum().sort_values(ascending=False))
sns.lineplot(
    x=monthly_revenue.index,
    y=monthly_revenue.values,
    ax=axes[0,1],
    marker="o"
    
)
axes[0,1].tick_params(axis="x", rotation=45)
axes[0,1].set_title("Monthly Revenue")
axes[0,1].set_xlabel("Month Name")
axes[0,1].set_ylabel("Revenue")

monthly_orders=(
    df.groupby("month_name")["order_id"]
    .nunique()
)
sns.lineplot(
    x=monthly_orders.index,
    y=monthly_orders.values,
    marker="o",
    ax=axes[1,0]
)
axes[1,0].tick_params(axis="x", rotation=45)
axes[1,0].set_title("Monthly Orders")
axes[1,0].set_xlabel("Month")
axes[1,0].set_ylabel("Orders")


# MONTHLY QUANTITY
monthly_quantity=(
    df.groupby("month_name")["quantity"]
    .sum().sort_values(ascending=False)
)
sns.lineplot(
    x=monthly_quantity.index,
    y=monthly_quantity.values,
    marker="o",
    ax=axes[1,1]
)
axes[1,1].tick_params(axis="x", rotation=45)
axes[1,1].set_title("Quantity Sold By Month")
axes[1,1].set_xlabel("Month Name")
axes[1,1].set_ylabel("Quantity Sold")

plt.tight_layout()
fig.savefig(
    "visualization/time_series.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()



# Relationship Analysis
fig,axes=plt.subplots(2,2, figsize=(12,6))

# Discount Vs Revenue
sns.regplot(
    data=df,
    x="discount",
    y="revenue",
    scatter_kws={"alpha": 0.4},
    ax=axes[0,0]
)
axes[0,0].set_title("Discount Vs Revenue")
axes[0,0].set_xlabel("Discount")
axes[0,0].set_ylabel("Revenue")


# Quantity vs revenue
sns.regplot(
    data=df,
    x="quantity",
    y="revenue",
    scatter_kws={"alpha": 0.4},
    ax=axes[0,1]
)
axes[0,1].set_title("Quantity Vs Revenue")
axes[0,1].set_xlabel("Quantity")
axes[0,1].set_ylabel("Revenue")

# Customer Rating Vs Revenue
sns.regplot(
    data=df,
    x="customer_rating",
    y="revenue",
    scatter_kws={"alpha": 0.4},
    ax=axes[1,0]
)
axes[1,0].set_title("Customer Rating Vs Revenue")
axes[1,0].set_xlabel("Customer Rating")
axes[1,0].set_ylabel("revenue")


# Delivery Days Vs Customer Rating
sns.regplot(
    data=df,
    x="delivery_days",
    y="customer_rating",
    scatter_kws={"alpha": 0.4},
    ax=axes[1,1]
)
axes[1,1].set_title("Delivery_Days Vs Customer_rating")
axes[1,1].set_xlabel("Delivery Days")
axes[1,1].set_label("Customer Rating")

plt.tight_layout()
fig.savefig(
    "visualization/relationship_analysis.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()



# BUsiness Focused Visaulization
# Average Order Value By Product Category
avg_order_value=(
    df.groupby("product_category")["revenue"]
    .mean().sort_values(ascending=False)
)

fig, axes=plt.subplots(2,2, figsize=(12,8))

sns.barplot(
    x=avg_order_value.index,
    y=avg_order_value.values,
    ax=axes[0,0]
)
axes[0,0].set_title("Average Order Value By Product Category")
axes[0,0].set_xlabel("Product Category")
axes[0,0].set_ylabel("Average Revenue")
for container in axes[0,0].containers:
    axes[0,0].bar_label(
        container,
        fmt="%.0f",
        padding=1
    )


# Average Customer Rating by Product Category
avg_rating=(
    df.groupby("product_category")["customer_rating"]
    .mean()
    .sort_values(ascending=False)
)
sns.barplot(
    x=avg_rating.index,
    y=avg_rating.values,
    ax=axes[0,1]
)
for container in axes[0,1].containers:
    axes[0,1].bar_label(
        container,
        fmt="%.2f",
        padding=1
    )
axes[0,1].set_title("Average Customer Rating by Category")
axes[0,1].set_xlabel("Product Category")
axes[0,1].set_ylabel("Average Rating")


# Average Delivery Days by Region
avg_days=(
    df.groupby("region")["delivery_days"]
    .mean()
    .sort_values(ascending=False)
)
sns.barplot(
    x=avg_days.index,
    y=avg_days.values,
    ax=axes[1,0]
)
for container in axes[1,0].containers:
    axes[1,0].bar_label(
        container,
        fmt="%.0f",
        padding=1
    )
axes[1,0].set_title("Average Delivery days by Region")
axes[1,0].set_xlabel("Region")
axes[1,0].set_ylabel("Average Delivery Days")


# Average revenue by region
avg_revenue=(
    df.groupby("region")["revenue"]
    .mean()
    .sort_values(ascending=False)
)
sns.barplot(
    x=avg_revenue.index,
    y=avg_revenue.values,
    ax=axes[1,1]
)
for container in axes[1,1].containers:
    axes[1,1].bar_label(
        container,
        fmt="%.0f",
        padding=1
    )
axes[1,1].set_title("Average Revenue by Region")
axes[1,1].set_xlabel("Region")
axes[1,1].set_ylabel("Average Revenue")

plt.tight_layout()
fig.savefig(
    "visualization/business_analysis.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show() 
