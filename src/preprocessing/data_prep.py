import pandas as pd

def format_data(product_df, customer_df, transactions_df):

    product_df = product_df.apply(lambda col: col.astype('category'))


    customer_df = customer_df.apply(lambda col: col.astype('category'))



    transactions_df['TRANSACTION_DATE'] = pd.to_datetime(transactions_df['TRANSACTION_DATE'])

    transactions_df['PK'] = transactions_df['PK'].astype('category')
    transactions_df['BUSINESS_SEGMENT'] = transactions_df['BUSINESS_SEGMENT'].astype('category')
    transactions_df['CUST_NO'] = transactions_df['CUST_NO'].astype('category')
    transactions_df['PRODUCT_CODE'] = transactions_df['PRODUCT_CODE'].astype('category')
    transactions_df['YYKURZANGA'] = transactions_df['YYKURZANGA'].astype('category')
    transactions_df['SALES_ORDER_NO'] = transactions_df['SALES_ORDER_NO'].astype('category')
    transactions_df['SALES_ORDER_ITEM_NO'] = transactions_df['SALES_ORDER_ITEM_NO'].astype('category')

    return product_df, customer_df, transactions_df





