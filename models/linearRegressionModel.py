import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

def create_and_train_linear_regression(df):
    na_columns = df.columns[df.isna().any()].tolist()
    print(na_columns)

    # le = LabelEncoder()
    # df.loc[:, 'station'] = le.fit_transform(df['station'])

    df = pd.get_dummies(df, columns=['station'])

    columns_to_train = df.columns.tolist()

    columns_to_train.remove('norwich_arrival_time')

    other_columns_to_train = [
        'station',
        'day_of_week',
        'month',
        'actual_departure',
        'departure_difference',
        'planned_departure',
        'actual_arrival',
        'london_leave_time',
        'london_planned_time',
        'norwich_planned_time',
        'london_leave_difference'
    ]
    columns_to_train = [col for col in columns_to_train if col in other_columns_to_train or 'station' in col]

    X = df[columns_to_train]
    y = df['norwich_arrival_time']
    print("this is the length of Y ", len(y))
    print("this is the length of X", len(X))

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    alphas = np.arange(1, 10, 1)

    best_rmse = None
    best_alpha = None
    best_weights = None
    best_lr = None

    for alpha in alphas:
        lr = Ridge(alpha=alpha)

        for _ in range(30):
            np.random.seed(0)
            weights = np.random.uniform(low=0.5, high=2.5, size=X_train.shape[0])


            lr.fit(X_train, y_train, sample_weight=weights)


            y_pred = lr.predict(X_test)


            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)

            if best_rmse is None or rmse < best_rmse:
                best_rmse = rmse
                best_alpha = alpha
                best_weights = weights
                best_lr = lr

    print(f'Best Alpha: {best_alpha}, Best Weights: {best_weights}, Best Root Mean Squared Error: {best_rmse}')


    plt.scatter(y_train, best_lr.predict(X_train), color='blue', label='Train data')


    plt.scatter(y_test, best_lr.predict(X_test), color='red', label='Test data')


    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')

    plt.legend()

    plt.show()

    return best_lr,  scaler