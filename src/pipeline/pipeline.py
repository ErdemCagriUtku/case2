import config.config
from src.ingestion.load_new_data import load_new_data
from src.preprocessing.data_prep import format_data
import pandas as pd

loaded_data_array=load_new_data(config.config.PRODUCT_PATH, config.config.CUSTOMER_PATH, config.config.TRANSACTIONS_PATH)

product_df=loaded_data_array[0]
customer_df=loaded_data_array[1]
transactions_df=loaded_data_array[2]

format_data(product_df, customer_df, transactions_df)

