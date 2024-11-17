import pandas as pd
import io
from datetime import datetime
import numpy as np

# 1. Check if file format is CSV
def is_csv(data: str) -> bool:
    try:
        pd.read_csv(io.StringIO(data))  # Try reading the CSV
        return True
    except Exception:
        return False

# 2. Check if table contains value (not empty)
def is_table_not_empty(data: pd.DataFrame) -> bool:
    return not data.empty

# 3. Check if column names are as expected
def has_valid_column_names(data: pd.DataFrame, expected_columns: list) -> bool:
    return list(data.columns) == expected_columns

# 4. Check if certain critical columns have null values
def has_no_nulls_in_critical_columns(data: pd.DataFrame, critical_columns: list) -> bool:
    return data[critical_columns].isnull().sum().sum() == 0

# 5. Check if data types are correct
def has_correct_data_types(data: pd.DataFrame, expected_dtypes: dict) -> bool:
    for col, expected_dtype in expected_dtypes.items():
        if col in data.columns and not pd.api.types.is_dtype_equal(data[col].dtype, expected_dtype):
            return False
    return True

# 6. Check if date format is valid (xx/xx/XX)
def has_valid_date_format(data: pd.DataFrame, date_column: str) -> bool:
    try:
        pd.to_datetime(data[date_column], format='%d/%m/%y', errors='raise')
        return True
    except ValueError:
        return False

# 7. Check for outliers in sales volume and revenue
def has_no_outliers(data: pd.DataFrame, columns: list) -> bool:
    for column in columns:
        if column in data.columns:
            q1 = data[column].quantile(0.25)
            q3 = data[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            if ((data[column] < lower_bound) | (data[column] > upper_bound)).any():
                return False
    return True

# 8. Check if transaction date is not in the future
def is_transaction_date_valid(data: pd.DataFrame, date_column: str) -> bool:
    today = pd.to_datetime(datetime.now().date())
    return (pd.to_datetime(data[date_column], errors='coerce') <= today).all()

# 9. Check if transaction year and month are drivable from transaction date
def is_year_month_deriveable(data: pd.DataFrame, date_column: str, year_column: str, month_column: str) -> bool:
    data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
    year_match = (data[date_column].dt.year == data[year_column]).all()
    month_match = (data[date_column].dt.month == data[month_column]).all()
    return year_match and month_match

# 10. Check for duplicates based on customer number, product number, and transaction date
def has_no_duplicates(data: pd.DataFrame, key_columns: list) -> bool:
    return not data.duplicated(subset=key_columns).any()

# Main validation function
def validate_data(csv_data: str):
    expected_columns = ["customer_no", "product_no", "sales_volume", "revenue", "tr_date", "tr_year", "tr_month"]
    critical_columns = ["customer_no", "product_no", "sales_volume", "tr_date"]
    expected_dtypes = {
        "customer_no": object,
        "product_no": object,
        "sales_volume": float,
        "revenue": float,
        "tr_date": object,
        "tr_year": int,
        "tr_month": int
    }
    outlier_columns = ["sales_volume", "revenue"]
    key_columns = ["customer_no", "product_no", "tr_date"]

    # 1. Check CSV format
    if not is_csv(csv_data):
        return "Invalid CSV format"

    data = pd.read_csv(io.StringIO(csv_data))

    # 2. Check if table contains values
    if not is_table_not_empty(data):
        return "Data table is empty"

    # 3. Check if column names match
    if not has_valid_column_names(data, expected_columns):
        return "Invalid column names"

    # 4. Check for nulls in critical columns
    if not has_no_nulls_in_critical_columns(data, critical_columns):
        return "Null values found in critical columns"

    # 5. Check data types
    if not has_correct_data_types(data, expected_dtypes):
        return "Data types mismatch"

    # 6. Check date format
    if not has_valid_date_format(data, "tr_date"):
        return "Invalid date format"

    # 7. Check for outliers
    if not has_no_outliers(data, outlier_columns):
        return "Outliers detected in sales volume or revenue"

    # 8. Check transaction date is not in the future
    if not is_transaction_date_valid(data, "tr_date"):
        return "Transaction date is in the future"

    # 9. Check if year and month are drivable from transaction date
    if not is_year_month_deriveable(data, "tr_date", "tr_year", "tr_month"):
        return "Transaction year and month do not match transaction date"

    # 10. Check for duplicates
    if not has_no_duplicates(data, key_columns):
        return "Duplicate records detected based on customer number, product number, and transaction date"

    return "Validation successful"













# if file format is not csv
#
#
#
# if table contains value
#
# if col names are as we know
#
# if customer no / product no/ sales volume / tr date is null
#
# if dtypes are not as shown in here
#
# if date format is not xx/xx/XX
#
# if sales volume and revenue are outlier
#
# if transaction date is bigger than today
#
# if transaction year and month are not driveable from the tr date
#
# if there are duplicates (customer ve product icin tarih ve cust no ya göre denenebilir)->burada devam da edilebilir

