import spacy
from spacy.matcher import Matcher
from collections import Counter
from math import inf

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
    # todo сделать доп поиск по паттерну + свой мега способ
    for match_id, start, end in matches:
        string_id = spacy_nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        name = span.text.replace("startup", "")
        name = name.replace("Startup", "")
        startups.append(name)
    return startups


def get_startup_names2(text):
    doc = spacy_nlp(text.strip())

    organization_entities = list()
    org_pos = dict()
    for i in doc.ents:
        entry = str(i.lemma_).lower()
        text = text.replace(str(i).lower(), "")
        if i.label_ in ["ORG"]:
            organization_entities.append(entry)
            ent_list = org_pos.get(entry, list())
            ent_list.append((i.start_char + i.end_char) / 2)
            org_pos[entry] = ent_list

    counter = Counter(organization_entities)
    new_counter = counter.copy()
    for org1 in counter:
        for org2 in counter:
            if org1 == org2:
                continue
            if org1.lower() in org2.lower():
                new_counter[org2] += counter[org1]

    most_pop_sp = sorted(new_counter.items(), key=lambda s: -s[1])[:3]

    matcher = Matcher(spacy_nlp.vocab)
    patterns_word = [
        [{"LOWER": "startup"}]
    ]
    matcher.add("StartupWord", patterns_word)

    matches = matcher(doc)
    word_startup = list()

    for match_id, start, end in matches:
        string_id = spacy_nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        word_startup.append((start + end) / 2)

    sp_probs = list()
    for sp in most_pop_sp:
        positions = org_pos[sp[0]]
        min_dist = inf
        for pos in positions:
            dist = min([abs(pos - word_sp) for word_sp in word_startup])
            min_dist = min(min_dist, dist)
        count = new_counter[sp[0]]
        # print(sp[0], min_dist)
        sp_probs.append((sp[0], count + (1 / min_dist) * 60))

    return sorted(sp_probs, key=lambda s: -s[1])[0][0]
