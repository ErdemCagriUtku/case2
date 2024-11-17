from lib2to3.main import diff_texts
from typing import final

import config.config
from src.ingestion.load_new_data import load_new_data

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso


def train_model (model_df, last_year):

    # Split the data
    model_df_train=model_df[model_df['FISCAL_YEAR']!=last_year]
    model_df_test=model_df[model_df['FISCAL_YEAR']==last_year]

    model_features=['LPG_CODE', 'CUST_NAME', 'FISCAL_YEAR']
    #'PRODUCT_TYPE'-> filtered out

    X_train=model_df_train[model_features]
    y_train=model_df_train['volume_weighted_average']


    X_test=model_df_test[model_features]
    y_test=model_df_test['volume_weighted_average']


    # X = model_df[['LPG_CODE', 'BUSINESS_SEGMENT', 'FISCAL_YEAR', 'CUST_ADRESSE_ORT','CUST_NAME','CUST_TYPE', 'sum_QTY','sum_REVENUE_LC_ORIG', 'sum_REVENUE_GC_ORIG', 'sum_LLP_LC_ORIG', 'sum_LLP_GC_ORIG']]  # Input features
    # y = model_df['volume_weighted_average']  # Target variable

    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

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
    best_model = None

    # Loop through each model, fit, predict, and calculate MSE
    for model_name, model in models.items():
        # Fit the model
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate MSE
        mse = mean_squared_error(y_test, y_pred)

        # Store the MSE in the dictionary
        mse_dict[model_name] = mse
        print(f"{model_name} MSE: {mse:.4f}")

    # Find the model with the minimum MSE
    best_model_name = min(mse_dict, key=mse_dict.get)
    best_mse = mse_dict[best_model_name]
    best_model = models[best_model_name]  # Store the best model object

    print(f"\nThe model with the minimum MSE is: {best_model_name} with an MSE of {best_mse:.4f}")


    X = model_df[model_features]
    y = model_df['volume_weighted_average']

    best_model.fit(X, y)

    return best_model


    # linear_model = LinearRegression()
    # linear_model.fit(X_train, y_train)
    #
    # # Predict and evaluate
    # y_pred = linear_model.predict(X_test)
    # mse = mean_squared_error(y_test, y_pred)
    # print(f"Mean Squared Error: {mse}")
    #
    #
    # #ridge_model = Ridge(alpha=100.0)
    # #ridge_model = Ridge(alpha=10.0)
    # ridge_model = Ridge(alpha=1.0)
    # ridge_model.fit(X_train, y_train)
    # ridge_pred = ridge_model.predict(X_test)
    # print(f"Ridge Regression MSE: {mean_squared_error(y_test, ridge_pred)}")
    #
    #
    #
    # #lasso_model = Lasso(alpha=100.0)
    # #lasso_model = Lasso(alpha=10.0)
    # lasso_model = Lasso(alpha=0.1)
    # lasso_model.fit(X_train, y_train)
    # lasso_pred = lasso_model.predict(X_test)
    # print(f"Lasso Regression MSE: {mean_squared_error(y_test, lasso_pred)}")
    #
    #
    # #duplicate check
    # # model_df['count_rows']=model_df.groupby(['LPG_CODE', 'BUSINESS_SEGMENT', 'FISCAL_YEAR', 'CUST_NAME','CUST_ADRESSE_ORT'])['FISCAL_YEAR'].transform('count')
    # # print(model_df[model_df['count_rows']!=1])
    #
    #
    # X_train_final=model_df_backup[model_features]
    # y_train_final=model_df_backup['volume_weighted_average']
    #
    # lasso_model_final = Lasso(alpha=0.1)
    # lasso_model_final.fit(X_train_final, y_train_final)