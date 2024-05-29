import pandas as pd
import spacy

from nlp.nlp import create_patterns, read_csv_to_df, create_entity_ruler
from reasoning_engine import DialogueFlowEngine
import preprocessData.processData as processData
from sklearn.preprocessing import LabelEncoder, StandardScaler

import KNNmodel.model as model






def main():
    df = pd.read_csv('processed_data.csv')

    condition = df[['actual_arrival', 'norwich_arrival_time']].isna().all(axis=1)
    df = df.dropna()

    knn_model, le, scaler = model.create_and_train_knn(df)


    test_values = {
        'station': ['MANNGTR'],
        'planned_departure': [1045.0],
        'actual_departure': [1055.0],
        'departure_difference': [10.0],
        'day_of_week': [4],
        'month': [3],
        'london_leave_time': [1000],
    }

    test_df = pd.DataFrame(test_values)

    test_df['station'] = le.transform(test_df['station'])

    test_df = scaler.transform(test_df)

    single_pred = knn_model.predict(test_df)
    print(single_pred)





if __name__ == '__main__':
    main()