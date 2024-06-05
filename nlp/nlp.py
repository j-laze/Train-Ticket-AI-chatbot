import dateparser
import pandas as pd
from itertools import combinations

from utils import JourneyType, TimeCondition, station_df



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
        station_words = station.split()

        pattern = [{"LOWER": {"FUZZY1": word.lower()}} for word in station_words]
        name_patterns.append({"label": "STATION", "pattern": pattern, "id": station_id})

        long_name = row['longname']
        if pd.notna(long_name):
            long_name = long_name.replace('-', ' ')
            long_name_words = long_name.split()
            long_name_pattern = [{"LOWER": {"FUZZY1": word.lower()}} for word in long_name_words]
            longname_patterns.append({"label": "STATION", "pattern": long_name_pattern, "id": station_id})

            # If the long name ends with "rail station", create a seperate pattern without these words
            if long_name.lower().endswith("rail station"):
                short_name_words = long_name_words[:-2]
                for combination in combinations(short_name_words,
                                                len(short_name_words)):  # remove the last two words("rail",  "station")
                    short_name_pattern = [{"LOWER": word.lower()} for word in short_name_words]
                    longname_patterns_no_rail_station.append(
                        {"label": "STATION", "pattern": short_name_pattern, "id": station_id})
                    names_station = long_name_words[-1:]
                    names_station_pattern = [{"LOWER": word.lower()} for word in names_station]
                    names_station_patterns.append(
                        {"label": "STATION", "pattern": names_station_pattern, "id": station_id})
    return longname_patterns, names_station_patterns, longname_patterns_no_rail_station, name_patterns




def create_entity_ruler(nlp, patterns):
    longname_patterns, names_station_patterns, longname_patterns_no_rail_station, name_patterns = patterns
    ruler = nlp.add_pipe("entity_ruler", before="ner", validate=True, config={"overwrite_ents": True})
    ruler.add_patterns(longname_patterns)
    ruler.add_patterns(names_station_patterns)
    ruler.add_patterns(longname_patterns_no_rail_station)
    ruler.add_patterns(name_patterns)


def recognise_station_pred(doc):
    station_alpha3 = recognise_station(doc)
    if station_alpha3:
        station_tiploc = station_df.loc[station_df['alpha3'] == station_alpha3, 'tiploc'].values[0]
        if station_tiploc in ['CLCHSTR', 'MANNGTR', 'IPSWICH', 'STWMRKT', 'DISS', 'CHLMSFD', 'STFD', 'SHENFLD',
                              'WITHAME', 'MRKSTEY', 'INGTSTN', 'KELVEDN', 'NEEDHAM', 'HFLPEVL']:
            return station_tiploc
    return None




def recognise_chosen_service(doc):
    for token in doc:
        if token.text.lower() == 'delay':
            return 'delay'
        elif token.text.lower() == 'ticket':
            return 'ticket'
    return None


def yes_or_no(doc):
    for token in doc:
        if token.text.lower() == 'yes':
            return 'yes'
        elif token.text.lower() == 'no':
            return 'no'
    return None


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


def recognise_time_mode(doc, user_enquiry, is_return):
    arrive_before_phrases = ['arrive before', 'arrive by', 'arrive at', 'arriving before', 'arriving by', 'arriving at']
    leave_after_phrases = ['leave after', 'leave by', 'leave at', 'leaving after', 'leaving by', 'leaving at']

    for i in range(len(doc) - 1):
        phrase = f"{doc[i].text.lower()} {doc[i + 1].text.lower()}"

        if phrase in arrive_before_phrases:
            if is_return:
                user_enquiry.ret_time_condition = TimeCondition.ARRIVE_BEFORE
            else:
                user_enquiry.out_time_condition = TimeCondition.ARRIVE_BEFORE
        elif phrase in leave_after_phrases:
            if is_return:
                user_enquiry.ret_time_condition = TimeCondition.DEPART_AFTER
            else:
                user_enquiry.out_time_condition = TimeCondition.DEPART_AFTER

    last_token = doc[-1].text.lower()
    if last_token in arrive_before_phrases:
        if is_return:
            user_enquiry.ret_time_condition = TimeCondition.ARRIVE_BEFORE
        else:
            user_enquiry.out_time_condition = TimeCondition.ARRIVE_BEFORE
    elif last_token in leave_after_phrases:
        if is_return:
            user_enquiry.ret_time_condition = TimeCondition.DEPART_AFTER
        else:
            user_enquiry.out_time_condition = TimeCondition.DEPART_AFTER


def recognise_times(doc, user_enquiry, is_return):
    arrive_before_phrases = ['arrive before', 'arrive by', 'arrive at', 'arriving before', 'arriving by', 'arriving at']
    leave_after_phrases = ['leave after', 'leave by', 'leave at', 'leaving after', 'leaving by', 'leaving at']
    for token in doc.ents:
        if token.label_ == 'TIME':
            if token.start > 1:
                prev_phrase = doc[token.start - 2:token.start].text.lower()
                if prev_phrase in arrive_before_phrases:
                    if is_return:
                        user_enquiry.ret_time_condition = 'arrive before'
                    else:
                        user_enquiry.out_time_condition = 'arrive before'
                elif prev_phrase in leave_after_phrases:
                    if is_return:
                        user_enquiry.ret_time_condition = 'leave after'
                    else:
                        user_enquiry.out_time_condition = 'leave after'
            if is_return:
                user_enquiry.ret_time = token.text
            else:
                user_enquiry.out_time = token.text


def recognise_dates(doc, user_enquiry, is_return):
    for token in doc.ents:
        if token.label_ == 'DATE':
            if is_return:
                user_enquiry.ret_date = dateparser.parse(token.text).strftime("%Y-%m-%d")
            else:
                user_enquiry.out_date = dateparser.parse(token.text).strftime("%Y-%m-%d")

## NOTE: assumes if pm not specified, time is am/24hr
## TODO: use some regex to handle more cases and make this more robust
def fmt_natlang_time(input_str):
    input_str = input_str.lower()

    if any(phrase in input_str for phrase in ["noon", "midday", "mid day"]):
        return "12:00"
    if any(phrase in input_str for phrase in ["midnight", "mid night"]):
        return "00:00"

    digits_str = "".join(c for c in input_str if c.isdigit())
    digit_count = len(digits_str)

    # if there are 0 or >4 digits, return None
    if digit_count == 0 or digit_count > 4:
        return None

    has_pm = "pm" in input_str

    ## if there is only 2 or 1 digits, it is the hour
    if digit_count <= 2:
        hour_int = int(digits_str)
        if has_pm:
            hour_int += 12
        if hour_int == 12:
            hour_int = 0
        if hour_int < 10:
            return f"0{hour_int}:00"
        return f"{hour_int}:00"

    ## if 3 or more digits but no colon return None
    if ":" not in input_str:
        return None

    ## if there are 3 digits, the first is the hour, the last 2 are the minutes
    if digit_count == 3:
        hour_int = int(digits_str[0])
        mins_int = int(digits_str[-2:])
        mins_str = f"{mins_int}" if mins_int >= 10 else f"0{mins_int}"
        if has_pm: hour_int += 12
        if hour_int < 10:
            return f"0{hour_int}:{mins_str}"
        return f"{hour_int}:{mins_str}"

    ## if there are 4 digits, the first 2 are the hour, the last 2 are the minutes
    hour_int = int(digits_str[:2])
    mins_str = int(digits_str[-2:])
    if has_pm:
        hour_int += 12
    return f"{hour_int}:{mins_str}"


def print_named_entities_debug(doc):
    print("\nNamed Entities:")
    for ent in doc.ents:
        print(f"Text: {ent.text}\tStart: {ent.start_char}\tEnd: {ent.end_char}\tLabel: {ent.label_}\tID: {ent.ent_id_}")

    print("")


def print_time_tokens(doc):
    print("\nTime Entities:")
    for ent in doc.ents:
        if ent.label_ == 'TIME':  # Check if the entity is a time entity
            print(
                f"Text: {ent.text}\tStart: {ent.start_char}\tEnd: {ent.end_char}\tLabel: {ent.label_}\tID: {ent.ent_id_}")
    print("")


def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes


def minutes_to_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02d}:{minutes:02d}"
