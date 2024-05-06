import spacy
import pandas as pd
from itertools import combinations


def create_entity_ruler(nlp, station_data):
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
                for combination in combinations(short_name_words, len(short_name_words)):   # Remove the last two words ("rail", "station")
                    short_name_pattern = [{"LOWER": word.lower()} for word in short_name_words]
                    longname_patterns_no_rail_station.append({"label": "STATION", "pattern": short_name_pattern, "id": station_id})
                    names_station = long_name_words[-1:]
                    names_station_pattern = [{"LOWER": word.lower()} for word in names_station]
                    names_station_patterns.append({"label": "STATION", "pattern": names_station_pattern, "id": station_id})



    ruler = nlp.add_pipe("entity_ruler", before="ner",validate=True, config={"overwrite_ents": True})
    ruler.add_patterns(longname_patterns)
    ruler.add_patterns(names_station_patterns)
    ruler.add_patterns(longname_patterns_no_rail_station)
    ruler.add_patterns(name_patterns)
   # ruler.add_patterns(pattern3)

def main():
    # Load the English model
    nlp = spacy.load('en_core_web_trf')
    #nlp.add_pipe("merge_entities")

    column_names = ["name", "longname", "name_alias", "alpha3", "tiploc"]

    # Read the CSV file
    df = pd.read_csv('stations/stations.csv', names=column_names, skiprows=1)

    print(df.head())

    # Define the column names


    # Read the CSV file

    # Call the function to create the entity ruler
    create_entity_ruler(nlp, df)

    while True:
        user_input = input("Please enter a station name or 'exit' to quit: ").lower()

        # Break the loop if the user enters 'exit'
        if user_input == 'exit':
            break

        # Process the text
        doc = nlp(user_input)
        # Process the text



        print("\nNamed Entities:")
        for ent in doc.ents:
            print(f"Text: {ent.text}\tStart: {ent.start_char}\tEnd: {ent.end_char}\tLabel: {ent.label_}\tID: {ent.ent_id_}")

        for token in doc:
            if token.text in ['to', 'from'] and token.i < len(doc) - 1:
                next_token = doc[token.i + 1]
                if next_token.ent_type_ == 'STATION':
                    print(f"{token.text.upper()}_STATION: {next_token.text} (ID: {next_token.ent_id_})")


        print("")

if __name__ == "__main__":
    main()