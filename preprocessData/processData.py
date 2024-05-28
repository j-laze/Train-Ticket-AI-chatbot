import pandas as pd
import os

def readTrainData():
    path = 'data/TRAIN_DARWIN'
    # END_STATION = 'LIVST'
    # START_STATION =
    dataframes = []
    for file in os.listdir(path):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(path, file), low_memory=False)
            df['rid'] = df['rid'].astype(str)
            df['date'] = df['rid'].str[:8]
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
            df['month'] = df['date'].dt.month
            df['day_of_week'] = df['date'].dt.weekday
            df = df[['tpl', 'pta', 'ptd', 'arr_at', 'dep_at','day_of_week', 'month']]
            df = df.dropna(subset=['ptd', 'dep_at'])

            df['ptd'] = pd.to_datetime(df['ptd'], format="%H:%M") - pd.to_datetime('1900-01-01 00:00:00')
            df['ptd'] = df['ptd'].dt.total_seconds() / 60

            df['dep_at'] = pd.to_datetime(df['dep_at'], format="%H:%M") - pd.to_datetime('1900-01-01 00:00:00')
            df['dep_at'] = df['dep_at'].dt.total_seconds() / 60

            df['pta'] = pd.to_datetime(df['pta'], format="%H:%M") - pd.to_datetime('1900-01-01 00:00:00')
            df['pta'] = df['pta'].dt.total_seconds() / 60

            df['arr_at'] = pd.to_datetime(df['arr_at'], format="%H:%M") - pd.to_datetime('1900-01-01 00:00:00')
            df['arr_at'] = df['arr_at'].dt.total_seconds() / 60


            df['departure_difference'] = (df['dep_at'] - df['ptd'])
            df['arrival_difference'] = (df['arr_at'] - df['pta'])


            pd.set_option('display.max_columns', None)

            dataframes.append(df)



    df = pd.concat(dataframes)
    df = df.rename(columns={
        'tpl': 'station',
        'pta': 'planned_arrival',
        'ptd': 'planned_departure',
        'arr_at': 'actual_arrival',
        'dep_at': 'actual_departure',
    })
    # Y should be deviation from norwich arrival time
    df = df[['station', 'planned_arrival', 'planned_departure', 'actual_arrival', 'actual_departure',  'departure_difference', 'arrival_difference', 'day_of_week', 'month']]
    return df
#classify into weekday or weekend
#classify if its peak or off peak

