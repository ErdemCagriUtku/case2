# README
This project requires the user to specify key configuration variables before running the pipeline. Below is a brief explanation of each variable:

## Configuration Variables

### File Paths
* PRODUCT_PATH: Path to the product master dataset (e.g., product_master_anonymised.csv).
<br /> Example: "C:/Users/cagri/Downloads/Case Study - Part 2/product_master_anonymised.csv"

* CUSTOMER_PATH: Path to the customer master dataset (e.g., customer_master_anonymised.csv).
<br /> Example: "C:/Users/cagri/Downloads/Case Study - Part 2/customer_master_anonymised.csv"

* TRANSACTIONS_PATH: Path to the transactions dataset (e.g., transactions_anonymised.csv).
<br /> Example: "C:/Users/cagri/Downloads/Case Study - Part 2/transactions_anonymised.csv"

### Value Range Settings
* MAX_VOL_PRICE: Maximum allowable numeric value for volume-related pricing (in HQ Currency) to identify and handle outliers.
<br /> Example: 100000000

### Output Settings
* SAVE_PREDS_PATH: Path where the generated predictions file will be saved.
<br /> Example: C:/Users/cagri/Downloads/Case Study - Part 2/preds_output.csv

## Instructions
Edit the config.py file to input the correct file paths and settings for your environment.
Save the changes before running the pipeline.
