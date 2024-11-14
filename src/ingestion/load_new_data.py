import pandas as pd

product_path = 'C:/Users/cagri/Downloads/Case Study - Part 2/product_master_anonymised.csv'
customer_path = 'C:/Users/cagri/Downloads/Case Study - Part 2/customer_master_anonymised.csv'
transactions_path = 'C:/Users/cagri/Downloads/Case Study - Part 2/transactions_anonymised.csv'




product_df=pd.read_csv(product_path)

print(product_df,product_df.dtypes)
