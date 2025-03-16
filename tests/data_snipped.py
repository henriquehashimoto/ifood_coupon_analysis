

import pandas as pd


df_ab_test = pd.read_parquet("./data/processed/ab_test.parquet")
df_consumers = pd.read_parquet("./data/processed/consumers_processed.parquet")
df_orders = pd.read_parquet("./data/processed/orders_processed.parquet")
df_restaurants = pd.read_parquet("./data/processed/restaurants_processed.parquet")


print(df_ab_test.head())
print(df_consumers.head())
print(df_orders.head())
print(df_restaurants.head())
