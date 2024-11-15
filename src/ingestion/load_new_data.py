import pandas as pd

def load_new_data(product_path, customer_path, transactions_path):
    transactions_df = pd.read_csv(transactions_path)
    customer_df = pd.read_csv(customer_path)
    product_df = pd.read_csv(product_path)
    return product_df, customer_df, transactions_df



