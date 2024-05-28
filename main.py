import pandas as pd
import spacy

from nlp.nlp import create_patterns, read_csv_to_df, create_entity_ruler
from reasoning_engine import DialogueFlowEngine
import preprocessData.processData as processData
from sklearn.preprocessing import LabelEncoder, StandardScaler

import KNNmodel.model as model






def main():
    dataframe = processData.readTrainData()

    print(dataframe.head())
    knn_model, le, scaler = model.create_and_train_knn(dataframe)

    test_values = {
        'planned_arrival': [0],
        'planned_departure': [0],
      # Add this
        'actual_departure': [600.0],
        'departure_difference': [10.0],
        'arrival_difference': [0],     # add london start and end

        'day_of_week': [4],
        'month': [3],
        'station': ['IPSWICH']
    }

    # Convert tesijt_values to a DataFrame
    test_df = pd.DataFrame(test_values)

    test_df['station'] = le.transform(test_df['station'])

    test_df = scaler.transform(test_df)




    single_pred = knn_model.predict(test_df)
    print(single_pred)






if __name__ == '__main__':
    main()