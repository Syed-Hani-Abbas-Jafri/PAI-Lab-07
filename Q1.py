import pandas as pd
import numpy as np

np.random.seed(42)
numRows = 150

data = {
    'customerId': [f'CUST_{1000 + i}' if i % 12 != 0 else np.nan for i in range(numRows)],
    'joinDate': pd.date_range(start='2023-01-01', periods=numRows, freq='2D'),
    'age': [np.random.randint(18, 65) if i % 7 != 0 else np.nan for i in range(numRows)],
    'gender': np.random.choice(['Male', 'Female', 'Other'], size=numRows, p=[0.48, 0.48, 0.04]),
    'city': np.random.choice(['Karachi', 'Lahore', 'Islamabad', 'Peshawar'], size=numRows),
    'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books'], size=numRows),
    'orderCount': np.random.randint(1, 30, size=numRows),
    'totalSpent': [round(np.random.uniform(500, 50000), 2) if i % 9 != 0 else np.nan for i in range(numRows)],
    'isVip': np.random.choice([True, False], size=numRows, p=[0.2, 0.8])
}

df = pd.DataFrame(data)

print(df.shape)
print(df.dtypes)
print(df.isna().sum())

df.dropna(subset=['customerId'], inplace=True)

df['age'] = df['age'].fillna(df['age'].median())
df['totalSpent'] = df['totalSpent'].fillna(df['totalSpent'].mean())

df['joinDate'] = pd.to_datetime(df['joinDate'])
df['joinYear'] = df['joinDate'].dt.year
df['joinMonth'] = df['joinDate'].dt.month_name()

df['avgOrderValue'] = df['totalSpent'] / df['orderCount']

df['highValueCustomer'] = df['avgOrderValue'] > 2500

citySummary = df.groupby('city').agg(
    totalCustomers=('customerId', 'count'),
    avgTotalSpent=('totalSpent', 'mean'),
    maxOrderCount=('orderCount', 'max')
)
print(citySummary)

pivotTable = pd.pivot_table(df, index='category', columns='isVip', values='totalSpent', aggfunc='sum')
print(pivotTable)

topFive = df[df['category'].isin(['Electronics', 'Clothing'])].sort_values('totalSpent', ascending=False).head(5)
print(topFive)

vipCities = df[(df['isVip']) & (df['city'].isin(['Karachi', 'Lahore']))]
print(vipCities.groupby('city')['orderCount'].mean())
# Insight 1: Lahore has the highest number of customers (41), while Karachi has the highest average Total_Spent (27379.05).
# Insight 2: Books has the highest total revenue (1003473.64), followed by Electronics (997357.00), while Home has the lowest revenue (614022.34).
# Insight 3: VIP customers in Lahore have a higher average Order_Count (17.43) than VIP customers in Karachi (16.29).

#Output: (150, 9)
# customerId               str
# joinDate      datetime64[us]
# age                  float64
# gender                   str
# city                     str
# category                 str
# orderCount             int32
# totalSpent           float64
# isVip                   bool
# dtype: object
# customerId    13
# joinDate       0
# age           22
# gender         0
# city           0
# category       0
# orderCount     0
# totalSpent    17
# isVip          0
# dtype: int64
# C:\Users\Gaming Laptop House\Downloads\files (5)\prac123456.py:25: Pandas4Warning: The inplace keyword in DataFrame.dropna is deprecated and will be removed in a future version (PDEP-8).
# See https://pandas.pydata.org/docs/dev/whatsnew/v3.1.0.html#deprecation-inplace for more details.
#   df.dropna(subset=['customerId'], inplace=True)
#            totalCustomers  avgTotalSpent  maxOrderCount
# city                                                   
# Islamabad              30   24533.950045             28
# Karachi                29   27379.049851             29
# Lahore                 41   25955.630521             29
# Peshawar               37   21828.029613             29
# isVip               False         True 
# category                               
# Books        773581.96568  229891.67000
# Clothing     687625.76136   99350.15784
# Electronics  806814.38568  190542.61000
# Home         439472.59568  174549.74784
#     customerId   joinDate   age  gender       city  ...  isVip  joinYear joinMonth  avgOrderValue  highValueCustomer
# 103  CUST_1103 2023-07-26  62.0  Female    Karachi  ...   True      2023      July    7004.700000               True
# 17   CUST_1017 2023-02-04  41.0    Male  Islamabad  ...  False      2023  February   15985.256667               True
# 40   CUST_1040 2023-03-22  64.0  Female   Peshawar  ...  False      2023     March    2476.648947              False
# 43   CUST_1043 2023-03-28  20.0    Male  Islamabad  ...  False      2023     March    2874.952500               True
# 4    CUST_1004 2023-01-09  60.0  Female    Karachi  ...  False      2023   January   11499.057500               True

# [5 rows x 13 columns]
# city
# Karachi    16.285714
# Lahore     17.428571
# Name: orderCount, dtype: float64
