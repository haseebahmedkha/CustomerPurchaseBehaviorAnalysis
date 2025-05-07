import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import pymysql
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import mysql.connector



#connecting to the database
username = 'root'
password = quote_plus('Chodrykhan@880')
host = 'localhost'
port = 3306
database = 'customer_behavior'


# Check if the database exists
if database == 'customer_behavior':
    # Create a connection to the MySQL database
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')
    print("Connected to the database successfully.")
else:
    print("Database not found. Please check the database name.")


# Fetching data from the database
query = "select * from customer_orders;"
df = pd.read_sql(query, engine)
print(df.head())



#cleaning the data
df.dropna(inplace=True)
df['order_date'] = pd.to_datetime(df['order_date'])
df.isnull().sum()


# top 5 products 
top_5_products = df['product_name'].value_counts().head(5)
print("Top 5 products:\n", top_5_products)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_5_products.index, y=top_5_products.values, palette='viridis')
plt.title('Top 5 Products Sold')
plt.xlabel('Product Name')
plt.ylabel('Number of Sales')
plt.tight_layout()
plt.savefig('top_5_products.png')
plt.show()
plt.close()




# daily sales trend
df['order_date'] = df['order_date'].dt.date
daily_sales = df.groupby('order_date')['price'].sum().reset_index()
print("Daily sales trend:\n", daily_sales)

plt.figure(figsize=(10, 6))
plt.plot(daily_sales['order_date'], daily_sales['price'], marker='o', linestyle='-', color='b')
plt.title('Daily Sales Trend')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.savefig('daily_sales_trend.png')
plt.show()
plt.close()


# top customers by spending
topcustomers = df.groupby('customer_id')['price'].sum().reset_index()
print("Top customers by spending:\n", topcustomers.sort_values(by='price', ascending=False))

plt.figure(figsize=(10, 6))
sns.catplot(x='customer_id', y='price', data=topcustomers.sort_values(by='price', ascending=False).head(10), kind='bar', palette='viridis')
plt.title('Top 10 Customers by Spending')
plt.xlabel('Customer ID')
plt.ylabel('Total Spending')
plt.tight_layout()
plt.savefig('top_customers.png')
plt.show()
plt.close()


