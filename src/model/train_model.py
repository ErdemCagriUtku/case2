from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso


def train_model (model_df, last_year):

    # Split the data
    model_df_train=model_df[model_df['FISCAL_YEAR']<last_year]
    model_df_test=model_df[model_df['FISCAL_YEAR']==last_year]

    model_features=['LPG_CODE', 'CUST_NAME', 'FISCAL_YEAR']


    X_train=model_df_train[model_features]
    y_train=model_df_train['volume_weighted_average']


    X_test=model_df_test[model_features]
    y_test=model_df_test['volume_weighted_average']


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

