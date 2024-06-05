import numpy as np
import pandas as pd
import pickle
import pickle

from sklearn.preprocessing import LabelEncoder


def make_prediction(knn, le, scaler, data):
    print("hello")

    data.station = le.transform([data.station])[0]

    data_list = [
        data.station,
        data.day_of_week,
        data.month,
        data.actual_departure,
        data.departure_difference,
        data.planned_departure,
        data.london_leave_time,
        data.norwich_planned_time,
    ]

    prediction_data = pd.DataFrame([data_list], columns=['station', 'day_of_week', 'month', 'actual_departure',
                                                         'departure_difference', 'planned_departure',
                                                         'london_leave_time', 'norwich_planned_time'])

    prediction_data = pd.DataFrame(scaler.transform(prediction_data), columns=prediction_data.columns)

    prediction = knn.predict(prediction_data)

    return prediction
