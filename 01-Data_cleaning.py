import pandas as pd
import numpy as np


#                             DATA UNDERSTANDING AND VALIDATION


df=pd.read_csv("raw_data.csv")
print(df.head())
print(df.shape)
print(df.info())
print(df.describe())

print(df.isna().sum())

print(df.duplicated().sum())

print(df["order_id"].nunique())
print(df["customer_id"].nunique())

# check category column 
print(df["product_category"].unique())

# check region
print(df["region"].unique())

# check quantity
quan_check=(df["quantity"]<=0).sum()
print("\nSuspicious quantity count:", quan_check)
print(df["quantity"].min())
print(df["quantity"].max())

# check unit_price
print(df["unit_price"].min())
print(df["unit_price"].max())

# check discount
print(df["discount"].min())
print(df["discount"].max())

# check payment method
print(df["payment_method"].unique())

# check delivery days
print("\nDelivery_days Validation:")
print(df["delivery_days"].min())
print(df["delivery_days"].max())

#check customer rating
print("\n Customer rating validation:") 
print(df["customer_rating"].min())
print(df["customer_rating"].max())

# validate date
print(df["order_date"].dtype)
print(df["order_date"].min())
print(df["order_date"].max())

# check Revenue
print("\n Revenue check:")
print(df["revenue"].min())
print(df["revenue"].max())

# Revenue Validation
df["revenue2"]=(df["quantity"]*df["unit_price"]*(1-df["discount"]))
print(df["revenue2"].head(5))

revenue_match=df["revenue"].equals(df["revenue"])
print("Revenue matched:", revenue_match)

df.drop(columns=["revenue2"], inplace=True) 


#------------------------DATA CLEANING------------------------

clean_df=df.copy()

print(clean_df.shape)
print(clean_df.dtypes)

# Standardize Column Nammes
clean_df.columns=(
    clean_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Date Data Type Change
clean_df["order_date"]=pd.to_datetime(
    clean_df["order_date"],
    errors="coerce"
)


# categorical data cleaning.
#  Remove unnecessary spaces.
categorical_columns=[
    "product_category",
    "region",
    "payment_method"
]

for column in categorical_columns:
    clean_df[column]=(
        clean_df[column]
        .str.strip()
        .str.capitalize()
        .str.replace("Cod", "COD")
    )

# Numerical Data Cleaning.

numerical_columns=[
    "quantity",
    "unit_price",
    "discount",
    "delivery_days",
    "customer_rating",
    "revenue"
]

for column in numerical_columns:
    print(
        f"{column}: "
        f"Min= {clean_df[column].min()},"
        f"Max= {clean_df[column].max()}"
    )

# Date Cleaning
today=pd.Timestamp.today().normalize()
future_date=clean_df[clean_df["order_date"]>today]
print("\nrows with future dates:")
print(len(future_date))


# -------------------------------------------FEATURE ENGINEERING------------------------------------
#  The dataset has 5000 rows and 12 columns but 3308 rows contains future dates as today.
# So I excluded these rows from my analysis.

analysis_df=(clean_df[clean_df["order_date"]<=today].copy())
print(analysis_df["order_id"].nunique())
print(analysis_df["customer_id"].nunique())

# Date Feature
analysis_df["year"]=analysis_df["order_date"].dt.year
analysis_df["month_name"]=analysis_df["order_date"].dt.month_name()
analysis_df["day_name"]=analysis_df["order_date"].dt.day_name()
analysis_df["quarter"]=analysis_df["order_date"].dt.quarter
analysis_df["is_weekend"]=analysis_df["order_date"].dt.day_of_week>=5

print(analysis_df.shape)


# Sales And Discount Feature.
# Create Gross sales.
analysis_df["gross_sales"]=(analysis_df["quantity"] * analysis_df["unit_price"])

# Discount Amount
analysis_df["discount_amount"]=analysis_df["discount"]*analysis_df["gross_sales"]



# -------------Order Value Category----------
# categorize column based on their revenue.
analysis_df["order_value_category"]=pd.cut(
    analysis_df["revenue"],
    bins=[-np.inf, 500, 1500, np.inf],
    labels=["Low Value", "Medium Value", "High Value"]
)
print(analysis_df["order_value_category"].value_counts())

# Total Order per custumer
customer_order_count=(
    analysis_df.groupby("customer_id")["order_id"]
    .count()
    .reset_index(name='total_order')
)
print(customer_order_count.head(10))


# TotalRevenue per customer
customer_revenue=(
    analysis_df.groupby("customer_id")["revenue"]
    .sum()
    .reset_index(name="total_customer_revenue")
)
print(customer_revenue.head())

# combine the two customer features
customer_features=customer_order_count.merge(
    customer_revenue,
    on="customer_id",
    how="left"
)
print(customer_features.head(10))

analysis_df=analysis_df.merge(
    customer_features,
    on="customer_id",
    how="left"
)

# customer value features

analysis_df["customer_avg_order_value"]=(
    analysis_df["total_customer_revenue"]/
    analysis_df["total_order"]
)

print(
    analysis_df[[
        "customer_id",
        "total_order",
        "total_customer_revenue",
        "customer_avg_order_value"
    ]].head(20)
)



#  product feature
# revenue by product category

category_revenue=(
    analysis_df.groupby("product_category")["revenue"]
    .sum()
    .reset_index(name="category_total_revenue")
)


# number of order by category
category_order=(
    analysis_df.groupby("product_category")["order_id"]
    .count()
    .reset_index(name="category_order_count")
)


# combine category features
category_features=category_revenue.merge(
    category_order,
    on="product_category",
    how="left"
)

# delivery performance features
# Delivery category
analysis_df["delivery_category"]=pd.cut(
    analysis_df["delivery_days"],
    bins=[0, 3, 6, np.inf],
    labels=["Fast", "Standard", "slow"]
)

# customer rating features
# Rating category
analysis_df["rating_category"]=pd.cut(
    analysis_df["customer_rating"],
    bins=[0, 2, 3, 5],
    labels=["Poor", "Average", "Good"]
)

print(analysis_df.shape)
print(clean_df.shape)

analysis_df.to_excel("Cleaned_data.xlsx", index=False)





 
