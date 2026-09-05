import os
os.system("cls")

import pandas as pd
import numpy as np

file = pd.read_csv(r"C:\Users\Ajmal\OneDrive\Desktop\Python\01_Python Project\ShopKart_Orders_Raw.csv")

# print(file)

# print(file.shape)                              ## This tells you rows and columns.
# print(file.columns)                            ## This tells you all column names.
# file.info()                                    ## This tells you: column names, data types, number of non-null values
# print(file.isnull().sum())                     ## This tells you how many missing values are in each column.
# print(file.duplicated().sum())                 ## This tells you how many duplicate rows exist.
# print(file.describe())                         ## This gives you basic statistics for numerical columns.
# print(file["OrderDate"].head(10))              ## This gives you top 10 Order Date.
# print(file["OrderStatus"].value_counts())      ## This gives you one time order Status and is count how mane times came.
# print(file["PaymentMethod"].value_counts())    ## This gives you one time Payment method and is count how mane times came.


# duplicates = file[file.duplicated(keep=False)]                              ## This gives Show me rows that are completely duplicated.
# print(duplicates)

# print(file[file.duplicated("OrderID",keep=False)].sort_values("OrderID"))   ## Find every row where OrderID appears more than once.and sorts those duplicate records by OrderID

# # Cleaning Task 1 — Remove duplicates .......................

clean_file = file.drop_duplicates()

# print("Before:",file.shape)
# print("After:",clean_file.shape)
# print("duplicates: ",file.duplicated().sum())
# print("duplicates remaining: ",clean_file.duplicated().sum())


# # Cleaning Task 2 — Standardize Payment Methods ..................................

# print(clean_file)
# print(clean_file["PaymentMethod"].unique())
# print(clean_file["PaymentMethod"].value_counts(dropna=False))


clean_file["PaymentMethod"] = clean_file["PaymentMethod"].replace({
    "upi":"UPI",
    "debit card":"Debit Card",
    "cash":"Cash",
    "net banking":"Net Banking",
    "credit card":"Credit Card"
})

# # Cleaning Task 3 — OrderDate .....................................

# print(clean_file)
# print(clean_file["OrderDate"].dtype)

clean_file["OrderDate"] = pd.to_datetime(
    clean_file["OrderDate"],
    errors="coerce")

# print(clean_file["OrderDate"].isna().sum())
# print(clean_file["OrderDate"].dtype)

clean_file["OrderDate"] = pd.to_datetime(
    file.loc[clean_file.index,"OrderDate"],
    errors="coerce",
    format="mixed"
)

# print(clean_file["OrderDate"].isna().sum())
# print(clean_file["OrderDate"].dtype)

# # Cleaning Task 3.1 — Investigate the 5 invalid dates ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

# print(clean_file[clean_file["OrderDate"].isna()])
# print(clean_file[clean_file["OrderDate"].isna()]["OrderID"])


# # Cleaning Task 4 — Missing Values .........................................................

# print(clean_file.isnull().sum())
# print(clean_file[clean_file["CustomerName"].isna()])
# print(clean_file[clean_file["City"].isna()])
# print(
#     clean_file[clean_file["CustomerID"]=="C1696"]
#     [["CustomerID","CustomerName"]]
# )

# # Cleaning Task 4A — Recover missing CustomerName ,,,,,

name_check = clean_file.groupby("CustomerID")["CustomerName"].nunique()
# print(name_check[name_check > 1])

# print(name_check.value_counts())

# # Task 4B — Fill the missing CustomerName ,,,,,

customer_name_map = clean_file.groupby("CustomerID")["CustomerName"].first()

clean_file["CustomerName"] = clean_file["CustomerName"].fillna(
    clean_file["CustomerID"].map(customer_name_map)
)

# print(clean_file["CustomerName"].isna().sum())

# Task 4B — Missing City ,,,,,

# print(clean_file[clean_file["City"].isna()][["OrderID","CustomerID","CustomerName","City","State"]].head(10))

# print(
#     clean_file[clean_file["City"].isna()]
#     ["State"]
#     .value_counts(dropna=False)
# )

# print(clean_file.groupby("State")["City"].unique())

# # Task 4B — Step 1: Remove extra spaces from City ,,,,,

clean_file["City"] = clean_file["City"].str.strip()

# print(clean_file.groupby("State")["City"].unique())

# # Task 4B — Fill only the safe cities ,,,,,
city_map = {
    "Delhi": "Delhi",
    "Gujarat": "Ahmedabad",
    "Haryana": "Gurugram",
    "Karnataka": "Bengaluru",
    "Rajasthan": "Jaipur",
    "Tamil Nadu": "Chennai",
    "Telangana": "Hyderabad",
    "West Bengal": "Kolkata"
}

clean_file["City"] = clean_file["City"].fillna(
    clean_file["State"].map(city_map)
)

# print(clean_file["City"].isna().sum())

# print(
#     clean_file[clean_file["City"].isna()]
#     [["OrderID","CustomerID","CustomerName","City","State"]]
# )

# print(
#     clean_file[clean_file["City"].isna()]
#     ["CustomerID"]
#     .unique()
# )

missing_city_customers = clean_file.loc[
    clean_file["City"].isna(),"CustomerID"
].unique()

# print(
#     clean_file[
#         clean_file["CustomerID"].isin(missing_city_customers)
#     ][["CustomerID","CustomerName","City","State"]]
#     .sort_values("CustomerID")
# )

# # Next: Missing PaymentMethod ...........................................................

# print(
#     clean_file[clean_file["PaymentMethod"].isna()]
#     [["OrderID","CustomerID","CustomerName","PaymentMethod"]]
# )

# # Step 1 — Get the customers with missing payment methods ,,,,

missing_payment_customers = clean_file.loc[
    clean_file["PaymentMethod"].isna(),"CustomerID"
].unique()

# print(missing_city_customers)

# # Step 2 — Check those customers' other orders ,,,,

# print(
#     clean_file[
#         clean_file["CustomerID"].isin(missing_city_customers)
#     ][["CustomerID","CustomerName","PaymentMethod"]]
#     .sort_values("CustomerName")
# )

# print(clean_file["PaymentMethod"].isna().sum())

# # replacing NaN with "Unknown" after keeping the original information ,,,

clean_file["PaymentMethod"] = clean_file["PaymentMethod"].fillna("Unknown")

# print(clean_file["PaymentMethod"].value_counts(dropna=False))

# # Task 4C — Missing Rating ,,,,,,

# print(clean_file[clean_file["Rating"].isna()]
#     [["OrderID","CustomerID","CustomerName","PaymentMethod","Rating"]]
# )

# print(
#     clean_file.loc[
#         clean_file["Rating"].isna(),
#         "OrderStatus"
#     ].value_counts()
# )

# print(clean_file.isna().sum())

# print(clean_file.shape)

# # Cleaning Task 5 — Check Numeric Data .......................................

# # Step 5A — Quantity ,,,,,
# print(clean_file["Quantity"].describe())

# print(clean_file[clean_file["Quantity"] <= 0])

# print(clean_file[clean_file["Quantity"] <= 0][[
#     "OrderID",
#     "Product",
#     "Quantity",
#     "UnitPrice",
#     "Discount",
#     "Revenue",
#     "Cost",
#     "Profit",
#     "OrderStatus"
# ]])

clean_file = clean_file[clean_file["Quantity"] > 0]

# print(clean_file.shape)
# print(clean_file["Quantity"].min())
# print((clean_file["Quantity"] <= 0).sum())

# # Cleaning Task 6 — Check Revenue ...............................

# # Step 1: Find negative Revenue ,,,,,
# print(clean_file[clean_file["Revenue"] < 0][[
#     "OrderID",
#     "Product",
#     "Quantity",
#     "UnitPrice",
#     "Discount",
#     "Revenue",
#     "Cost",
#     "Profit",
#     "OrderStatus"
# ]])

# print((clean_file["Revenue"] <= 0).sum())

# # Step 2 — Remove negative Revenue ,,,,,
clean_file = clean_file[clean_file["Revenue"] >= 0]

# print(clean_file.shape)
# print(clean_file["Revenue"].min())
# print((clean_file["Revenue"] < 0).sum())

# Next: Revenue, Cost & Profit consistency

# check_Profit = clean_file["Revenue"] - clean_file["Cost"]

# print((check_Profit != clean_file["Profit"]).sum())

# print(clean_file[check_Profit != clean_file["Profit"]][[
#     "OrderID",
#     "Product",
#     "Quantity",
#     "UnitPrice",
#     "Discount",
#     "Revenue",
#     "Cost",
#     "Profit",
#     "OrderStatus"
# ]].head(10))

# # Next Cleaning Task — Check Discount ............................................

# print(clean_file["Discount"].describe())
# print(clean_file["Discount"].unique())

# print(clean_file[
#     (clean_file["Discount"] < 0) |
#     (clean_file["Discount"] > 1)
# ][["OrderID","Discount","Revenue","Profit"]])

# # Next Cleaning Task — Rating ...................................................

# print(clean_file["Rating"].describe())
# print(clean_file["Rating"].unique())

# print(clean_file[
#     (clean_file["Rating"] < 1) |
#     (clean_file["Rating"] > 5)
# ][["OrderID","CustomerID","Rating","OrderStatus"]])

clean_file.loc[clean_file["Rating"] > 5, "Rating"] = np.nan

# print(clean_file["Rating"].unique())
# print(clean_file["Rating"].isna().sum())

# # Next Task — Check UnitPrice and Cost ...........................................

# print(clean_file["UnitPrice"].describe())
# print(clean_file["Cost"].describe())

# print(clean_file[
#     (clean_file["UnitPrice"] <= 0) |
#     (clean_file["Cost"] <= 0)
# ][[
#     "OrderID",
#     "Product",
#     "Quantity",
#     "UnitPrice",
#     "Cost",
#     "Revenue",
#     "Profit"
# ]])

# print(
#     ((clean_file["Cost"] <= 0) |
#     (clean_file["UnitPrice"] <= 0)).sum())

# # Next Task — Check Revenue Calculation .........................................

# expected_revenue = (
#     clean_file["Quantity"]
#     * clean_file["UnitPrice"]
#     * (1 - clean_file["Discount"])
# )

# revenue_difference = clean_file["Revenue"] - expected_revenue

# print(revenue_difference.abs().max())

# # Next Task — Check OrderStatus ................................................

# print(clean_file["OrderStatus"].value_counts(dropna=False))
# print(clean_file["OrderStatus"].unique())

# # Next Task — Check SalesChannel ..................................................

# print(clean_file["SalesChannel"].value_counts(dropna=False))
# print(clean_file["SalesChannel"].unique())

# # Next Task — Check City carefully ....................................................

# print(clean_file["City"].value_counts(dropna=False))
# print(clean_file["City"].unique())

# # Next Task — Check State ...............................................................

# print(clean_file["State"].value_counts(dropna=False))
# print(clean_file["State"].unique())
# print(clean_file["State"].isna().sum())

# # Next Task — Product & Category ........................................................

# print(clean_file["Product"].value_counts(dropna=False))
# print(clean_file["Category"].value_counts(dropna=False))
# print(clean_file[["Product", "Category"]].isna().sum())

# # Next Task — PaymentMethod final check ...................................................

# print(clean_file["PaymentMethod"].value_counts(dropna=False))
# print(clean_file["PaymentMethod"].isna().sum())

# # Final Missing-Value Audit ..............................................................

# print(clean_file.isna().sum())
# print(clean_file.shape)

# # Final Data Quality Check ...................................................................

# print(clean_file["OrderID"].duplicated().sum())
# print(clean_file["OrderID"].nunique())

# Step 1 — Find the duplicate OrderID ,,,,,
# duplicate_orders = clean_file[
#     clean_file["OrderID"].duplicated(keep=False)
# ]

# print(duplicate_orders)

# # Step 2 — Compare them ,,,,,

# print(duplicate_orders.T)


# Step 3 — Remove the duplicate OrderID ,,,,,

clean_file = clean_file.drop_duplicates(subset="OrderID", keep="first")

# print(clean_file.shape)
# print(clean_file["OrderID"].duplicated().sum())
# print(clean_file["OrderID"].nunique())

# # Next step: Final data-quality audit ........................

# print(clean_file.isnull().sum())


# # Why are we keeping them?
# # 1. OrderDate → 5 missing/invalid
# # We already identified these as invalid dates. We don't know the real dates, so we should not invent them.
# # 2. City → 20 missing
# # These are from Maharashtra and Uttar Pradesh, where there are multiple possible cities. CustomerID also wasn't reliable enough to determine the correct city.
# # So we leave them as NaN.
# # 3. Rating → 68 missing
# # These are either originally missing or invalid Rating = 6 values that we converted to NaN.
# # A missing customer rating does not mean the rating was 3, 4, etc. So we don't make up a rating.

# # Next step: Check the final data types .......................................

# print(clean_file.dtypes)

# # Next task: Check for text inconsistencies .....................................

# print(clean_file["City"].unique())
# print(clean_file["PaymentMethod"].unique())
# print(clean_file["OrderStatus"].unique())

# # Next task: Final numerical validation  .........................................

# print(clean_file[clean_file["Quantity"] <= 0])
# print(clean_file[clean_file["Revenue"] < 0])
# print(clean_file[clean_file["Cost"] <= 0])
# print(clean_file[clean_file["UnitPrice"] <= 0])

# # Next: Check Discount and Rating

# print(clean_file[clean_file["Discount"] < 0])
# print(clean_file[clean_file["Discount"] > 1])
# print(clean_file[clean_file["Rating"] < 1])
# print(clean_file[clean_file["Rating"] > 5])

# # Final validation — business calculations ...................................
# print("Total rows:", len(clean_file))
# print("Total columns:", len(clean_file.columns))
# print("Duplicate rows:", clean_file.duplicated().sum())
# print("Duplicate OrderIDs:", clean_file["OrderID"].duplicated().sum())
# print("Total missing values:", clean_file.isnull().sum().sum())

# #  ....................................  cleaning phase is complete  ......................................................

# Next task: Save the cleaned dataset ..................

clean_file.to_csv(
    r"C:\Users\Ajmal\OneDrive\Desktop\Python\01_Python Project\ShopKart_Orders_Cleaned.csv",
    index=False
)

print(os.path.exists(
    r"C:\Users\Ajmal\OneDrive\Desktop\Python\01_Python Project\ShopKart_Orders_Cleaned.csv"
))