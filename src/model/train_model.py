import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso


def train_model (model_df, prediction_year):

    # Split the data
    model_df_train = model_df[model_df['FISCAL_YEAR'] == prediction_year - 3]
    model_df_validation = model_df[model_df['FISCAL_YEAR'] == prediction_year - 2]
    model_df_test = model_df[model_df['FISCAL_YEAR']==prediction_year-1]


    model_df_train = pd.merge(model_df_train.drop(columns=['discount_weighted_average']), model_df_validation[['LPG_CODE', 'CUST_NAME','discount_weighted_average']], on=['LPG_CODE', 'CUST_NAME'], how='inner')
    model_df_train.rename(columns={'discount_weighted_average': 'next_years_discount_weighted_average'}, inplace=True)
    # TEST
    print(model_df_train.info)

    model_df_validation = pd.merge(model_df_validation.drop(columns=['discount_weighted_average']), model_df_test[['LPG_CODE', 'CUST_NAME','discount_weighted_average']], on=['LPG_CODE', 'CUST_NAME'], how='inner')
    model_df_validation.rename(columns={'discount_weighted_average': 'next_years_discount_weighted_average'}, inplace=True)


    model_features=['count_tr_id', 'sum_QTY', 'sum_REVENUE_LC_ORIG', 'sum_REVENUE_GC_ORIG', 'sum_LLP_LC_ORIG', 'sum_LLP_GC_ORIG',
    'count_product_types', 'count_product_codes', 'last_CUST_ADRESSE_ORT', 'LPG_CODE', 'CUST_NAME', 'FISCAL_YEAR']


    X_train=model_df_train[model_features]
    y_train=model_df_train['next_years_discount_weighted_average']


    X_validation=model_df_validation[model_features]
    y_validation=model_df_validation['next_years_discount_weighted_average']


    # Initialize and train model
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression, alpha=100.0': Ridge(alpha=100.0),
        'Ridge Regression, alpha=10.0': Ridge(alpha=10.0),
        'Ridge Regression, alpha=1.0': Ridge(alpha=1.0),
        'Lasso Regression, alpha=10.0': Lasso(alpha=10.0),
        'Lasso Regression, alpha=1.0': Lasso(alpha=1.0),
        'Lasso Regression, alpha=0.1': Lasso(alpha=0.1)
    }

    # Dictionary to store MSE of each model
    mse_dict = {}
    mae_dict = {}
    best_model = None

    # Loop through each model, fit, predict, and calculate MSE
    for model_name, model in models.items():
        # Fit the model
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_validation)

        # Calculate MSE
        mse = mean_squared_error(y_validation, y_pred)
        mae = mean_absolute_error(y_validation, y_pred)

        # Store the MSE in the dictionary
        mse_dict[model_name] = mse
        mae_dict[model_name] = mae
        print(f"{model_name} MSE: {mse:.4f} MAE: {mae:.4f}")

    # Find the model with the minimum MSE
    best_model_name = min(mse_dict, key=mse_dict.get)
    best_mse = mse_dict[best_model_name]
    best_mae=mae_dict[best_model_name]
    best_model = models[best_model_name]  # Store the best model object

    print(f"\nVolume-Weighted Average Discount is predicted for FY = {prediction_year-1}. "
          f"\nThe model with the minimum MSE is: {best_model_name} with an MSE of {best_mse:.4f} and a MAE of {best_mae:.4f}")

    # TEST
    # predictions = best_model.predict(X_test)
    # # Creating a DataFrame with the actual features and predictions
    # X_test['preds'] = predictions
    # X_test.to_csv(config.SAVE_PREDS_PATH, index=False)


    X = X_validation[model_features]
    y = y_validation

    best_model.fit(X, y)

    return best_model

