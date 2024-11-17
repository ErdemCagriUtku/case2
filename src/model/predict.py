def predict_next_year (model_df,final_reg_model,pred_year):
    pred_df = model_df[['LPG_CODE', 'CUST_NAME']].drop_duplicates()
    pred_df['FISCAL_YEAR']=pred_year
    pred_df['PREDS_NEXT_YEAR']=final_reg_model.predict(pred_df)

    #print(pred_df['PREDS_NEXT_YEAR'].mean(axis=0))
    #print(pred_df)
    #print(model_df_train['volume_weighted_average'].mean(axis=0))

    cols = ['LPG_CODE', 'CUST_NAME']
    pred_df[cols] = pred_df[cols].astype('int64')

    #print(pred_df)

    return pred_df