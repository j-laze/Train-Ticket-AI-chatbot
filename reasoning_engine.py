from utils import Enquiry
from nlp.nlp import recognise_station_directions, recognise_times, recognise_dates, recognise_station, \
    print_named_entities_debug, recognise_single_or_return, recognise_time_mode
import sys


class DialogueFlowEngine:
    def __init__(self, nlp, station_df):
        self.nlp = nlp
        self.station_df = station_df
        self.user_enquiry = Enquiry()
        self.state = 'ASKING_JOURNEY_DETAILS'
        self.dialogue_flow = {
            'ASKING_JOURNEY_DETAILS': {
                'method': self.handle_journey_details,
                'next_state': 'ASKING_START_LOCATION'
            },
            'ASKING_START_LOCATION': {
                'method': self.handle_start_location,
                'next_state': 'ASKING_END_LOCATION'
            },
            'ASKING_END_LOCATION': {
                'method': self.handle_end_location,
                'next_state': 'ASKING_JOURNEY_TYPE'
            },
            'ASKING_JOURNEY_TYPE': {
                'method': self.handle_journey_type,
                'next_state': 'ASKING_OUTGOING_DATE_TIME'
            },
            'ASKING_OUTGOING_DATE_TIME': {
                'method': self.handle_out_date_time,
                'next_state': 'ASKING_OUTGOING_TIME_CONSTRAINT'
            },
            'ASKING_OUTGOING_TIME_CONSTRAINT': {
                'method': self.handle_out_time_constraint,
                'next_state': 'ASKING_PASSENGERS'
            },

            'ASKING_PASSENGERS': {
                'method': self.handle_journey_details,
                'next_state': 'ASKING_RAILCARD'
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
                'method': None,
                'next_state': None
            }
        }

    def handle_return_time_constraint(self, doc):
        if self.user_enquiry.journey_type == 'RETURN':
            self.state = 'ASKING_PASSENGERS'
        elif self.user_enquiry.journey_type == 'RETURN':
            self.state = 'ASKING_RETURN_DATE_TIME'
        self.state = self.dialogue_flow[self.state]['next_state']


    def handle_out_time_constraint(self, doc):
        if not self.user_enquiry.out_time_condition:
            recognise_time_mode(doc, self.user_enquiry)
            self.state = 'ASKING_OUTGOING_DATE_TIME'
        self.state = self.dialogue_flow[self.state]['next_state']





    def handle_out_date_time(self, doc):
        if not self.user_enquiry.out_date or not self.user_enquiry.out_time:
            recognise_dates(doc, self.user_enquiry)
            recognise_times(doc, self.user_enquiry)
            self.state = 'ASKING_JOURNEY_TYPE'
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


    def handle_journey_type(self, doc):
        recognise_single_or_return(doc)
        if not self.user_enquiry.journey_type:
            self.user_enquiry.journey_type = recognise_single_or_return()
            self.state = 'ASKING_END_LOCATION'
        self.state = self.dialogue_flow[self.state]['next_state']


    def handle_end_location(self, doc):
        if not self.user_enquiry.end_alpha3:
            self.user_enquiry.end_alpha3 = recognise_station(doc)
            self.state = 'ASKING_START_LOCATION'
        self.state = self.dialogue_flow[self.state]['next_state']


    def handle_start_location(self, doc):
        if not self.user_enquiry.start_alpha3:
            self.user_enquiry.start_alpha3 = recognise_station(doc)
            self.state = 'ASKING_JOURNEY_DETAILS'
        self.state = self.dialogue_flow[self.state]['next_state']

    def handle_journey_details(self, doc):
        recognise_station_directions(doc, self.user_enquiry)
        recognise_times(doc, self.user_enquiry)
        recognise_single_or_return(doc, self.user_enquiry)
        self.state = self.dialogue_flow[self.state]['next_state']

    def process_input(self, user_input):
        doc = self.nlp(user_input)
        handler_method = self.dialogue_flow[self.state]['method']
        if handler_method:
            handler_method(doc)


    def ask_question(self, question):
        user_input = input(question)
        if user_input.lower() == 'exit':
            sys.exit()
        self.process_input(user_input)
        print(self.user_enquiry)



    def run(self):
        while self.state != 'COMPLETED':
            if self.state == 'ASKING_JOURNEY_DETAILS':
                self.ask_question("What journey details would you like to provide? ")
            elif self.state == 'ASKING_START_LOCATION':
                self.ask_question("What's your starting location? ")
            elif self.state == 'ASKING_END_LOCATION':
                self.ask_question("What's your end location? ")
            elif self.state == 'ASKING_JOURNEY_TYPE':
                self.ask_question("Is this a single or return journey? ")
            elif self.state == 'ASKING_OUTGOING_TIME_CONSTRAINT':
                self.ask_question("Do you want to depart at or arrive by a certain time for your outgoing journey? ")
            elif self.state == 'ASKING_OUTGOING_DATE_TIME':
                self.ask_question("What's your outgoing date and time? ")
            elif self.state == 'ASKING_RETURN_TIME_CONSTRAINT':
                self.ask_question("Do you want to depart at or arrive by a certain time for your return journey? ")
            elif self.state == 'ASKING_RETURN_DATE_TIME':
                self.ask_question("What's your return date and time? ")
            elif self.state == 'ASKING_PASSENGERS':
                self.ask_question("How many adults and children are there? ")
            elif self.state == 'ASKING_RAILCARD':
                self.ask_question("Do you have a railcard? ")

