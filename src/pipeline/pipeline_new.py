import config.config
from src.ingestion.load_new_data import load_new_data
from src.data_preparation.pre_process import pre_process

from src.model.predict import predict_next_year
from src.model.train_model import train_model

#!#data_valid csv test

loaded_data_array=load_new_data(config.config.PRODUCT_PATH, config.config.CUSTOMER_PATH, config.config.TRANSACTIONS_PATH)

product_df=loaded_data_array[0]
customer_df=loaded_data_array[1]
transactions_df=loaded_data_array[2]

#!#data valid other tests


model_df=pre_process(transactions_df, customer_df, product_df)

final_reg_model=train_model(model_df,config.config.LAST_YEAR)

pred_df=predict_next_year(model_df,final_reg_model,config.config.LAST_YEAR+1)

pred_df.to_csv(config.config.SAVE_PREDS_PATH, index=False)




