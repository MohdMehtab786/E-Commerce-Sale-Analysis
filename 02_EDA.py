# ---------------------------EDA--------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_excel("Cleaned_data.xlsx")
print(df.shape)
print(df.dtypes)
print(df.columns.tolist())

        
# Categorical Summary

categorical_columns = [
    "product_category",
    "region",
    "payment_method",
    "month_name",
    "day_name",
    "order_value_category",
    "delivery_category",
    "rating_category"
]

# Store value counts of all categorical columns
categorical_results = []

for column in categorical_columns:

    print(f"\n{column}:")
    
    counts = df[column].value_counts()

    print(counts)

    for value, count in counts.items():
        categorical_results.append({
            "Column": column,
            "Value": value,
            "Count": count
        })


# Convert results into DataFrame
categorical_data = pd.DataFrame(categorical_results)

print("\nCategorical Summary:")
print(categorical_data)


# Save to Excel
with pd.ExcelWriter(
    "EDA_result.xlsx",
    engine="openpyxl"
) as writer:

    categorical_data.to_excel(
        writer,
        sheet_name="EDA",
        index=False
    )

# Overall Sales Performance

# Total Revenue
total_revenue=df["revenue"].sum().round(2)
print("\nTotal Revenue:")
print(total_revenue)

# Total Orders

total_orders=df["order_id"].nunique()
print("\nTotal Orders:")
print(total_orders)


# Total quantity sold
total_quantity=df["quantity"].sum()
print("\nTotal Quantity Sold:")
print(total_quantity)


# Average Order Value
average_order_value=(total_revenue/ total_orders).round(2)
print("\nAverage Order Value;")
print(average_order_value)


# Average Quantity Per Order
average_quantity_per_order=(total_quantity/total_orders)
print("\nAverage Order per Order:")
print(average_quantity_per_order)

# Average Discount
average_discount=(df["discount"].mean())
print("\nAverage Discount:")
print((average_discount*100).round(2), "%")


# Average Customer Rating
average_rating=df["customer_rating"].mean().round(2)
print("\nAverage Customer Rating:")
print(average_rating)


average_delivery_days=df["delivery_days"].mean()
print("\nAverage Delivery Days:")
print(average_delivery_days)


kpi_data=pd.DataFrame({
    "Metrics":[
        "Total Revenue",
         
        "Total Orders",
        "Total Quantity",
        "Average Order Value",
        "Average Quantity Per Order",
        "Averager Discount",
        "Average Custoomer Rating",
        "Average Delivery Days"
    ],
    "Value":[
        total_revenue,
        
        total_orders,
        total_quantity,
        average_order_value,
        average_quantity_per_order,
        average_discount,
        average_rating,
        average_delivery_days
    ]
})

with pd.ExcelWriter("EDA_result.xlsx", engine="openpyxl", mode="a",
                    if_sheet_exists="overlay") as writer:
    kpi_data.to_excel(
        writer,
        sheet_name="EDA",
        index=False,
        startcol=8
    )

# categorical Analysis

# Revenue by product category
revenue_by_product=(df.groupby("product_category")["revenue"].sum())
print("\n Revenue By Product Category:")
print(revenue_by_product)

# Revenue By Region.
rev_by_region=(df.groupby("region")["revenue"].sum().sort_values(ascending=False))
print("\nRevenue By Region:")
print(rev_by_region)

# Revenue By Payemnt Method.
rev_by_paymentmethod=(df.groupby("payment_method")["revenue"].sum().sort_values(ascending=False))
print("\nRevenue By Payment_method:")
print(rev_by_paymentmethod)

# Revenue By Year
rev_by_year=(
    df.groupby("year")["revenue"]
    .sum()
    .sort_values(ascending=False)
)
print("\nRevenue by Year:")
print(rev_by_year)


# Revenue By Month Name
rev_by_month_name=(
    df.groupby("month_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
)
print("\nRevenue By Month Name:")
print(rev_by_month_name)


# Revenue By Day_Name
rev_by_day_name=(
    df.groupby("day_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\n Revenue By Day Name:")
print(rev_by_day_name)

# Quarterly Revenue
quarterly_rev=(
    df.groupby("quarter")["revenue"]
    .sum()
    .sort_values(ascending=False)
)
print("\nQuarterly Revenue")
print(quarterly_rev)

# Revenue By Rating
rev_by_rating_category=(
    df.groupby("rating_category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)
print("\nRevenue By Rating:")
print(rev_by_rating_category)

order_by_years=(df.groupby("year")["order_id"].nunique())
print(order_by_years)


with pd.ExcelWriter("EDA_result.xlsx", engine="openpyxl", mode="a",
                    if_sheet_exists="overlay")as writer:
    startrow=0
    revenue_by_product.to_excel (
        writer,
        sheet_name="EDA2",
        startcol=0,
        header=["Revenue"],
        
        startrow=startrow
    )
    startrow+=len(revenue_by_product)+3
    rev_by_region.to_excel(
        writer,
        sheet_name="EDA2",
        header=["Revenue"],
        startrow=startrow
    )
    rev_by_paymentmethod.to_excel(
        writer,
        sheet_name="EDA2",
        startcol=3,
        
        header=["Revenue"]
    )
    rev_by_year.to_excel(
        writer,
        sheet_name="EDA2",
        header=["Revenue"],
        startcol=6
    )
    rev_by_month_name.to_excel(
        writer,
        sheet_name="EDA2",
        header=["Revenue"],
        startrow=5,
        startcol=3
    )
    rev_by_day_name.to_excel(
        writer,
        sheet_name="EDA2",
        header=["Revenue"],
        startcol=6,
        startrow=8
    )
    quarterly_rev.to_excel(
        writer,
        sheet_name="EDA2",
        startrow=12,
        startcol=0
    )
    rev_by_rating_category.to_excel(
        writer,
        sheet_name="EDA2",
        startrow=12,
        startcol=9
    )
    order_by_years.to_excel(
        writer,
        sheet_name="EDA2",
        startcol=9,
        startrow=18
    )



# Numerical Analysis

# Correlation mtarix
numerical_columns=[
    "quantity",
    "unit_price",
    "discount",
    "delivery_days",
    "customer_rating",
    "revenue",
    "discount_amount"
]
correlation_matrix=df[numerical_columns].corr()
print("\nCorrelation Matrix:")
print(correlation_matrix)
corr=pd.DataFrame(correlation_matrix)


# strong correlation
# correlation_pair=correlation_matrix.unstack()
# correlation_pair=correlation_pair[
#     correlation_pair!=1
# ]
# correlation_pair=correlation_pair.abs().sort_values(ascending=False)
# print("\nStrongest Correlation")
# print(correlation_pair.head(20))

with pd.ExcelWriter("EDA_result.xlsx", engine="openpyxl", mode="a",
                    if_sheet_exists="overlay")as writer:
    corr.to_excel(
        writer,
        sheet_name="EDA2",
        startcol=15
    )