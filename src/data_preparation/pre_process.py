from itertools import count

import pandas as pd

def volume_weighted_average(values, volumes):
    if volumes.sum() != 0:
        return  (values * volumes).sum()/volumes.sum()
    else:
        return -1

def pre_process(transactions_df, customer_df, product_df):

    transactions_df = transactions_df[transactions_df['LLP_GC_ORIG'] != 0]

    transactions_df['DISCOUNT_AMOUNT'] = transactions_df['LLP_GC_ORIG'] - transactions_df['REVENUE_GC_ORIG']
    transactions_df['DISCOUNT_RATE'] = transactions_df['DISCOUNT_AMOUNT']/transactions_df['LLP_GC_ORIG']

    # TEST
    # print(transactions_df.isna().sum())

    print((transactions_df==0).sum())
    print(transactions_df.isna().sum())

    # TEST
    # print(transactions_df.loc[:,'DISCOUNT_RATE'].mean())
    # print(transactions_df['LLP_LC_ORIG'] - (transactions_df['LOCAL_LIST_PRICE'] * transactions_df['QUANTITY']))
    # grouped = df.groupby(['Category', 'Subcategory'])['Value'].first().reset_index()
    # print(grouped)

    product_df.rename(columns={'FY': 'FISCAL_YEAR'}, inplace=True)

    product_df = product_df.drop_duplicates(subset=['FISCAL_YEAR', 'PRODUCT_CODE'],keep='last')
    customer_df = customer_df.drop_duplicates(subset=['FISCAL_YEAR', 'CUST_NO'], keep='last')

    merged_main_df = pd.merge(transactions_df, product_df, on=['FISCAL_YEAR', 'PRODUCT_CODE'], how='inner')

    merged_main_df = pd.merge(merged_main_df, customer_df, on=['FISCAL_YEAR', 'CUST_NO'], how='inner')

    merged_main_df=merged_main_df[merged_main_df['LLP_GC_ORIG']!=0]

    #TEST
    merged_main_df.to_csv('C:/Users/cagri/Downloads/Case Study - Part 2/merged_main_df.csv', index=False)

    # TEST
    # print(merged_main_df['BUSINESS_SEGMENT'].isna().sum())
    #
    # print(merged_main_df.info)
    # print(merged_main_df.dtypes)
    # print(merged_main_df['DISCOUNT_RATE'])

    model_df = merged_main_df.groupby(['LPG_CODE', 'CUST_NAME', 'FISCAL_YEAR']).agg(
         discount_weighted_average = ('DISCOUNT_RATE', lambda x: volume_weighted_average(x, merged_main_df.loc[x.index, 'LLP_GC_ORIG'])),
         sum_DISCOUNT= ('DISCOUNT_AMOUNT', 'sum'),
         count_tr_id = ('PK', 'nunique'),
         sum_QTY = ('QUANTITY', 'sum'),
         sum_REVENUE_LC_ORIG = ('REVENUE_LC_ORIG', lambda x: merged_main_df.loc[x.index, 'REVENUE_LC_ORIG'].sum()),
         sum_REVENUE_GC_ORIG = ('REVENUE_GC_ORIG', lambda x: merged_main_df.loc[x.index, 'REVENUE_GC_ORIG'].sum()),
         sum_LLP_LC_ORIG=('LLP_LC_ORIG', lambda x: merged_main_df.loc[x.index, 'LLP_LC_ORIG'].sum()),
         sum_LLP_GC_ORIG=('LLP_GC_ORIG', lambda x: merged_main_df.loc[x.index, 'LLP_GC_ORIG'].sum()),
         count_product_types = ('PRODUCT_TYPE', 'nunique'),
         count_product_codes = ('PRODUCT_CODE', 'nunique'),
         last_CUST_ADRESSE_ORT = ('CUST_ADRESSE_ORT', 'first')

     ).reset_index()


    model_df=model_df[model_df['sum_LLP_GC_ORIG']!=0]

    # TEST
    # print (model_df['volume_weighted_average'])
    # print(model_df.info)
    # print(model_df.isna().sum())
    # print(model_df.dtypes)

    # print(merged_main_df.dtypes)
    # print(model_df.dtypes)
    # print(product_df.dtypes)

    cols =['LPG_CODE', 'CUST_NAME']
    model_df[cols] = model_df[cols].astype('category')

    #TEST
    model_df.to_csv('C:/Users/cagri/Downloads/Case Study - Part 2/model_df.csv', index=False)
    print("\nmodel_sums:")
    print(model_df[['sum_DISCOUNT', 'sum_REVENUE_GC_ORIG', 'sum_LLP_GC_ORIG']].sum())

    return model_df


import pandas as pd


