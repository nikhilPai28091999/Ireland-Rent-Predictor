import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, make_scorer
# import xgboost as xgb  # make sure to install: pip install xgboost
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('data/cleaned-data.csv')
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]


models = {
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
}

# Define features and target
X = df.drop(columns=["Sno", "Title", "Price"])
y = df["Price"]



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and evaluate all
results = []

for name, model in models.items():

    ###### Run K Fold Cross Validation to check whether this model is the right choice or not #####################
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)
    rmse_scorer = make_scorer(lambda y_true, y_pred: np.sqrt(mean_squared_error(y_true, y_pred)), greater_is_better=False)

    cv_mae = cross_val_score(model, X, y, cv=kf, scoring=mae_scorer)
    cv_rmse = cross_val_score(model, X, y, cv=kf, scoring=rmse_scorer)

    print(f"📊 K-Fold CV MAE (avg): {-np.mean(cv_mae):.2f}")
    print(f"📊 K-Fold CV RMSE (avg): {-np.mean(cv_rmse):.2f}")
    ###### Run K Fold Cross Validation to check whether this model is the right choice or not #####################


    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)


    importances = model.feature_importances_
    feature_names = X_train.columns

    # Save as DataFrame
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    })
    importance_df = importance_df[~importance_df["feature"].str.startswith("Location_")]
    importance_df = importance_df.sort_values(by="importance", ascending=False)
    importance_df.to_csv("data/feature_importances.csv", index=False)
    # mae = mean_absolute_error(y_test, y_pred)
    # rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # results.append((name, mae, rmse))
    # print(results)

# # Save trained model
# joblib.dump(model, "rental_price_model.pkl")

# # Save feature names (from training set)
# joblib.dump([col for col in X.columns if col != "Unnamed: 0"], "model_features.pkl")
