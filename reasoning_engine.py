from user_enquiry import Enquiry
from npl_utils import recognise_station_directions, recognise_times
import sys
class ReasoningEngine:
    def __init__(self, nlp, station_df):
        self.nlp = nlp
        self.station_df = station_df
        self.user_enquiry = Enquiry(None, None, None, None, 1, 0)

    def process_input(self, user_input):
        doc = self.nlp(user_input)
        to_station, from_station = recognise_station_directions(doc, self.user_enquiry)
        time_action, time_value = recognise_times(doc, self.user_enquiry)
        print(f"From: {from_station}, To: {to_station}, Time: {time_value}, Action: {time_action}")
        if from_station != "":
            self.user_enquiry.setStartAlpha3(from_station)
        if to_station != "":
            self.user_enquiry.setEndAlpha3(to_station)
        if time_value != "":
            self.user_enquiry.setTime(time_value)
        if time_action != "":
            self.user_enquiry.setDepartOrArrive(time_action)



    def ask_question(self, question):
        user_input = input(question)
        if user_input.lower() == 'exit':
            sys.exit()
        self.process_input(user_input)

    def run(self):
        questions = [
            ('time', "Please enter the time of your journey: "),
            ('depart_or_arrive', "Please specify whether you want to depart or arrive: "),
            ('start_alpha3', "Please enter the start station: "),
            ('end_alpha3', "Please enter the end station: "),
            ('adults', "Please enter the number of adults: "),
            ('children', "Please enter the number of children: "),
        ]

        while True:
            for attr, question in questions:
                if getattr(self.user_enquiry, attr) in ["", None, 0]:
                    self.ask_question(question)
            print(self.user_enquiry)
            modify = input(
                "Do you want to modify any details? If yes, please specify the attribute (or type 'no' to continue): ")
            if modify.lower() == 'no':
                break
            elif modify in dict(questions):
                self.ask_question(dict(questions)[modify])