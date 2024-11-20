import config.config
from src.data_preparation.validate import is_csv, is_table_not_empty, has_no_duplicates, has_valid_date_format, \
    is_transaction_date_valid, is_year_month_deriveable, clean_nas_and_print_message, is_file_empty, \
    filter_outliers_with_constant, remove_duplicate_rows, check_column_types
from src.ingestion.load_new_data import load_new_data
from src.data_preparation.validate import remove_rows_if_unreasonable_discount
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
# TEST
print("\nfirst check tr:")
print(transactions_df[['LLP_GC_ORIG', 'REVENUE_GC_ORIG']].sum())

# if not has_no_duplicates(transactions_df):
#     transactions_df = transactions_df.drop_duplicates()
#     print("Duplicate records detected and removed from transaction data")

# Duplicates are detected, removed and logged
transactions_df = remove_duplicate_rows(transactions_df, primary_key_column="PK")

# Date format, range and consistency checked
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

# Outliers removed
value_check_columns = ['REVENUE_GC_ORIG', 'LLP_GC_ORIG']
transactions_df = filter_outliers_with_constant(transactions_df, value_check_columns, config.config.MAX_VOL_PRICE, "PK")

# Above 100% discount rates removed
transactions_df = remove_rows_if_unreasonable_discount(transactions_df)

# TEST
# print("\ntransactions_df:")
# print(transactions_df.dtypes)
# print("\ncustomer_df:")
# print(customer_df.dtypes)
# print("\nproduct_df:")
# print(product_df.dtypes)


# Dtypes checked
format_check_columns_product = ['FY', 'PRODUCT_CODE']
check_column_types(product_df, format_check_columns_product, 'int64')

format_check_columns_cust = ['FISCAL_YEAR', 'CUST_NO']
check_column_types(customer_df, format_check_columns_cust, 'int64')

format_check_columns_tr = ['FISCAL_YEAR', 'CUST_NO', 'PRODUCT_CODE']
check_column_types(transactions_df, format_check_columns_tr, 'int64')

format_check_columns_tr_fl = ['REVENUE_LC_ORIG', 'REVENUE_GC_ORIG', 'LOCAL_LIST_PRICE', 'LLP_LC_ORIG',  'LLP_GC_ORIG']
check_column_types(transactions_df, format_check_columns_tr_fl, 'float64')

# TEST
#print(transactions_df[['LLP_GC_ORIG', 'REVENUE_GC_ORIG']].sum())

#prepare the data
model_df=pre_process(transactions_df, customer_df, product_df)

# TEST
# print("\nmodel_df:")
# print(model_df.dtypes)

#pick the best model
final_reg_model=train_model(model_df,config.config.PREDICTION_YEAR)

#predict the next year
pred_df=predict_next_year(model_df,final_reg_model,config.config.PREDICTION_YEAR)

#save the predictions
pred_df.to_csv(config.config.SAVE_PREDS_PATH, index=False)




