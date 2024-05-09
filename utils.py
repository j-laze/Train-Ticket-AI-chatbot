import datetime
from enum import Enum


class JourneyType(Enum):
    SINGLE = 1
    RETURN = 2

class TimeCondition(Enum):
    DEPART_AFTER = 1
    RETURN_BEFORE = 2

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
            start_alpha3: str = None,                   ## 3 letter code for the start station
            end_alpha3: str = None,                     ## 3 letter code for the end station
            journey_type: JourneyType = None,           ## SINGLE or RETURN
            out_time: str = None,                       ## the time of departure or arrival for the outward journey
            ret_time: str = None,                       ## the time of departure or arrival for the return journey
            out_date: str = None,                       ## ON_DEPART or ON_ARRIVE
            ret_date: str = None,                       ## ON_DEPART or ON_ARRIVE
            out_time_condition: TimeCondition = None,   ## date and time of departure for the outward journey
            ret_time_condition: TimeCondition = None,   ## date and time of departure for the return journey
            adults: int = None,                         ## number of adults
            children: int = None,                       ## number of children
            railcard: Railcard = None,                  ## the type of railcard
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

class Journey:

    def __init__(
            self,
            start_alpha3: str = None,           ## 3 letter code for the start station
            end_alpha3: str = None,             ## 3 letter code for the end station
            journey_type: JourneyType = None,   ## SINGLE or RETURN
            out_depart_time: datetime = None,   ## date and time of departure for the outward journey
            out_arrive_time: datetime = None,   ## date and time of arrival for the outward journey
            ret_depart_time: datetime = None,   ## date and time of departure for the return journey
            ret_arrive_time: datetime = None,   ## date and time of arrival for the return journey
    ):
        self.start_alpha3 = start_alpha3
        self.end_alpha3 = end_alpha3
        self.journey_type = journey_type
        self.out_depart_time = out_depart_time
        self.out_arrive_time = out_arrive_time
        self.ret_depart_time = ret_depart_time
        self.ret_arrive_time = ret_arrive_time
