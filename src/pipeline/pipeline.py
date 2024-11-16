from lib2to3.main import diff_texts

import config.config
from src.ingestion.load_new_data import load_new_data
from src.preprocessing.data_prep import format_data
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso

loaded_data_array=load_new_data(config.config.PRODUCT_PATH, config.config.CUSTOMER_PATH, config.config.TRANSACTIONS_PATH)

product_df=loaded_data_array[0]
customer_df=loaded_data_array[1]
transactions_df=loaded_data_array[2]

# loaded_data_array=format_data(product_df, customer_df, transactions_df)
#
# product_df=loaded_data_array[0]
# customer_df=loaded_data_array[1]
# transactions_df=loaded_data_array[2]

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

merged_main_df=merged_main_df[merged_main_df['LLP_GC_ORIG']!=0]

print(merged_main_df['BUSINESS_SEGMENT'].isna().sum())

print(merged_main_df.info)
print(merged_main_df.dtypes)
print(merged_main_df['DISCOUNT_RATE'])

def volume_weighted_average(values, volumes):
    if volumes.sum() != 0:
        return  (values * volumes).sum()/volumes.sum()
    else:
        return -1


# Calculate weighted average for each category
# model_df = merged_main_df.groupby(['LPG_CODE', 'BUSINESS_SEGMENT', 'FISCAL_YEAR', 'CUST_NO', 'PRODUCT_CODE']).apply(
#     lambda x: volume_weighted_average(x['DISCOUNT_RATE'], x['LLP_GC_ORIG'])
# )

model_df = merged_main_df.groupby(['LPG_CODE', 'BUSINESS_SEGMENT', 'FISCAL_YEAR', 'CUST_ADRESSE_ORT','CUST_NAME','CUST_TYPE']).agg(
     volume_weighted_average = ('DISCOUNT_RATE', lambda x: volume_weighted_average(x, merged_main_df.loc[x.index, 'LLP_GC_ORIG'])),
     sum_DISCOUNT= ('DISCOUNT_AMOUNT', 'sum'),
     sum_QTY = ('QUANTITY', 'sum'),
     sum_REVENUE_LC_ORIG = ('REVENUE_LC_ORIG', lambda x: merged_main_df.loc[x.index, 'REVENUE_LC_ORIG'].sum()),
     sum_REVENUE_GC_ORIG = ('REVENUE_GC_ORIG', lambda x: merged_main_df.loc[x.index, 'REVENUE_GC_ORIG'].sum()),
     sum_LLP_LC_ORIG=('LLP_LC_ORIG', lambda x: merged_main_df.loc[x.index, 'LLP_LC_ORIG'].sum()),
     sum_LLP_GC_ORIG=('LLP_GC_ORIG', lambda x: merged_main_df.loc[x.index, 'LLP_GC_ORIG'].sum())
 ).reset_index()
#'PRODUCT_TYPE', ->filtered out

model_df_backup=model_df
model_df=model_df[model_df['sum_LLP_GC_ORIG']!=0]
#model_df['volume_weighted_average']=model_df['sum_DISCOUNT']/model_df['sum_LLP_GC_ORIG']

print (model_df['volume_weighted_average'])


print(model_df.info)
print(model_df.isna().sum())
print(model_df.dtypes)

# print(merged_main_df.dtypes)
# print(model_df.dtypes)
# print(product_df.dtypes)
cols =['BUSINESS_SEGMENT','LPG_CODE',  'FISCAL_YEAR', 'CUST_ADRESSE_ORT','CUST_NAME','CUST_TYPE']

model_df[cols] = model_df[cols].astype('category')


# Split the data
model_df_train=model_df[model_df['FISCAL_YEAR']!=2024]
model_df_test=model_df[model_df['FISCAL_YEAR']==2024]

model_features=['LPG_CODE', 'BUSINESS_SEGMENT', 'FISCAL_YEAR', 'CUST_ADRESSE_ORT','CUST_NAME','CUST_TYPE', 'sum_QTY','sum_REVENUE_LC_ORIG', 'sum_REVENUE_GC_ORIG', 'sum_LLP_LC_ORIG', 'sum_LLP_GC_ORIG']
#'PRODUCT_TYPE'-> filtered out

X_train=model_df_train[model_features]
y_train=model_df_train['volume_weighted_average']


X_test=model_df_test[model_features]
y_test=model_df_test['volume_weighted_average']


# X = model_df[['LPG_CODE', 'BUSINESS_SEGMENT', 'FISCAL_YEAR', 'CUST_ADRESSE_ORT','CUST_NAME','CUST_TYPE', 'sum_QTY','sum_REVENUE_LC_ORIG', 'sum_REVENUE_GC_ORIG', 'sum_LLP_LC_ORIG', 'sum_LLP_GC_ORIG']]  # Input features
# y = model_df['volume_weighted_average']  # Target variable

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)


# Initialize and train model
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Predict and evaluate
y_pred = linear_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")


#ridge_model = Ridge(alpha=100.0)
#ridge_model = Ridge(alpha=10.0)
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train, y_train)
ridge_pred = ridge_model.predict(X_test)
print(f"Ridge Regression MSE: {mean_squared_error(y_test, ridge_pred)}")



#lasso_model = Lasso(alpha=100.0)
#lasso_model = Lasso(alpha=10.0)
lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_train, y_train)
lasso_pred = lasso_model.predict(X_test)
print(f"Lasso Regression MSE: {mean_squared_error(y_test, lasso_pred)}")


#duplicate check
# model_df['count_rows']=model_df.groupby(['LPG_CODE', 'BUSINESS_SEGMENT', 'FISCAL_YEAR', 'CUST_NAME','CUST_ADRESSE_ORT'])['FISCAL_YEAR'].transform('count')
# print(model_df[model_df['count_rows']!=1])

pred_df=model_df_backup[model_features]
pred_df['FISCAL_YEAR']=2025
pred_df['PREDS_2025']=lasso_model.predict(pred_df)

print(pred_df['PREDS_2025'].mean(axis=0))

print(pred_df)
print(model_df_train['volume_weighted_average'].mean(axis=0))

pred_df[cols] = pred_df[cols].astype('int64')

final_preds=pred_df.groupby(['LPG_CODE', 'FISCAL_YEAR','CUST_NAME']).agg(
     aggregated_2025_preds = ('PREDS_2025', lambda x: volume_weighted_average(x, pred_df.loc[x.index, 'sum_LLP_GC_ORIG']))
 ).reset_index()

print(final_preds)

final_preds.to_csv(config.config.SAVE_PREDS_PATH, index=False)

# MESELELER
#
# 1) join lerken ki year ve pr code, year ve customer code unique degil, uniquelestirilmesi lazim
# 2) modeli kurarken büyük bir granularity yaptim, ama sonuc bu granularitede degil, bu mantikli mi
# 3) predict yaparken direkt bütün eski data setini ayniymis gibi kabul ettim (sales volume leri de dahil), bu mantikli mi?
# 4) gelen kodu hic test etmedim (data validation kismi)
# 5) kodumun tamami ayni sayfada structure edilmesi lazim (fonksiyonlar vs olusturulmasi lazim)
# 6) pipeline dizayninin ne oldugunu tam olarak anlayip ona uygun bir sey yaptigimdan emin olmam lazim
# 7) laso ve ridge regressionlarin parametrelerini baska sayilarla denemedim, optimize edilmesi gerekebilir
# 8) Cocuka mail atip, yarim saat schedule etmem lazim
# 9) Umut, rabia veya harunla konusmam lazim bu olmus mu diye
# 10) kodumu anlatan basit bir görsel hazirlamam lazim
# 11) en son kodumu temizlemem lazim


