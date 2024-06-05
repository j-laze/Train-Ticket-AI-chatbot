import pandas as pd
import os
import numpy as np


def readTrainData():
    path = 'data/TRAIN_DARWIN'
    dataframes = []
    for file in os.listdir(path):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(path, file), low_memory=False)

            df['rid'] = df['rid'].astype(str)
            df['date'] = df['rid'].str[:8]
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
            df['month'] = df['date'].dt.month
            df['day_of_week'] = df['date'].dt.weekday
            df = df[['rid', 'tpl', 'pta', 'ptd', 'arr_at', 'dep_at', 'day_of_week', 'month', 'wta', 'wtd']]

            condition = (df['pta'].isna()) & ((df['tpl'] != 'LIVST') & (df['tpl'] != 'NRCH'))
            df = df.drop(df[condition].index)

            df['ptd'] = pd.to_datetime(df['ptd'], format="%H:%M") - pd.to_datetime('1900-01-01 00:00:00')
            df['ptd'] = df['ptd'].dt.total_seconds() / 60

            df['dep_at'] = pd.to_datetime(df['dep_at'], format="%H:%M") - pd.to_datetime('1900-01-01 00:00:00')
            df['dep_at'] = df['dep_at'].dt.total_seconds() / 60

            df['pta'] = pd.to_datetime(df['pta'], format="%H:%M") - pd.to_datetime('1900-01-01 00:00:00')
            df['pta'] = df['pta'].dt.total_seconds() / 60

            df['wta'] = pd.to_datetime(df['wta'], format="%H:%M", errors='coerce').fillna(
                pd.to_datetime(df['wtd'], format='%H:%M:%S', errors='coerce'))
            df['wta'] = df['wta'].dt.floor('min') - pd.to_datetime('1900-01-01 00:00:00')
            df['wta'] = df['wta'].dt.total_seconds() / 60

            df['wtd'] = pd.to_datetime(df['wtd'], format="%H:%M", errors='coerce').fillna(
                pd.to_datetime(df['wtd'], format='%H:%M:%S', errors='coerce'))
            df['wtd'] = df['wtd'].dt.floor('min') - pd.to_datetime('1900-01-01 00:00:00')
            df['wtd'] = df['wtd'].dt.total_seconds() / 60

            df['arr_at'] = pd.to_datetime(df['arr_at'], format="%H:%M") - pd.to_datetime('1900-01-01 00:00:00')
            df['arr_at'] = df['arr_at'].dt.total_seconds() / 60

            time_columns = ['ptd', 'dep_at', 'pta', 'wta', 'wtd', 'arr_at']

            for col in time_columns:
                df.loc[df[
                           col] < 240, col] += 1440  # To avoid midnight journeys showing as less time, we add a full day to any value in the early morning to ensure consistency

            grouped = df.groupby('rid')
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', None)

            for name, group in grouped:

                group['departure_difference'] = group['dep_at'] - group['ptd']
                group['arrival_difference'] = group['arr_at'] - group['pta']

                condition = (group['tpl'] == 'NRCH') & (group['pta'].isna())
                group.loc[condition, 'pta'] = group.loc[condition, 'wta']

                condition2 = (group['tpl'] == 'LIVST') & (group['ptd'].isna())
                group.loc[condition2, 'ptd'] = group.loc[condition2, 'wtd']

                condition3 = group['tpl'] == 'LIVST'
                group.loc[condition3, 'arr_at'] = group.loc[condition3, 'dep_at']
                group.loc[condition3, 'arrival_difference'] = group.loc[condition3, 'departure_difference']

                try:
                    london_leave_time = group.loc[group['tpl'] == 'LIVST', 'dep_at'].values[0]
                except Exception as e:
                    print(f"An error occurred with group {name} while getting london_leave_time: {e}")
                    print(group)

                try:
                    london_planned_time = group.loc[group['tpl'] == 'LIVST', 'ptd'].values[0]
                except Exception as e:
                    print(f"An error occurred with group {name} while getting london_planned_time: {e}")

                try:
                    london_leave_difference = london_leave_time - group.loc[group['tpl'] == 'LIVST', 'ptd'].values[
                        0]
                except Exception as e:
                    print(f"An error occurred with group {name} while calculating london_leave_difference: {e}")
                    print(group)

                try:
                    norwich_arrival_time = group.loc[group['tpl'] == 'NRCH', 'arr_at'].values[0]
                except Exception as e:
                    print(f"An error occurred with group {name} while getting norwich_arrival_time: {e}")
                    continue;

                try:
                    norwich_arrival_difference = norwich_arrival_time - \
                                                 group.loc[group['tpl'] == 'NRCH', 'pta'].values[0]
                except Exception as e:
                    print(f"An error occurred with group {name} while calculating norwich_arrival_difference: {e}")

                try:
                    norwich_planned_time = group.loc[group['tpl'] == 'NRCH', 'pta'].values[0]

                except Exception as e:
                    print(f"An error occurred with group {name} while calculating norwich_planned_time: {e}")
                    pd.set_option('display.max_rows', None)
                    pd.set_option('display.max_columns', None)
                    pd.set_option('display.width', None)
                    pd.set_option('display.max_colwidth', None)

                group['london_leave_time'] = london_leave_time
                group['london_leave_difference'] = london_leave_difference
                group['london_planned_time'] = london_planned_time
                group['norwich_arrival_time'] = norwich_arrival_time
                group['norwich_arrival_difference'] = norwich_arrival_difference
                group['norwich_planned_time'] = norwich_planned_time

                condition4 = group['tpl'].isin(['LIVST', 'NRCH'])
                group = group.drop(group[condition4].index)

                dataframes.append(group)

    df = pd.concat(dataframes)
    df = df.rename(columns={
        'tpl': 'station',
        'ptd': 'planned_departure',
        'arr_at': 'actual_arrival',
        'dep_at': 'actual_departure',
    })
    df = df[['station', 'planned_departure', 'actual_arrival', 'actual_departure',
             'departure_difference', 'arrival_difference', 'day_of_week', 'month', 'london_leave_difference',
             'norwich_arrival_difference',
             'london_leave_time', 'norwich_arrival_time', 'norwich_planned_time', 'london_planned_time']]
    return df
