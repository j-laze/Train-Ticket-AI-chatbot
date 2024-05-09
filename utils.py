import datetime
from enum import Enum


class JourneyType(Enum):
    SINGLE = 1
    RETURN = 2


class TimeCondition(Enum):
    ON_DEPART = 1
    ON_ARRIVE = 2


class Enquiry:

    def __init__(
            self,
            start_alpha3: str = None,
            end_alpha3: str = None,
            journey_type: JourneyType = None,
            out_time: str = None,
            ret_time: str = None,
            out_time_condition: TimeCondition = None,
            ret_time_condition: TimeCondition = None,
            out_date: str = None,
            ret_date: str = None

    ):
        self.start_alpha3 = start_alpha3  ## 3 letter code for the start station
        self.end_alpha3 = end_alpha3  ## 3 letter code for the end station
        self.journey_type = journey_type  ## SINGLE or RETURN
        self.out_time = out_time  ## the time of departure or arrival for the outward journey
        self.ret_time = ret_time  ## the time of departure or arrival for the return journey
        self.out_time_condition = out_time_condition  ## ON_DEPART or ON_ARRIVE
        self.ret_time_condition = ret_time_condition  ## ON_DEPART or ON_ARRIVE
        self.out_date = out_date  ## date and time of departure for the outward journey
        self.ret_date = ret_date  ## date and time of departure for the return journey


class Journey:

    def __init__(
            self,
            start_alpha3: str = None,  ## 3 letter code for the start station
            end_alpha3: str = None,  ## 3 letter code for the end station
            journey_type: JourneyType = None,  ## SINGLE or RETURN
            out_depart_time: datetime = None,  ## date and time of departure for the outward journey
            out_arrive_time: datetime = None,  ## date and time of arrival for the outward journey
            ret_depart_time: datetime = None,  ## date and time of departure for the return journey
            ret_arrive_time: datetime = None  ## date and time of arrival for the return journey
    ):
        self.start_alpha3 = start_alpha3
        self.end_alpha3 = end_alpha3
        self.journey_type = journey_type
        self.out_depart_time = out_depart_time
        self.out_arrive_time = out_arrive_time
        self.ret_depart_time = ret_depart_time
        self.ret_arrive_time = ret_arrive_time
