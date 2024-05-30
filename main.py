import pandas as pd
import spacy

from nlp.nlp import create_patterns, read_csv_to_df, create_entity_ruler
from reasoning_engine import DialogueFlowEngine
import preprocessData.processData as processData
from sklearn.preprocessing import LabelEncoder, StandardScaler

from gui_utils import *

# from models.linearRegressionModel import create_and_train_linear_regression

class App(CTk):
    def __init__(self):
        super().__init__()
        
        self.messages: list[(str, str)] = [] ## [(sent_by, text),...]

        set_appearance_mode(APPEARANCE_MODE)
        set_default_color_theme(COLOUR_THEME)

        self.geometry(APP_GEOMETRY)
        self.title(APP_NAME)
        
        self.frame = CTkFrame(master=self)
        self.frame.pack(fill=FRAME_FILL, expand=FRAME_EXPAND, padx=PADX*3, pady=PADY*3)

        self.header = CTkLabel(master=self.frame, text=APP_NAME, font=HEADER_FONT)
        self.header.pack(pady=(2*PADY, PADY), padx=PADX)
        
        self.conversation = Conversation(master=self.frame)
        
        self.entry = CTkEntry(master=self.frame, font=MSG_FONT, placeholder_text="...", width=CONVO_WIDTH+2*PADX)
        self.entry.bind("<Return>", self.send_user_msg)
        self.entry.pack(padx=PADX, pady=PADY)
        



         
        # self.send_bot_msg("INITIAL PROMPT")
        
    def waiting_for_user(self):
        return self.messages[-1][0] == "bot"
    
    def waiting_for_bot(self):
        return not self.waiting_for_user()
        
    def send_user_msg(self, _):
        if self.waiting_for_user():
            self.messages.append(("usr", self.entry.get()))
            self.conversation.add("usr", self.entry.get())
            self.entry.delete(0, "end")
            
    def send_bot_msg(self, msg):
        self.messages.append(("bot", msg))
        self.conversation.add("bot", msg)




def main():
    def time_to_minutes(time_str):
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    def minutes_to_time(minutes_list):
        minutes = int(minutes_list[0])
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours:02d}:{minutes:02d}"
    
    

    nlp = spacy.load('en_core_web_sm')
    station_df = read_csv_to_df()

    patterns = create_patterns(station_df)
    create_entity_ruler(nlp, patterns)

    engine = DialogueFlowEngine(nlp, station_df)

    run_generator = engine.run() 
    question = next(run_generator)  
    print(question)

    user_response = "delay"  

    next_question = run_generator.send(user_response)  
    print(next_question)
    
    



   #
   #  df = pd.read_csv('data2.csv')
   #  #df = pd.read_csv('processed_data.csv')
   #
   #
   #
   #  lr, le, scaler = create_and_train_linear_regression(df)
   #
   #
   # # knn_model, le, scaler = model.create_and_train_knn(df)
   #
   #  def time_to_minutes(time_str):
   #      hours, minutes = map(int, time_str.split(':'))
   #      return hours * 60 + minutes
   #
   #  print(time_to_minutes("12:30"))  # Outputs: 750
   #
   #  test_values = {
   #      'station': ['MANNGTR'],
   #      'day_of_week': [4],
   #      'month': [3],
   #      'actual_departure': [time_to_minutes("18:10")],
   #      'departure_difference': [10.0],
   #      'planned_departure': [time_to_minutes("18:00")],
   #      'london_leave_time': [time_to_minutes("16:40")],
   #      'london_planned_time': [time_to_minutes("16:40")],
   #      'norwich_planned_time': [time_to_minutes("18:35")],
   #      'london_leave_difference': [0.0],
   #  }
   #
   #  test_df = pd.DataFrame(test_values)
   #
   #  test_df['station'] = le.transform(test_df['station'])
   #
   #  test_df = scaler.transform(test_df)
   #
   #  single_pred = lr.predict(test_df)
   #  print(minutes_to_time(single_pred))





if __name__ == '__main__':
    main()