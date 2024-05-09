
def recognise_station_directions(doc, user_enquiry):
    to_station_id = user_enquiry.start_alpha3
    from_station_id = user_enquiry.end_alpha3
    for token in doc:
        if token.text in ['to', 'from'] and token.i < len(doc) - 1:
            next_token = doc[token.i + 1]
            if next_token.ent_type_ == 'STATION':
                print(f"Token: {next_token.text}, ID: {next_token.ent_id_}")  # Debug print statement
                if token.text == 'to':
                    to_station_id = next_token.ent_id_
                elif token.text == 'from':
                    from_station_id = next_token.ent_id_
    return to_station_id, from_station_id

def recognise_times(doc, user_enquiry):
    arrive_before_phrases = ['arrive before', 'arrive by', 'arrive at', 'arriving before', 'arriving by', 'arriving at']
    leave_after_phrases = ['leave after', 'leave by', 'leave at', 'leaving after', 'leaving by', 'leaving at']
    time_value = user_enquiry.time
    time_action = user_enquiry.depart_or_arrive
    for token in doc.ents:
        if token.label_ == 'TIME':
            time_value = token.text
            # Check the previous two tokens to see if they form a phrase
            if token.start > 1:
                prev_phrase = doc[token.start - 2:token.start].text.lower()
                if prev_phrase in arrive_before_phrases:
                    time_action = 'arrive before'
                elif prev_phrase in leave_after_phrases:
                    time_action = 'leave after'
    return time_action, time_value
def print_named_entities_debug(doc):
    print("\nNamed Entities:")
    for ent in doc.ents:
        print(f"Text: {ent.text}\tStart: {ent.start_char}\tEnd: {ent.end_char}\tLabel: {ent.label_}\tID: {ent.ent_id_}")

    print("")