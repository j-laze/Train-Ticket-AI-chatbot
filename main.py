import pickle

import pandas as pd
import spacy

from nlp.nlp import create_patterns, create_entity_ruler, time_to_minutes, minutes_to_time
from dialog_flow_engine import DialogueFlowEngine
from utils import station_df
import preprocessData.processData as processData
from sklearn.preprocessing import LabelEncoder, StandardScaler

from gui_utils import *

from models.linearRegressionModel import create_and_train_linear_regression
from models.knnRegressionModel import create_and_train_knn

# df = pd.read_csv('data2.csv')
# df = df.dropna()
# knn, le, scaler = create_and_train_knn(df)
#
#
#
# def save_model(knn, le, scaler):
#     with open('models/dumpedModels/knnModel.pkl', 'wb') as file:
#         pickle.dump(knn, file)
#     with open('models/dumpedModels/labelEncoder.pkl', 'wb') as file:
#         pickle.dump(le, file)
#     with open('models/dumpedModels/scaler.pkl', 'wb') as file:
#         pickle.dump(scaler, file)
#
# save_model(knn, le, scaler)




class App(CTk):
    def __init__(self):
        super().__init__()

        self.messages: list[(str, str)] = []  ## [(sent_by, text),...]

        set_appearance_mode(APPEARANCE_MODE)
        set_default_color_theme(COLOUR_THEME)

        self.geometry(APP_GEOMETRY)
        self.title(APP_NAME)

        self.frame = CTkFrame(master=self)
        self.frame.pack(fill=FRAME_FILL, expand=FRAME_EXPAND, padx=PADX * 3, pady=PADY * 3)

        self.header = CTkLabel(master=self.frame, text=APP_NAME, font=HEADER_FONT)
        self.header.pack(pady=(2 * PADY, PADY), padx=PADX)

        self.conversation = Conversation(master=self.frame)

        # self.entry = CTkEntry(master=self.frame, font=MSG_FONT, placeholder_text="...", width=CONVO_WIDTH + 2 * PADX)
        self.entry = CTkTextbox(master=self.frame, font=MSG_FONT, width=CONVO_WIDTH + 2 * PADX)
        self.entry.bind("<Return>", self.send_user_msg)
        self.entry.pack(padx=PADX, pady=PADY)

        self.nlp = spacy.load('en_core_web_sm')


        self.patterns = create_patterns(station_df)
        create_entity_ruler(self.nlp, self.patterns)

        self.engine = DialogueFlowEngine(self.nlp, station_df)

        self.run_gen = self.engine.run()
        question = next(self.run_gen)

        self.send_bot_msg(question)

        # self.send_bot_msg("INITIAL PROMPT")

    def waiting_for_user(self):
        return self.messages[-1][0] == "bot"

    def waiting_for_bot(self):
        return not self.waiting_for_user()

    def send_user_msg(self, _):
        if self.waiting_for_user():
            user_msg = self.entry.get("1.0", "end").strip()
            self.messages.append(("usr", user_msg))
            self.conversation.add("usr", user_msg)

            next_question = self.run_gen.send(user_msg)
            self.send_bot_msg(next_question)

            self.entry.delete("0.0", "end-1c")
            return "break"

    def send_bot_msg(self, msg):
        self.messages.append(("bot", msg))
        self.conversation.add("bot", msg)


def main():
    app = App()
    app.mainloop()

    #df = pd.read_csv('data2.csv')
    # df = df.dropna()




if __name__ == '__main__':
    main()
