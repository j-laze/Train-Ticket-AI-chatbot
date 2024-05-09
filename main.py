import spacy

from nlp.nlp import create_patterns, read_csv_to_df, create_entity_ruler
from reasoning_engine import DialogueFlowEngine






def main():
    nlp = spacy.load('en_core_web_trf')
    station_df = read_csv_to_df()
    patterns = create_patterns(station_df)
    create_entity_ruler(nlp, patterns)
    engine = DialogueFlowEngine(nlp, station_df)
    engine.run()


if __name__ == "__main__":
    main()