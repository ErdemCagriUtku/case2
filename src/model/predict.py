from lib2to3.main import diff_texts
from typing import final

import config.config
from src.ingestion.load_new_data import load_new_data

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso

def predict_next_year (model_df,final_reg_model,pred_year):
    pred_df = model_df[['LPG_CODE', 'CUST_NAME']].drop_duplicates()
    #pred_df=model_df_backup[model_features]
    pred_df['FISCAL_YEAR']=pred_year
    pred_df['PREDS_NEXT_YEAR']=final_reg_model.predict(pred_df)

    print(pred_df['PREDS_NEXT_YEAR'].mean(axis=0))

    print(pred_df)
    #print(model_df_train['volume_weighted_average'].mean(axis=0))
    cols = ['LPG_CODE', 'CUST_NAME']
    pred_df[cols] = pred_df[cols].astype('int64')

    # final_preds=pred_df.groupby(['FISCAL_YEAR','LPG_CODE', 'CUST_NAME']).agg(
    #      aggregated_2025_preds = ('PREDS_2025', lambda x: volume_weighted_average(x, pred_df.loc[x.index, 'sum_LLP_GC_ORIG']))
    #  ).reset_index()

    print(pred_df)
    return pred_df