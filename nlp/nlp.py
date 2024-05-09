import pandas as pd
from itertools import combinations

from utils import JourneyType, TimeCondition


def create_patterns(station_data):
    name_patterns = []
    longname_patterns = []
    names_station_patterns = []
    longname_patterns_no_rail_station = []
    for index, row in station_data.iterrows():
        station = row['name']
        station_id = row['alpha3']
        if pd.isna(station_id):
            continue
        station = station.replace('-', ' ')
        station_words = station.split()  # Split the station name into words

        pattern = [{"LOWER": {"FUZZY1": word.lower()}} for word in station_words]
        name_patterns.append({"label": "STATION", "pattern": pattern, "id": station_id})

        long_name = row['longname']
        if pd.notna(long_name):
            long_name = long_name.replace('-', ' ')
            long_name_words = long_name.split()
            long_name_pattern = [{"LOWER": {"FUZZY1": word.lower()}} for word in long_name_words]
            longname_patterns.append({"label": "STATION", "pattern": long_name_pattern, "id": station_id})

            # If the long name ends with "rail station", create an additional pattern without these words
            if long_name.lower().endswith("rail station"):
                short_name_words = long_name_words[:-2]
                for combination in combinations(short_name_words,
                                                len(short_name_words)):  # Remove the last two words ("rail", "station")
                    short_name_pattern = [{"LOWER": word.lower()} for word in short_name_words]
                    longname_patterns_no_rail_station.append(
                        {"label": "STATION", "pattern": short_name_pattern, "id": station_id})
                    names_station = long_name_words[-1:]
                    names_station_pattern = [{"LOWER": word.lower()} for word in names_station]
                    names_station_patterns.append(
                        {"label": "STATION", "pattern": names_station_pattern, "id": station_id})
    return longname_patterns, names_station_patterns, longname_patterns_no_rail_station, name_patterns


def read_csv_to_df():
    column_names = ["name", "longname", "name_alias", "alpha3", "tiploc"]
    # Read the CSV file
    df = pd.read_csv('data/stations.csv', names=column_names, skiprows=1)

    return df


def create_entity_ruler(nlp, patterns):
    longname_patterns, names_station_patterns, longname_patterns_no_rail_station, name_patterns = patterns
    ruler = nlp.add_pipe("entity_ruler", before="ner", validate=True, config={"overwrite_ents": True})
    ruler.add_patterns(longname_patterns)
    ruler.add_patterns(names_station_patterns)
    ruler.add_patterns(longname_patterns_no_rail_station)
    ruler.add_patterns(name_patterns)


def recognise_station_directions(doc, user_enquiry):
    for token in doc:
        if token.text in ['to', 'from'] and token.i < len(doc) - 1:
            next_token = doc[token.i + 1]
            if next_token.ent_type_ == 'STATION':
                if token.text == 'to':
                    user_enquiry.end_alpha3 = next_token.ent_id_
                elif token.text == 'from':
                    user_enquiry.start_alpha3 = next_token.ent_id_

def recognise_station(doc):
    station_id = None
    for token in doc:
        if token.ent_type_ == 'STATION':
            station_id = token.ent_id_
    return station_id


def recognise_single_or_return(doc, user_enquiry):
    for token in doc:
        if token.text in ['single', 'return']:
            if token.text == 'single':
                user_enquiry.journey_type = JourneyType.SINGLE
            elif token.text == 'return':
                user_enquiry.journey_type = JourneyType.RETURN


def recognise_time_mode(doc, user_enquiry):
    arrive_before_phrases = ['arrive before', 'arrive by', 'arrive at', 'arriving before', 'arriving by', 'arriving at']
    leave_after_phrases = ['leave after', 'leave by', 'leave at', 'leaving after', 'leaving by', 'leaving at']

    for i in range(len(doc) - 1):  # Iterate over the tokens in the document, excluding the last token
        phrase = f"{doc[i].text.lower()} {doc[i + 1].text.lower()}"  # Form a phrase with the current token and the next token

        if phrase in arrive_before_phrases:
            user_enquiry.out_time_condition = TimeCondition.ARRIVE_BEFORE
        elif phrase in leave_after_phrases:
            user_enquiry.out_time_condition = TimeCondition.DEPART_AFTER

    # Check the last token separately
    last_token = doc[-1].text.lower()
    if last_token in arrive_before_phrases:
        user_enquiry.out_time_condition = TimeCondition.ARRIVE_BEFORE
    elif last_token in leave_after_phrases:
        user_enquiry.out_time_condition = TimeCondition.DEPART_AFTER

def recognise_times(doc,
                    user_enquiry):  # TODO: maybe add a return condition, so i know if the time is for the return journey
    arrive_before_phrases = ['arrive before', 'arrive by', 'arrive at', 'arriving before', 'arriving by', 'arriving at']
    leave_after_phrases = ['leave after', 'leave by', 'leave at', 'leaving after', 'leaving by', 'leaving at']

    for token in doc.ents:
        if token.label_ == 'TIME':
            # Check the previous two tokens to see if they form a phrase
            if token.start > 1:
                prev_phrase = doc[token.start - 2:token.start].text.lower()
                if prev_phrase in arrive_before_phrases:
                    user_enquiry.out_time_condition = 'arrive before'
                elif prev_phrase in leave_after_phrases:
                    user_enquiry.out_time_condition = 'leave after'
            user_enquiry.out_time = token.text


def recognise_dates(doc, user_enquiry):  # maybe add a return condition, so i know if the date is for the return journey
    for token in doc.ents:
        if token.label_ == 'DATE':
            if user_enquiry.JourneyType == 'SINGLE':
                user_enquiry.out_date = token.text
            if user_enquiry.JourneyType == 'RETURN':
                user_enquiry.ret_date = token.text


def print_named_entities_debug(doc):
    print("\nNamed Entities:")
    for ent in doc.ents:
        print(f"Text: {ent.text}\tStart: {ent.start_char}\tEnd: {ent.end_char}\tLabel: {ent.label_}\tID: {ent.ent_id_}")

    print("")


def print_time_tokens(doc):
    print("\nTime Entities:")
    for ent in doc.ents:
        if ent.label_ == 'TIME':  # Check if the entity is a time entity
            print(f"Text: {ent.text}\tStart: {ent.start_char}\tEnd: {ent.end_char}\tLabel: {ent.label_}\tID: {ent.ent_id_}")
    print("")
