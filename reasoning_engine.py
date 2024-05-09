from utils import Enquiry
from nlp.nlp import recognise_station_directions, recognise_times, recognise_dates, recognise_station, \
    print_named_entities_debug, recognise_single_or_return, recognise_time_mode, print_time_tokens, fmt_natlang_time
import sys

from webscrape.splitmyfare import get_journeys
from utils import JourneyType, TimeCondition, Railcard
from utils import Enquiry, Journey


class DialogueFlowEngine:
    def __init__(self, nlp, station_df):
        self.nlp = nlp
        self.station_df = station_df
        self.user_enquiry = Enquiry()
        self.state = 'ASKING_JOURNEY_DETAILS'
        self.dialogue_flow = {
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
                'next_state': 'COMPLETED'
            },
            'ASKING_RAILCARD': {
                'method': self.handle_journey_details,
                'next_state': 'COMPLETED'
            },
            'ASKING_RETURN_DATE_TIME': {
                'method': self.handle_return_date_time,
                'next_state': 'ASKING_RETURN_TIME_CONSTRAINT'
            },
            'ASKING_RETURN_TIME_CONSTRAINT': {
                'method': self.handle_return_time_constraint,
                'next_state': 'ASKING_PASSENGERS'
            },

            'COMPLETED': {
                'method': self.completion,
                'next_state': None
            }
        }

    def handle_journey_details(self, doc):
        recognise_station_directions(doc, self.user_enquiry)
        recognise_times(doc, self.user_enquiry)
        recognise_single_or_return(doc, self.user_enquiry)
        self.state = self.dialogue_flow[self.state]['next_state']

    def handle_start_location(self, doc):
        self.user_enquiry.start_alpha3 = recognise_station(doc)
        self.state = self.dialogue_flow[self.state]['next_state']

    def start_location_check(self):
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
        recognise_dates(doc, self.user_enquiry)
        recognise_times(doc, self.user_enquiry)
        self.state = self.dialogue_flow[self.state]['next_state']

    def out_date_time_check(self):    # check
        return self.user_enquiry.out_date or self.user_enquiry.out_time

    def handle_out_time_constraint(self, doc):
        recognise_time_mode(doc, self.user_enquiry)
        self.state = self.dialogue_flow[self.state]['next_state']

    def out_time_constraint_check(self):
        return self.user_enquiry.out_time_condition


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



    def completion(self):
        user_input = input("Thank you for providing your journey details, are they correct?")
        if user_input.lower() == 'no':
            self.user_enquiry = Enquiry()
            self.state = 'ASKING_JOURNEY_DETAILS'
            self.state = self.dialogue_flow[self.state]['next_state']
        elif user_input.lower() == 'yes':
            # print("completed enquiry: ", self.user_enquiry)
            # self.user_enquiry.out_time = fmt_natlang_time(self.user_enquiry.out_time)
            # print(self.user_enquiry.out_time)
            # url = get_search_url(self.user_enquiry)
            # print(url)

            # ## TODO: post demo, uncomment above and remove below

            print("FOLLOWING DEFAULTS FOR DEMO: ")
            print("| journey_type = JourneyType:SINGLE")
            print("| out_time_condition = TimeCondition.DEPART_AFTER")
            print("| out_date = 2024-05-10")
            print("| children = 0")

            demo_enquiry = Enquiry(
                start_alpha3        = self.user_enquiry.start_alpha3,
                end_alpha3          = self.user_enquiry.end_alpha3,
                journey_type        = JourneyType.SINGLE,
                out_time_condition  = TimeCondition.DEPART_AFTER,
                out_time            = fmt_natlang_time(self.user_enquiry.out_time),
                out_date            = "2024-05-10",
                adults              = self.user_enquiry.adults,
                children            = 0,
            )

            priced_journeys = get_journeys(demo_enquiry)









    def handle_return_time_constraint(self, doc):
        if self.user_enquiry.journey_type == 'RETURN':
            self.state = 'ASKING_PASSENGERS'
        elif self.user_enquiry.journey_type == 'RETURN':
            self.state = 'ASKING_RETURN_DATE_TIME'
        self.state = self.dialogue_flow[self.state]['next_state']









    def handle_return_date_time(self, doc):
        recognise_dates(doc, self.user_enquiry)
        recognise_times(doc, self.user_enquiry)
        print(f"Return Date: {self.user_enquiry.ret_date}, Return Time: {self.user_enquiry.ret_time}")
        if not self.user_enquiry.ret_date:
            self.state = 'ASKING_RETURN_DATE_TIME'
        elif not self.user_enquiry.ret_time:
            self.state = 'ASKING_RETURN_DATE_TIME'
        self.state = self.dialogue_flow[self.state]['next_state']






            # TODO add a check to see if the station is in the station_df



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
        user_input = input(question)
        if user_input.lower() == 'exit':
            sys.exit()
        self.process_input(user_input)
        print(self.user_enquiry)



    def run(self):
        if self.state == 'ASKING_JOURNEY_DETAILS':
            self.ask_question("Hi ! i am a bot which can help you find cheapest tickets for your train journey ! please tell me your journey details: ")
        while True:
            if self.state == 'ASKING_START_LOCATION':
                self.ask_question("Where are you travelling from? ")

            elif self.state == 'ASKING_END_LOCATION':
                self.ask_question(f"I see you travelling from {self.user_enquiry.start_alpha3}. Where are you travelling to? ")

            elif self.state == 'ASKING_JOURNEY_TYPE':
                self.ask_question("Are you looking for a single or return ticket? ")

            elif self.state == 'ASKING_OUTGOING_TIME_CONSTRAINT':
                self.ask_question(f"Do you want to leave at {self.user_enquiry.out_time} or arrive by a certain time to your destination? ")

            elif self.state == 'ASKING_OUTGOING_DATE_TIME':
                self.ask_question("What time would you like to travel at ? ")

            elif self.state == 'ASKING_RETURN_TIME_CONSTRAINT':
                self.ask_question("Do you want to depart at or arrive by a certain time for your return journey? ")

            elif self.state == 'ASKING_RETURN_DATE_TIME':
                self.ask_question("What's your return date and time? ")

            elif self.state == 'ASKING_PASSENGERS':
                self.ask_question(f"How many adult and child tickets would you like to {self.user_enquiry.end_alpha3} ? ")

            elif self.state == 'ASKING_RAILCARD':
                self.ask_question("Do you have a railcard? ")


            elif self.state == 'COMPLETED':
                self.completion()


