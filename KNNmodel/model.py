from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import numpy as np


def create_and_train_knn(df):
    # Handle missing values
    df = df.dropna()
    print(df.shape[0])

    le = LabelEncoder()
    df.loc[:, 'station'] = le.fit_transform(df['station'])


    scaler = StandardScaler()
    df.loc[:, ['planned_arrival', 'planned_departure', 'actual_arrival', 'actual_departure', 'departure_difference', 'arrival_difference', 'day_of_week', 'month', 'station']]\
        = scaler.fit_transform(df[['planned_arrival', 'planned_departure', 'actual_arrival', 'actual_departure', 'departure_difference', 'arrival_difference', 'day_of_week', 'month', 'station']])

    print("DF HEAD",    4df.head())
    X = df.drop('actual_arrival', axis=1)
    y = df['actual_arrival']
    print("this is the lenght of Y ", y)# Set 'actual_arrival' as the target variable
    print("this is the length of X", X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn = KNeighborsRegressor(n_neighbors=5)

    # Train the model using the training data
    knn.fit(X_train, y_train)

    return knn, le, scaler