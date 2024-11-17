import pandas as pd
import io
from datetime import datetime

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

# Check if transaction year and month are drivable from transaction date
def is_year_month_deriveable(data: pd.DataFrame, date_column: str, year_column: str, month_column: str) -> bool:
    data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
    year_match = (data[date_column].dt.year == data[year_column]).all()
    month_match = (data[date_column].dt.month == data[month_column]).all()
    return year_match and month_match

# Check for duplicates based on customer number, product number, and transaction date
def has_no_duplicates(data: pd.DataFrame) -> bool:
    return not data.duplicated().any()


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

