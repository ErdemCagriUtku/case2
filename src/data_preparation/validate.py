import pandas as pd
import io
from datetime import datetime
import os


# Check if the path exists and not empty
def is_file_empty(file_path):

    if not os.path.exists(file_path):
        print (f"The file '{file_path}' does not exist.")
        return True

    # Check if the file size is 0 bytes
    if os.path.getsize(file_path) == 0:
        print(f"The file '{file_path}' exists and is empty.")
        return True
    else:
         print(f"The file '{file_path}' exists and is not empty.")
         return False


# Check if file format is CSV
def is_csv(data: str) -> bool:
    try:
        pd.read_csv(io.StringIO(data))  # Try reading the CSV
        return True
    except Exception:
        return False

# Check if table contains value (not empty)
def is_table_not_empty(data: pd.DataFrame) -> bool:
    return not data.empty


# Check if date format is valid (xx/xx/XX)
def has_valid_date_format(data: pd.DataFrame, date_column: str) -> bool:
    try:
        pd.to_datetime(data[date_column], format='%d/%m/%y', errors='raise')
        return True
    except ValueError:
        return False

# Check if transaction date is not in the future
def is_transaction_date_valid(data: pd.DataFrame, date_column: str) -> bool:
    today = pd.to_datetime(datetime.now().date())
    return (pd.to_datetime(data[date_column], errors='coerce') <= today).all()

# Check if transaction year is drivable from transaction date
def is_year_month_deriveable(data: pd.DataFrame, date_column: str, year_column: str) -> bool:
    data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
    year_match = (data[date_column].dt.year == data[year_column]).all()
    return year_match

# TEST
# Check for duplicates based on customer number, product number, and transaction date (not performed))
# def has_no_duplicates(data: pd.DataFrame) -> bool:
#     return not data.duplicated().any()

# Check for duplicates
def remove_duplicate_rows(df, primary_key_column):

    # Identify duplicate rows
    duplicate_rows = df[df.duplicated(keep=False)]  # Keep all duplicates for logging
    removed_pk_values = duplicate_rows[primary_key_column].unique()  # Get unique PKs of duplicates

    if not duplicate_rows.empty:
        print(
            f"The following rows were identified as duplicates and removed based on the PK column '{primary_key_column}':")
        for pk in removed_pk_values:
            print(f" - {pk}")
    else:
        print("No duplicate rows found.")

    # Remove duplicates (keeping the first occurrence)
    filtered_df = df.drop_duplicates(keep='first')

    return filtered_df



def clean_nas_and_print_message(df: pd.DataFrame, critical_column: str):

    # Check if there are any NaN values in the DataFrame
    if df[critical_column].isna().any():
        # Count total NaN values
        na_count = df[critical_column].isna().sum()
        print(f"Found {na_count} missing values in the {critical_column} of the DataFrame.")

        # Drop rows with any NaN values
        df_cleaned = df.dropna(subset=[critical_column])
        print("Dropping rows with NaN values.")
    else:
        print("No missing values found.")
        df_cleaned = df

    return df_cleaned



def filter_outliers_with_constant(df, columns, max_allowed_value, transaction_id_column):

    rows_to_remove = []

    for col in columns:

        # Identify rows where the column value exceeds the maximum allowed value
        outlier_rows = df[(df[col] > max_allowed_value) | (df[col] < 0)]
        for _, row in outlier_rows.iterrows():
            transaction_id = row[transaction_id_column]
            print(
                f"Row with {transaction_id_column} '{transaction_id}' is deleted due to high/low value in column '{col}'.")
            rows_to_remove.append(row.name)

    # Drop the rows identified as outliers
    filtered_df = df.drop(index=rows_to_remove)

    return filtered_df


def check_column_types(df, columns_to_check, expected_type):

    column_types = {}

    for col in columns_to_check:
        if col in df.columns:
            col_type = df[col].dtype
            if col_type == expected_type:
                column_types[col] = col_type
            else:
                column_types[col] = f"Column {col} is not {expected_type}, found {col_type}"
        else:
            column_types[col] = "Column not found in DataFrame"

    return column_types

def remove_rows_if_unreasonable_discount (df):

    # Identify rows where 'REVENUE_GC_ORIG' is greater than 'LLP_GC_ORIG'
    rows_to_remove = df['REVENUE_GC_ORIG'] > df['LLP_GC_ORIG']

    # Check if there are any rows to remove
    if rows_to_remove.any():
        # Remove the rows
        rows_removed = df[rows_to_remove].index
        df = df[~rows_to_remove]  # Keep only rows where the condition is not met

        # Notify the user
        print(f"Rows with indices {list(rows_removed)} have been removed because "
              "'REVENUE_GC_ORIG' was greater than 'LLP_GC_ORIG'.")
    else:
        print("No rows were removed. 'REVENUE_GC_ORIG' was not greater than 'LLP_GC_ORIG' in any row.")

    return df