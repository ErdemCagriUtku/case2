def predict_next_year (model_df,final_reg_model,pred_year):

    #TEST
    #pred_df = model_df[['LPG_CODE', 'CUST_NAME', 'FISCAL_YEAR']].drop_duplicates()

    model_features = ['count_tr_id', 'sum_QTY', 'sum_REVENUE_LC_ORIG', 'sum_REVENUE_GC_ORIG', 'sum_LLP_LC_ORIG',
                      'sum_LLP_GC_ORIG',
                      'count_product_types', 'count_product_codes', 'last_CUST_ADRESSE_ORT', 'LPG_CODE', 'CUST_NAME',
                      'FISCAL_YEAR']

    model_df_test = model_df[model_df['FISCAL_YEAR'] == pred_year-1]
    pred_df = model_df_test[model_features]

    pred_df['DISCOUNT_PREDICTIONS_PRED_YEAR']=final_reg_model.predict(pred_df)

    #print(pred_df['PREDS_NEXT_YEAR'].mean(axis=0))
    #print(pred_df)
    #print(model_df_train['volume_weighted_average'].mean(axis=0))

    cols = ['LPG_CODE', 'CUST_NAME']
    pred_df[cols] = pred_df[cols].astype('int64')

    #print(pred_df)

    return pred_df[['CUST_NAME','LPG_CODE', 'DISCOUNT_PREDICTIONS_PRED_YEAR']]