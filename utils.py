import datetime
from enum import Enum
import pandas as pd
import pickle


def open_model():
    with open('models/dumpedModels/knnModel.pkl', 'rb') as file:
        knn_load = pickle.load(file)
    with open('models/dumpedModels/labelEncoder.pkl', 'rb') as file:
        le_load = pickle.load(file)
    with open('models/dumpedModels/scaler.pkl', 'rb') as file:
        scaler_load = pickle.load(file)
    return knn_load, le_load, scaler_load


knn, le, scaler = open_model()


def read_csv_to_df():
    column_names = ["name", "longname", "name_alias", "alpha3", "tiploc"]
    df = pd.read_csv('data/stations.csv', names=column_names, skiprows=1)

    return df


station_df = read_csv_to_df()


class JourneyType(Enum):
    SINGLE = 1
    RETURN = 2


class TimeCondition(Enum):
    DEPART_AFTER = 1
    ARRIVE_BEFORE = 2


class Railcard(Enum):
    AGE_16_17 = 1
    AGE_16_25 = 2
    AGE_26_30 = 3
    DISABLED = 4
    FAMILY_FRIEND = 5
    NETWORK = 6
    SENIOR = 7
    TOGETHER = 8
    VETERAN = 9


class Enquiry:

    def __init__(
            self,
            start_alpha3: str = None,  ## 3 letter code for the start station
            end_alpha3: str = None,  ## 3 letter code for the end station
            journey_type: JourneyType = None,  ## SINGLE or RETURN
            out_time: str = None,  ## the time of departure or arrival for the outward journey
            ret_time: str = None,  ## the time of departure or arrival for the return journey
            out_date: str = None,  ## ON_DEPART or ON_ARRIVE
            ret_date: str = None,  ## ON_DEPART or ON_ARRIVE
            out_time_condition: TimeCondition = None,  ## date and time of departure for the outward journey
            ret_time_condition: TimeCondition = None,  ## date and time of departure for the return journey
            adults: int = None,  ## number of adults
            children: int = None,  ## number of children
            railcard: Railcard = None,  ## the type of railcard
    ):
        self.start_alpha3 = start_alpha3
        self.end_alpha3 = end_alpha3
        self.journey_type = journey_type
        self.out_time = out_time
        self.ret_time = ret_time
        self.out_time_condition = out_time_condition
        self.ret_time_condition = ret_time_condition
        self.out_date = out_date
        self.ret_date = ret_date
        self.adults = adults
        self.children = children
        self.railcard = railcard

    def __str__(self):
        return f"Enquiry(start_alpha3={self.start_alpha3}, end_alpha3={self.end_alpha3}, journey_type={self.journey_type}, out_time={self.out_time}, ret_time={self.ret_time}, out_date={self.out_date}, ret_date={self.ret_date}, out_time_condition={self.out_time_condition}, ret_time_condition={self.ret_time_condition}, adults={self.adults}, children={self.children}, railcard={self.railcard})"


class DelayPrediction:
    def __init__(
            self,
            station: str = None,  ## the station code
            day_of_week: int = None,  ## the day of the week
            month: int = None,  ## the month
            actual_departure: int = None,  ## the actual departure time
            departure_difference: int = None,  ## the difference between the actual and planned departure times
            planned_departure: int = None,  ## the planned departure time
            actual_arrival: int = None,  ## the actual arrival time
            london_leave_time: int = None,  ## the time the train leaves london
            london_planned_time: int = None,  ## the planned time the train leaves london
            london_leave_difference: int = None,
            norwich_planned_time: int = None,
            norwich_arrival_time: int = None,
            norwich_arrival_difference: int = None
    ):
        self.station = station
        self.day_of_week = day_of_week
        self.month = month
        self.actual_departure = actual_departure
        self.departure_difference = departure_difference
        self.planned_departure = planned_departure
        self.london_leave_time = london_leave_time
        self.norwich_planned_time = norwich_planned_time
        self.norwich_arrival_time = norwich_arrival_time


class Journey:

    def __init__(
            self,
            start_alpha3: str = None,  ## 3 letter code for the start station
            end_alpha3: str = None,  ## 3 letter code for the end station
            journey_type: JourneyType = None,  ## SINGLE or RETURN
            out_depart_time: datetime = None,  ## date and time of departure for the outward journey
            out_arrive_time: datetime = None,  ## date and time of arrival for the outward journey
            ret_depart_time: datetime = None,  ## date and time of departure for the return journey
            ret_arrive_time: datetime = None,  ## date and time of arrival for the return journey
    ):
        self.start_alpha3 = start_alpha3
        self.end_alpha3 = end_alpha3
        self.journey_type = journey_type
        self.out_depart_time = out_depart_time
        self.out_arrive_time = out_arrive_time
        self.ret_depart_time = ret_depart_time
        self.ret_arrive_time = ret_arrive_time
