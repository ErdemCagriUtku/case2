# Please specify data source paths before running the pipeline
PRODUCT_PATH = 'C:/Users/cagri/Downloads/Case Study - Part 2/product_master_anonymised.csv'
CUSTOMER_PATH = 'C:/Users/cagri/Downloads/Case Study - Part 2/customer_master_anonymised.csv'
TRANSACTIONS_PATH = 'C:/Users/cagri/Downloads/Case Study - Part 2/transactions_anonymised.csv'

# Maximum allowable value for volume-related pricing (in HQ Currency) to identify and handle outliers.
MAX_VOL_PRICE = 100000000  # Max value to filter outliers

# Output paths: Where to save the prediction results
SAVE_PREDS_PATH = 'C:/Users/cagri/Downloads/Case Study - Part 2/preds_output.csv'

# Prediction settings (This value is a constant that is used by the ML models, please do not make a change)
PREDICTION_YEAR = 2025  # The year for which predictions will be made
