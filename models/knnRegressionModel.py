from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

import numpy as np


def create_and_train_knn(df):
    na_columns = df.columns[df.isna().any()].tolist()
    print(na_columns)

    le = LabelEncoder()
    df.loc[:, 'station'] = le.fit_transform(df['station'])

    columns_to_train = [
        'station',
        'day_of_week',
        'month',
        'actual_departure',
        'departure_difference',
        'planned_departure',
        'london_leave_time',
        'norwich_planned_time',
    ]
    X = df[columns_to_train]
    y = df['norwich_arrival_difference']
    print("this is the length of Y ", len(y))
    print("this is the length of X", len(X))

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    neighbors = list(range(53, 55, 1))

    cv_scores = []

    for k in neighbors:
        knn = KNeighborsRegressor(n_neighbors=k)
        scores = cross_val_score(knn, X_train, y_train, cv=10, scoring='neg_mean_squared_error')
        cv_scores.append(scores.mean())
        rmse = np.sqrt(np.abs(scores.mean()))
        print(f"Number of neighbors: {k}, Cross-validation score: {scores.mean()}, RMSE: {rmse}")

    mse = [1 - x for x in cv_scores]

    optimal_k = neighbors[mse.index(min(mse))]
    print(f"The optimal number of neighbors is {optimal_k}")

    knn = KNeighborsRegressor(n_neighbors=optimal_k)

    knn.fit(X_train, y_train)

    y_train_pred = knn.predict(X_train)
    y_test_pred = knn.predict(X_test)

    plt.scatter(y_train, y_train_pred, color='blue', label='Train data')
    plt.scatter(y_test, y_test_pred, color='red', label='Test data')

    plt.title('Actual vs Predicted Values')
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')

    # Add more information to the legend
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    plt.legend([f'Train data (RMSE: {train_rmse:.2f})', f'Test data (RMSE: {test_rmse:.2f})'])

    plt.show()

    y_pred = knn.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    print('Root Mean Squared Error for Test Data:', rmse)

    return knn, le, scaler
