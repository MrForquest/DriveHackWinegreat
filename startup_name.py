import spacy
from spacy.matcher import Matcher
from collections import Counter

spacy_nlp = spacy.load('en_core_web_trf')


def get_startup_names(text):
    doc = spacy_nlp(text.strip())

    organization_entities = list()

    for i in doc.ents:
        entry = str(i.lemma_).lower()
        text = text.replace(str(i).lower(), "")
        if i.label_ in ["ORG"]:
            organization_entities.append(entry)

    counter = Counter(organization_entities)

    matcher = Matcher(spacy_nlp.vocab)
    patterns = [
        [{"LOWER": "startup"}, {"ENT_TYPE": {"IN": ["ORG", "PERSON"]}}],
        [{"LOWER": "startup"}, {"ENT_TYPE": {"IN": ["ORG", "PERSON"]}},
         {"ENT_TYPE": {"IN": ["ORG", "PERSON"]}}]
    ]

    matcher.add("StartUp", patterns)

    matches = matcher(doc)
    startups = list()
    for match_id, start, end in matches:
        string_id = spacy_nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        name = span.text.replace("startup", "")
        name = name.replace("Startup", "")
        startups.append(name)
    return startups
