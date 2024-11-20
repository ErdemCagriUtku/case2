import config.config
from src.data_preparation.validate import is_csv, is_table_not_empty, has_no_duplicates, has_valid_date_format, \
    is_transaction_date_valid, is_year_month_deriveable, clean_nas_and_print_message, is_file_empty
from src.ingestion.load_new_data import load_new_data
from src.data_preparation.pre_process import pre_process
import sys
from src.model.predict import predict_next_year
from src.model.train_model import train_model


# Check if the path exists/empty
if is_file_empty(config.config.PRODUCT_PATH):
    sys.exit()

if is_file_empty(config.config.CUSTOMER_PATH):
    sys.exit()

if is_file_empty(config.config.TRANSACTIONS_PATH):
    sys.exit()

# Check if the format is csv
if not is_csv(config.config.PRODUCT_PATH):
    print("Invalid Product Master CSV format. Please provide a valid csv file.")
    sys.exit()

if not is_csv(config.config.CUSTOMER_PATH):
    print("Invalid Customer Master CSV format. Please provide a valid csv file.")
    sys.exit()


if not is_csv(config.config.TRANSACTIONS_PATH):
    print("Invalid Transactions CSV format. Please provide a valid csv file.")
    sys.exit()


product_df, customer_df, transactions_df = load_new_data(config.config.PRODUCT_PATH, config.config.CUSTOMER_PATH, config.config.TRANSACTIONS_PATH)


if not is_table_not_empty(product_df):
    print("Data table is empty")
    sys.exit()

if not is_table_not_empty(customer_df):
    print("Data table is empty")
    sys.exit()

if not is_table_not_empty(transactions_df):
    print("Data table is empty")
    sys.exit()

if not has_no_duplicates(transactions_df):
    transactions_df = transactions_df.drop_duplicates()
    print("Duplicate records detected and removed from transaction data")

if not has_valid_date_format(transactions_df, "TRANSACTION_DATE"):
    print("Invalid date format")
elif not is_transaction_date_valid (transactions_df, "TRANSACTION_DATE"):
    print("Transaction date is in the future")
elif not is_year_month_deriveable(transactions_df, "TRANSACTION_DATE"):
    print("Transaction year does not match transaction date")
else: print("All date checks passed")


# Critical columns are checked for NA values
product_df = clean_nas_and_print_message(product_df, 'PRODUCT_CODE')
product_df = clean_nas_and_print_message(product_df, 'FY')

# Critical columns are checked for NA values
customer_df = clean_nas_and_print_message(customer_df, 'CUST_NO')
customer_df = clean_nas_and_print_message(customer_df, 'FISCAL_YEAR')

# Critical columns are checked for NA values
transactions_df = clean_nas_and_print_message(transactions_df, 'PK')
transactions_df = clean_nas_and_print_message(transactions_df, 'FISCAL_YEAR')
transactions_df = clean_nas_and_print_message(transactions_df, 'CUST_NO')
transactions_df = clean_nas_and_print_message(transactions_df, 'PRODUCT_CODE')

#prepare the data
model_df=pre_process(transactions_df, customer_df, product_df)

#pick the best model
final_reg_model=train_model(model_df,config.config.LAST_YEAR)

#predict the next year
pred_df=predict_next_year(model_df,final_reg_model,config.config.LAST_YEAR+1)

#save the predictions
pred_df.to_csv(config.config.SAVE_PREDS_PATH, index=False)




