import spacy
from spacy.matcher import Matcher
from collections import Counter
from math import inf

spacy_nlp = spacy.load('en_core_web_trf')


def get_startup_names(text):
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
    patterns_name = [
        [{"LOWER": "startup"}, {"ENT_TYPE": {"IN": ["ORG", "PERSON"]}}],
        [{"LOWER": "startup"}, {"ENT_TYPE": {"IN": ["ORG", "PERSON"]}},
         {"ENT_TYPE": {"IN": ["ORG", "PERSON"]}}]
    ]
    matcher.add("StartupName", patterns_name)

    patterns_word = [
        [{"LOWER": "startup"}]
    ]
    matcher.add("StartupWord", patterns_word)

    matches = matcher(doc)
    word_startup = list()
    name_startup = list()
    for match_id, start, end in matches:
        string_id = spacy_nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        if string_id == "StartupWord":
            word_startup.append((start + end) / 2)
        if string_id == "StartupName":
            name = span.text.replace("startup", "").replace("Startup", "").strip()
            name_startup.append(name)

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
    sp_names = sorted(sp_probs, key=lambda s: -s[1])
    sp_names = [sp[0].strip() for sp in sp_names]
    abs_sp = list()
    if name_startup:
        abs_sp = name_startup
    else:
        abs_sp.append(sp_names[0])
    return abs_sp


print("стартуем")
file = open("example_text_transport8.TXT", "r")
text_ = file.read()
file.close()
print(get_startup_names(text_))
