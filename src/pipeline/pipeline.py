import config.config
from src.ingestion.load_new_data import load_new_data
from src.preprocessing.data_prep import format_data
import pandas as pd

loaded_data_array=load_new_data(config.config.PRODUCT_PATH, config.config.CUSTOMER_PATH, config.config.TRANSACTIONS_PATH)

product_df=loaded_data_array[0]
customer_df=loaded_data_array[1]
transactions_df=loaded_data_array[2]

format_data(product_df, customer_df, transactions_df)

transactions_df=transactions_df[transactions_df['LLP_GC_ORIG']!=0]

transactions_df['DISCOUNT_AMOUNT'] = transactions_df['LLP_GC_ORIG'] - transactions_df['REVENUE_GC_ORIG']
transactions_df['DISCOUNT_RATE'] = transactions_df['DISCOUNT_AMOUNT']/transactions_df['LLP_GC_ORIG']

# TEST print(transactions_df.isna().sum())

print((transactions_df==0).sum())
print(transactions_df.isna().sum())
#print(transactions_df.loc[:,'DISCOUNT_RATE'].mean())
# TEST print(transactions_df['LLP_LC_ORIG'] - (transactions_df['LOCAL_LIST_PRICE'] * transactions_df['QUANTITY']))


product_df.rename(columns={'FY': 'FISCAL_YEAR'}, inplace=True )

merged_main_df = pd.merge(transactions_df, product_df, on=['FISCAL_YEAR', 'PRODUCT_CODE'], how='inner')

merged_main_df = pd.merge(merged_main_df, customer_df, on=['FISCAL_YEAR', 'CUST_NO'], how='inner')

print(merged_main_df['BUSINESS_SEGMENT'].isna().sum())

def volume_weighted_average(values, volumes):
    return (values * volumes).sum() / volumes.sum()

# Calculate weighted average for each category
# model_df = merged_main_df.groupby(['LPG_CODE', 'BUSINESS_SEGMENT', 'FISCAL_YEAR', 'CUST_NO', 'PRODUCT_CODE']).apply(
#     lambda x: volume_weighted_average(x['DISCOUNT_RATE'], x['LLP_GC_ORIG'])
# )

model_df = merged_main_df.groupby(['LPG_CODE',  'FISCAL_YEAR', 'CUST_NO','CUST_ADRESSE_ORT','CUST_NAME','CUST_TYPE']).agg(
    volume_weighted_average=('DISCOUNT_RATE', lambda x: volume_weighted_average(x,merged_main_df.loc[x.index,'LLP_GC_ORIG'])),
    sum_QTY = ('QUANTITY', lambda x: merged_main_df.loc[x.index, 'QUANTITY'].sum()),
    sum_REVENUE_LC_ORIG = ('REVENUE_LC_ORIG', lambda x: merged_main_df.loc[x.index, 'REVENUE_LC_ORIG'].sum()),
    sum_REVENUE_GC_ORIG = ('REVENUE_GC_ORIG', lambda x: merged_main_df.loc[x.index, 'REVENUE_GC_ORIG'].sum()),
    sum_LLP_LC_ORIG=('LLP_LC_ORIG', lambda x: merged_main_df.loc[x.index, 'LLP_LC_ORIG'].sum()),
    sum_LLP_GC_ORIG=('LLP_GC_ORIG', lambda x: merged_main_df.loc[x.index, 'LLP_GC_ORIG'].sum())
).reset_index()

print(model_df.info)
print(model_df.isna().sum())

#'BUSINESS_SEGMENT'


# CUST_NO
