from utils import Enquiry
from nlp.nlp import recognise_station_directions, recognise_times, recognise_dates, recognise_station, \
    print_named_entities_debug, recognise_single_or_return, recognise_time_mode, print_time_tokens, fmt_natlang_time, \
    recognise_chosen_service, recognise_station_pred, time_to_minutes, minutes_to_time, yes_or_no
import sys
import datetime

from webscrape.splitmyfare import get_journeys
from utils import JourneyType, TimeCondition, Railcard
from utils import Enquiry, Journey, DelayPrediction
from utils import knn, le, scaler
from models.getPredictionKnn import make_prediction
import dateparser


class DialogueFlowEngine:
    def __init__(self, nlp, station_df):
        self.service = None
        self.nlp = nlp
        self.station_df = station_df
        self.user_enquiry = Enquiry()
        self.prediction_enquiry = DelayPrediction()
        self.state = 'ASKING_SERVICE'
        self.dialogue_flow = {
            'ASKING_SERVICE': {
                'method': self.handle_asking_service,
                'check': self.ask_service_check,
                'next_state': 'ASKING_SERVICE'
            },

            'ASKING_PREDICTION_STATION': {
                'method': self.handle_pred_station,
                'check': self.pred_station_check,
                'next_state': 'ASKING_PREDICTION_DELAY'
            },
            'ASKING_PREDICTION_DELAY': {
                'method': self.handle_pred_delay,
                'check': self.pred_delay_check,
                'next_state': 'ASKING_PREDICTION_LONDON_LEAVE_TIME'
            },
            'ASKING_PREDICTION_LONDON_LEAVE_TIME': {
                'method': self.handle_pred_london_leave_time,
                'check': self.pred_london_leave_time_check,
                'next_state': 'ASKING_PREDICTION_NORWICH_PLANNED_TIME'
            },
            'ASKING_PREDICTION_NORWICH_PLANNED_TIME': {
                'method': self.handle_pred_norwich_planned_time,
                'check': self.pred_norwich_planned_time_check,
                'next_state': 'CONFIRMING_PREDICTION'
            },
            'CONFIRMING_PREDICTION': {
                'method': self.handle_confirming_prediction,
                'check': self.confirm_prediction_check,
                'next_state': 'COMPLETED_PREDICTION'
            },
            'COMPLETED_PREDICTION': {
                'method': self.completion_prediction,
                'next_state': None
            },
            'ASKING_JOURNEY_DETAILS': {
                'method': self.handle_journey_details,
                'check': self.start_location_check,
                'next_state': 'ASKING_START_LOCATION'
            },
            'ASKING_START_LOCATION': {
                'method': self.handle_start_location,
                'check': self.start_location_check,
                'next_state': 'ASKING_END_LOCATION'
            },
            'ASKING_END_LOCATION': {
                'method': self.handle_end_location,
                'check': self.end_location_check,
                'next_state': 'ASKING_JOURNEY_TYPE'
            },
            'ASKING_JOURNEY_TYPE': {
                'method': self.handle_journey_type,
                'check': self.journey_type_check,
                'next_state': 'ASKING_OUTGOING_DATE_TIME'
            },
            'ASKING_OUTGOING_DATE_TIME': {
                'method': self.handle_out_date_time,
                'check': self.out_date_time_check,
                'next_state': 'ASKING_OUTGOING_TIME_CONSTRAINT'
            },
            'ASKING_OUTGOING_TIME_CONSTRAINT': {
                'method': self.handle_out_time_constraint,
                'check': self.out_time_constraint_check,
                'next_state': 'ASKING_PASSENGERS'
            },

            'ASKING_PASSENGERS': {
                'method': self.handle_passengers,
                'check': self.passengers_check,
                'next_state': 'CONFIRMING_TICKET_INFO'
            },
            'CONFIRMING_TICKET_INFO': {
                'method': self.handle_confirming_ticket_info,
                'check': self.confirm_ticket_info_check,
                'next_state': 'COMPLETED'
            },
            'ASKING_RAILCARD': {
                'method': self.handle_journey_details,
                'next_state': 'COMPLETED'
            },
            'ASKING_RETURN_DATE_TIME': {
                'method': self.handle_return_date_time,
                'check': self.ret_date_time_check,
                'next_state': 'ASKING_RETURN_TIME_CONSTRAINT'
            },
            'ASKING_RETURN_TIME_CONSTRAINT': {
                'method': self.handle_return_time_constraint,
                'check': self.ret_time_constraint_check,
                'next_state': 'ASKING_PASSENGERS'
            },

            'COMPLETED': {
                'method': self.completion,
                'next_state': 'COMPLETED'
            },
            'EXIT': {
                'method': None,
                'next_state': None
            }

        }


    def ret_date_time_check(self):
        return self.user_enquiry.ret_date and self.user_enquiry.ret_time is not None

    def ret_time_constraint_check(self):
        return self.user_enquiry.ret_time_condition is not None



    def handle_confirming_ticket_info(self, doc):
        result = yes_or_no(doc)
        if not result:
            self.state = 'CONFIRMING_TICKET_INFO'
        elif result == 'yes':
            self.state = 'COMPLETED'
        else:
            self.user_enquiry = Enquiry()
            self.state = 'ASKING_JOURNEY_DETAILS'

    def confirm_ticket_info_check(self):
        return None


    def handle_confirming_prediction(self, doc):
        result = yes_or_no(doc)
        if not result:
            self.state = 'CONFIRMING_PREDICTION'
        elif result == 'yes':
            self.state = 'COMPLETED_PREDICTION'
        else:
            self.prediction_enquiry = DelayPrediction()
            self.state = 'ASKING_PREDICTION_STATION'


    def confirm_prediction_check(self):
        print("confirming prediction check")
        return None

    def handle_journey_details(self, doc):
        recognise_station_directions(doc, self.user_enquiry)
        recognise_times(doc, self.user_enquiry, False)
        recognise_dates(doc, self.user_enquiry, False)
        recognise_single_or_return(doc, self.user_enquiry)
        self.state = self.dialogue_flow[self.state]['next_state']

    def handle_start_location(self, doc):
        self.user_enquiry.start_alpha3 = recognise_station(doc)
        self.state = self.dialogue_flow[self.state]['next_state']

    def start_location_check(self):
        print("check hit")
        return self.user_enquiry.start_alpha3 is not None

    def handle_end_location(self, doc):
        self.user_enquiry.end_alpha3 = recognise_station(doc)
        self.state = self.dialogue_flow[self.state]['next_state']

    def end_location_check(self):
        return self.user_enquiry.end_alpha3 is not None

    def handle_journey_type(self, doc):
        recognise_single_or_return(doc, self.user_enquiry)
        self.state = self.dialogue_flow[self.state]['next_state']

    def journey_type_check(self):
        return self.user_enquiry.journey_type is not None

    def handle_out_date_time(self, doc):
        recognise_dates(doc, self.user_enquiry, False)
        recognise_times(doc, self.user_enquiry, False)
        self.state = self.dialogue_flow[self.state]['next_state']

    def out_date_time_check(self):  # check
        return self.user_enquiry.out_date and self.user_enquiry.out_time is not None

    def handle_out_time_constraint(self, doc):
        recognise_time_mode(doc, self.user_enquiry, False)
        if self.user_enquiry.journey_type == JourneyType.RETURN:
            self.state = 'ASKING_RETURN_DATE_TIME'
        else:
            self.state = self.dialogue_flow[self.state]['next_state']

    def out_time_constraint_check(self):
        return self.user_enquiry.out_time_condition is not None

    def handle_passengers(self, doc):
        for i in range(1, len(doc)):
            if doc[i].text in ['adults', 'children', 'adult'] and doc[i - 1].ent_type_ == 'CARDINAL':
                count = int(doc[i - 1].text)
                if doc[i].text == 'adults':
                    self.user_enquiry.adults = count
                if doc[i].text == 'adult':
                    self.user_enquiry.adults = count
                elif doc[i].text == 'children':
                    self.user_enquiry.children = count
        self.state = self.dialogue_flow[self.state]['next_state']

    def passengers_check(self):
        return self.user_enquiry.adults or self.user_enquiry.children

    def completion_prediction(self):
       # print("completed prediction enquiry: ", self.prediction_enquiry)
        self.prediction_enquiry.london_leave_time = time_to_minutes(self.prediction_enquiry.london_leave_time)
        self.prediction_enquiry.norwich_planned_time = time_to_minutes(self.prediction_enquiry.norwich_planned_time)
        self.prediction_enquiry.planned_departure = time_to_minutes(self.prediction_enquiry.planned_departure)
        self.prediction_enquiry.actual_departure = self.prediction_enquiry.planned_departure + self.prediction_enquiry.departure_difference
        #print(self.prediction_enquiry)
        prediction = make_prediction(knn,le, scaler, self.prediction_enquiry)
        print(prediction)
        rounded_prediction = round(prediction[0])
        print(rounded_prediction)
        self.prediction_enquiry.norwich_arrival_time = self.prediction_enquiry.norwich_planned_time + rounded_prediction
        message = f"Your train is expected to arrive at Norwich at {minutes_to_time(self.prediction_enquiry.norwich_arrival_time)}"
        self.prediction_enquiry = DelayPrediction()
        self.state = 'ASKING_SERVICE'
        yield message


       #self.state = 'EXIT'

    def completion(self):
            # self.user_enquiry.out_time = fmt_natlang_time(self.user_enquiry.out_time)
            # print(self.user_enquiry.out_time)
            # url = get_search_url(self.user_enquiry)
            # print(url)
            print(self.user_enquiry.out_date)
            print(type( self.user_enquiry.out_date))
            self.user_enquiry.out_date = dateparser.parse(self.user_enquiry.out_date).strftime("%Y-%m-%d")
            print("completed enquiry: ", self.user_enquiry)
            # ## TODO: post demo, uncomment above and remove below
            print("completed enquiry: ", self.user_enquiry)
            print()
            print("FOLLOWING DEFAULTS FOR DEMO: ")
            print("| journey_type = JourneyType:SINGLE")
            print("| out_time_condition = TimeCondition.DEPART_AFTER")
            print("| out_date = 2024-05-10")
            # print("| children = 0")
            print()

            demo_enquiry = Enquiry(
                start_alpha3=self.user_enquiry.start_alpha3,
                end_alpha3=self.user_enquiry.end_alpha3,
                journey_type=JourneyType.SINGLE,
                out_time_condition=TimeCondition.DEPART_AFTER,
                out_time=fmt_natlang_time(self.user_enquiry.out_time),
                out_date="2024-06-10",
                adults=self.user_enquiry.adults,
                children=0 if self.user_enquiry.children is None else self.user_enquiry.children,
            )

            priced_journeys = get_journeys(demo_enquiry)
            print("priced_journeys: ", priced_journeys)
            print()
            self.user_enquiry = Enquiry()
            self.state = 'ASKING_SERVICE'


    def handle_return_time_constraint(self, doc):
        print("return time constraint hit")
        recognise_time_mode(doc, self.user_enquiry, True)
        self.state = self.dialogue_flow[self.state]['next_state']

    def handle_return_date_time(self, doc):
        print("return hit date time")
        recognise_dates(doc, self.user_enquiry, True)
        recognise_times(doc, self.user_enquiry, True)
        print(f"Return Date: {self.user_enquiry.ret_date}, Return Time: {self.user_enquiry.ret_time}")
        if not self.user_enquiry.ret_date:
            self.state = 'ASKING_RETURN_DATE_TIME'
        elif not self.user_enquiry.ret_time:
            self.state = 'ASKING_RETURN_DATE_TIME'
        self.state = self.dialogue_flow[self.state]['next_state']


    def handle_pred_station(self, doc):
        self.prediction_enquiry.station = recognise_station_pred(doc)
        if not self.prediction_enquiry.station:
            self.state = 'ASKING_PREDICTION_STATION'
        else:
            self.state = self.dialogue_flow[self.state]['next_state']

    def handle_pred_delay(self, doc):
        for token in doc:
            if token.ent_type_ == 'CARDINAL':
                self.prediction_enquiry.departure_difference = int(token.text)
                self.prediction_enquiry.planned_departure = datetime.datetime.now().strftime("%H:%M")
                self.prediction_enquiry.day_of_week = datetime.datetime.now().weekday()
                self.prediction_enquiry.month = datetime.datetime.now().month
        if not self.prediction_enquiry.departure_difference:
            self.state = 'ASKING_PREDICTION_DELAY'
        else:
            self.state = self.dialogue_flow[self.state]['next_state']

    def pred_delay_check(self):
        return self.prediction_enquiry.departure_difference is not None

    def handle_pred_london_leave_time(self, doc):
        for token in doc.ents:
            if token.label_ == 'TIME':
                self.prediction_enquiry.london_leave_time = fmt_natlang_time(token.text)
                if self.prediction_enquiry.london_leave_time:
                    self.state = self.dialogue_flow[self.state]['next_state']
            else:
                self.state = 'ASKING_PREDICTION_LONDON_LEAVE_TIME'

    def pred_london_leave_time_check(self):
        return self.prediction_enquiry.london_leave_time is not None

    def handle_pred_norwich_planned_time(self, doc):
        for token in doc.ents:
            if token.label_ == 'TIME':
                self.prediction_enquiry.norwich_planned_time = fmt_natlang_time(token.text)
                if self.prediction_enquiry.norwich_planned_time:
                    print("next state")
                    self.state = self.dialogue_flow[self.state]['next_state']
            else:
                self.state = self.dialogue_flow[self.state]['ASKING_PREDICTION_NORWICH_PLANNED_TIME']

    def pred_norwich_planned_time_check(self):
        return self.prediction_enquiry.norwich_planned_time is not None

    def pred_station_check(self):
        return self.prediction_enquiry.station is not None

    def handle_asking_service(self, doc):
        if recognise_chosen_service(doc) == 'ticket':
            self.state = 'ASKING_JOURNEY_DETAILS'
        elif recognise_chosen_service(doc) == 'delay':
            self.state = 'ASKING_PREDICTION_STATION'
        else:
            self.state = 'ASKING_SERVICE'

    def journey_type_check(self):
        return self.user_enquiry.journey_type is not None

    def process_input(self, user_input):
        doc = self.nlp(user_input)
        handler_method = self.dialogue_flow[self.state]['method']
        if handler_method:
            handler_method(doc)

    def ask_question(self, question):
        handler_check = self.dialogue_flow[self.state]['check']
        if handler_check():
            self.state = self.dialogue_flow[self.state]['next_state']
            return
        user_input = yield question
        if user_input.lower() == 'exit':
            sys.exit()
        self.process_input(user_input)
        # print(self.user_enquiry)
        print()

    def ask_service_check(self):
        return self.service is not None

    def run(self):


        while True:

            if self.state == 'ASKING_SERVICE':
                yield from self.ask_question(
                    "Hi ! i am a bot which can help you find cheapest tickets or predict delay for a train journey! , please tell me if you would like to use the delay prediction service or our ticket service ? ")
            elif self.state == 'ASKING_PREDICTION_STATION':
                yield from self.ask_question("Please provide me the current station where you are located")

            elif self.state == 'ASKING_PREDICTION_DELAY':
                yield from self.ask_question("Please tell me your current delay time at your station")

            elif self.state == 'ASKING_PREDICTION_LONDON_LEAVE_TIME':
                yield from self.ask_question("Please tell me the time you left London")

            elif self.state == 'ASKING_PREDICTION_NORWICH_PLANNED_TIME':
                yield from self.ask_question("Please tell me the time your meant to arrive at norwich")

            elif self.state == 'ASKING_JOURNEY_DETAILS':
                yield from self.ask_question(
                    "Hi ! i am a bot which can help you find cheapest tickets for your train journey ! please tell me your journey details: ")
            elif self.state == 'ASKING_START_LOCATION':
                yield from self.ask_question("Where are you travelling from? ")

            elif self.state == 'ASKING_END_LOCATION':
                yield from self.ask_question(
                    f"I see you travelling from {self.user_enquiry.start_alpha3}. Where are you travelling to? ")

            elif self.state == 'ASKING_JOURNEY_TYPE':
                yield from self.ask_question("Are you looking for a single or return ticket? ")

            elif self.state == 'ASKING_OUTGOING_TIME_CONSTRAINT':
                yield from self.ask_question(
                    f"Do you want to leave at {self.user_enquiry.out_time} or arrive by a certain time to your destination? ")

            elif self.state == 'ASKING_OUTGOING_DATE_TIME':
                yield from self.ask_question("What date and time would you like to travel at ? ")

            elif self.state == 'ASKING_RETURN_TIME_CONSTRAINT':
                yield from self.ask_question(
                    f"Do you want to leave at {self.user_enquiry.ret_time} or arrive to your destination by {self.user_enquiry.ret_time} for your return journey? ")

            elif self.state == 'ASKING_RETURN_DATE_TIME':
                yield from self.ask_question("What's your return date and time? ")

            elif self.state == 'ASKING_PASSENGERS':
                yield from self.ask_question(
                    f"How many adult and child tickets would you like to {self.user_enquiry.end_alpha3} ? ")

            elif self.state == 'ASKING_RAILCARD':
                yield from self.ask_question("Do you have a railcard? ")

            elif self.state == 'CONFIRMING_PREDICTION':
                yield from self.ask_question("Did you enter the correct details? ")

            elif self.state == 'CONFIRMING_TICKET_INFO':
                yield from self.ask_question("Did you enter the correct details for your ticket? ")

            elif self.state == 'COMPLETED_PREDICTION':
                yield from self.completion_prediction()

            elif self.state == 'COMPLETED':
                yield from self.completion()

            elif self.state == 'EXIT':
                break;
