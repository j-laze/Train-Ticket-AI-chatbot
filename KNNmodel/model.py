from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import numpy as np


def create_and_train_knn(df):
    df = df.dropna()
    print(df.columns)

    le = LabelEncoder()
    df.loc[:, 'station'] = le.fit_transform(df['station'])

    columns_to_drop = ['actual_arrival', 'arrival_difference', 'norwich_arrival_difference', 'norwich_arrival_time',
                       'london_leave_difference']
    X = df.drop(columns_to_drop, axis=1)
    y = df['norwich_arrival_time']
    print("this is the length of Y ", len(y))
    print("this is the length of X", len(X))

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn = KNeighborsRegressor(n_neighbors=5)

    knn.fit(X_train, y_train)

    y_pred = knn.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)

    rmse = np.sqrt(mse)

    print('Root Mean Squared Error:', rmse)

    return knn, le, scaler