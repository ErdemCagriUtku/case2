import pandas as pd

def volume_weighted_average(values, volumes):
    if volumes.sum() != 0:
        return  (values * volumes).sum()/volumes.sum()
    else:
        return -1

def pre_process(transactions_df, customer_df, product_df):
    transactions_df['DISCOUNT_AMOUNT'] = transactions_df['LLP_GC_ORIG'] - transactions_df['REVENUE_GC_ORIG']
    transactions_df['DISCOUNT_RATE'] = transactions_df['DISCOUNT_AMOUNT']/transactions_df['LLP_GC_ORIG']

    # TEST print(transactions_df.isna().sum())

    print((transactions_df==0).sum())
    print(transactions_df.isna().sum())
    #print(transactions_df.loc[:,'DISCOUNT_RATE'].mean())
    # TEST print(transactions_df['LLP_LC_ORIG'] - (transactions_df['LOCAL_LIST_PRICE'] * transactions_df['QUANTITY']))

    # grouped = df.groupby(['Category', 'Subcategory'])['Value'].first().reset_index()
    # print(grouped)

    product_df.rename(columns={'FY': 'FISCAL_YEAR'}, inplace=True )

    merged_main_df = pd.merge(transactions_df, product_df, on=['FISCAL_YEAR', 'PRODUCT_CODE'], how='inner')

    merged_main_df = pd.merge(merged_main_df, customer_df, on=['FISCAL_YEAR', 'CUST_NO'], how='inner')

    merged_main_df=merged_main_df[merged_main_df['LLP_GC_ORIG']!=0]

    print(merged_main_df['BUSINESS_SEGMENT'].isna().sum())

    print(merged_main_df.info)
    print(merged_main_df.dtypes)
    print(merged_main_df['DISCOUNT_RATE'])


    # Calculate weighted average for each category
    # model_df = merged_main_df.groupby(['LPG_CODE', 'BUSINESS_SEGMENT', 'FISCAL_YEAR', 'CUST_NO', 'PRODUCT_CODE']).apply(
    #     lambda x: volume_weighted_average(x['DISCOUNT_RATE'], x['LLP_GC_ORIG'])
    # )

    model_df = merged_main_df.groupby(['LPG_CODE', 'CUST_NAME', 'FISCAL_YEAR']).agg(
         volume_weighted_average = ('DISCOUNT_RATE', lambda x: volume_weighted_average(x, merged_main_df.loc[x.index, 'LLP_GC_ORIG'])),
         sum_DISCOUNT= ('DISCOUNT_AMOUNT', 'sum'),
         sum_QTY = ('QUANTITY', 'sum'),
         sum_REVENUE_LC_ORIG = ('REVENUE_LC_ORIG', lambda x: merged_main_df.loc[x.index, 'REVENUE_LC_ORIG'].sum()),
         sum_REVENUE_GC_ORIG = ('REVENUE_GC_ORIG', lambda x: merged_main_df.loc[x.index, 'REVENUE_GC_ORIG'].sum()),
         sum_LLP_LC_ORIG=('LLP_LC_ORIG', lambda x: merged_main_df.loc[x.index, 'LLP_LC_ORIG'].sum()),
         sum_LLP_GC_ORIG=('LLP_GC_ORIG', lambda x: merged_main_df.loc[x.index, 'LLP_GC_ORIG'].sum())
     ).reset_index()
    #'PRODUCT_TYPE', ->filtered out

    model_df=model_df[model_df['sum_LLP_GC_ORIG']!=0]
    model_df_backup=model_df
    #model_df['volume_weighted_average']=model_df['sum_DISCOUNT']/model_df['sum_LLP_GC_ORIG']

    print (model_df['volume_weighted_average'])


    print(model_df.info)
    print(model_df.isna().sum())
    print(model_df.dtypes)

    # print(merged_main_df.dtypes)
    # print(model_df.dtypes)
    # print(product_df.dtypes)
    cols =['LPG_CODE', 'CUST_NAME']

    model_df[cols] = model_df[cols].astype('category')
    return model_df



# def format_data(product_df, customer_df, transactions_df):
#
#     product_df = product_df.apply(lambda col: col.astype('category'))
#
#     customer_df = customer_df.apply(lambda col: col.astype('category'))
#
#     transactions_df['TRANSACTION_DATE'] = pd.to_datetime(transactions_df['TRANSACTION_DATE'])
#
#     transactions_df['PK'] = transactions_df['PK'].astype('category')
#     transactions_df['BUSINESS_SEGMENT'] = transactions_df['BUSINESS_SEGMENT'].astype('category')
#     transactions_df['CUST_NO'] = transactions_df['CUST_NO'].astype('category')
#     transactions_df['PRODUCT_CODE'] = transactions_df['PRODUCT_CODE'].astype('category')
#     transactions_df['YYKURZANGA'] = transactions_df['YYKURZANGA'].astype('category')
#     transactions_df['SALES_ORDER_NO'] = transactions_df['SALES_ORDER_NO'].astype('category')
#     transactions_df['SALES_ORDER_ITEM_NO'] = transactions_df['SALES_ORDER_ITEM_NO'].astype('category')
#
#     return product_df, customer_df, transactions_df


