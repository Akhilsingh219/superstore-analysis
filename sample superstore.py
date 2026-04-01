import pandas as pd
import numpy as  np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv(
    r"C:\Users\WMG\Downloads\archive\Sample - Superstore.csv",
    encoding='latin1' )

##  data  reading:
print("File loaded successfully ")
print(data.head(10))
print(data.info())

print(data.shape)
print(data.isnull().sum())


 # data cleaning

data.columns =data.columns.str.strip().str.lower().str.replace(" ","_")

data["order_date"] = pd.to_datetime(data["order_date"])

data['ship_date'] = pd.to_datetime(data['ship_date'])

     # Remove depulicates

data =data.drop_duplicates()


print("\n  Data Cleaned Proper")

#  Total sales and profit

print("---Total sales--- ",data['sales'].sum())
print("---Total profit--- ",data['profit'].sum())


# Sales by Category

category_sales = data.groupby('category')['sales'].sum()
print(category_sales)

# create new column

data['order_year'] = data["order_date"].dt.year
data["order_month"] = data["order_date"].dt.month
data["shipping_days"] = (data["ship_date"] - data["order_date"]).dt.days

print(data[["order_year","order_month","shipping_days"]])


## Top 5 sales by product name

Top_sales = data.groupby('product_name')['sales'].sum().sort_values(ascending=False).head(5)

print(" Top_sales :" ,Top_sales)

print("="*50)
print("Executive Summary")
print("="*50)
print("Total Sales : ", round (data['sales'].sum(),2))
print("Total profit : ", round (data['profit'].sum(),2))
print("Total order : ", data['order_id'].nunique())
print("Best category :",data.groupby('category')['sales'].sum().idxmax())
print("Best Region :",data.groupby('region')['profit'].sum().idxmax())
print("="*50)






##  Visualization

# 1. Sales by Category (Bar)

plt.figure(figsize=(8, 5))
category_sales = data.groupby('category')['sales'].sum()
plt.bar(category_sales.index, category_sales.values,
        color=['steelblue','orange','green'])
plt.title("Sales by Category")
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.savefig("chart1_category_sales.png")
plt.show()

# 2. Sales Share by Category (Pie)
plt.figure(figsize=(6, 6))
plt.pie(category_sales, labels=category_sales.index,
        autopct='%1.1f%%', colors=['steelblue','orange','green'])
plt.title("Sales Share by Category")
plt.savefig("chart2_pie.png")
plt.show()

# 3. Yearly Sales Trend (Line)
plt.figure(figsize=(8, 5))
data.groupby('order_year')['sales'].sum().plot(marker='o', color='steelblue')
plt.title("Yearly Sales Trend")
plt.xlabel("Year")
plt.ylabel("Total Sales")
plt.savefig("chart3_yearly_trend.png")
plt.show()

# 4. Region-wise Total Sales (Seaborn)
plt.figure(figsize=(8, 5))
region_sales = data.groupby('region')['sales'].sum().reset_index()
sns.barplot(x='region', y='sales', data=region_sales, palette='Set2')
plt.title("Region-wise Total Sales")
plt.savefig("chart4_region_sales.png")
plt.show()






##  Save Clean Data

data.to_csv("superstore_cleaned.csv", index=False)
print("File Saved!")




