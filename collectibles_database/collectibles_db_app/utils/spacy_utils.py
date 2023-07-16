import spacy
from fuzzywuzzy import process
from .country_list import get_country_names

def extract_entities(text, user):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text) if text else nlp("")
    entities = []

    for token in doc:
        best_match, score = process.extractOne(token.text, get_country_names(user))
        if score >= 80: 
            entities.append((best_match, "GPE"))
        else:
            entities.append((token.text, token.ent_type_))

    return entities
