#!/usr/bin/env python3

import inflect
import nltk
import json
import random
import re
import mlconjug

IRREGULAR = {
    "eat": ["eating", "ate", "eaten"],
    "sleep with": ["sleeping", "slept with", "slept with"],
    "x-ray": ["x-raying", "x-rayed", "x-rayed"],
    "yeet": ["yeeting", "yeeted", "yoted"],
}

SCHEMA = [
    "My [ORGANISM] [ACTION:ps] [COMMONOBJECT:a].",
    "The [UTILITY] went out",
    "My [ORGANISM] [ACTION_NO_OBJECT:ps] to its death.",
    "My siblings threw [OBJECT:a] at me and it broke my [BODY_PART].",
    "I got bit by [ORGANISM:a]",
    "[ORGANISM:a:c] broke into my house and I'm hiding",
    "Can't, I'm in [PLACE]",
    "I broke my [BODY_PART]",
    "I have [DISEASE] and I know you're going to make it worse.",
    "I'm searching WebMD and I think I have [DISEASE].",
    "I got my fingers stuck in [OBJECT:a]",
    "Sorry, but if I open my camera [ORGANISM:p] from [PLACE] will come and [ACTION] me.",
    "Internet Explorer doesn't support [ACTION:pc] right now.",
    "It's [DIGIT][DIGIT]:[DIGIT][DIGIT] AM on my end right now",
]

WEIGHTS = None

p = inflect.engine()
p.classical(zero=False,herd=True,persons=False,ancient=False)
conjug = mlconjug.Conjugator(language='en')

def pluralize(word):
    noun = word
    # do some nlp to determine what to pluralize
    if ' ' in word:
        noun = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(word)) if pos[:2] == 'NN'][-1]
    return re.sub(noun, p.plural(noun), word)

def choose_scheme(d):
    global WEIGHTS
    if WEIGHTS is not None:
        return random.choices(population=SCHEMA, weights=WEIGHTS, k=1)[0]
    # first calculate weights
    weights = []
    for s in SCHEMA:
        count = 0
        for key in re.findall(r"\[([\w_]+)(?::\w+)*\]", s):
            count += len(d[key])
        weights.append(count)
    total_weights = sum(weights) or 1
    WEIGHTS = list(map(lambda w: w / total_weights, weights))
    return random.choices(population=SCHEMA, weights=WEIGHTS, k=1)[0]

def excuse_from_scheme(scheme, d):
    def replace(match):
        flags = set(match[2].split(':')) if match[2] is not None else []
        sub = random.choice(tuple(d[match[1]]))

        if 'ps' in flags: # past simple
            if sub in IRREGULAR:
                sub = IRREGULAR[sub][1]
            else:
                sub = conjug.conjugate(sub).conjug_info["indicative"]["indicative past tense"]["1p"]
        if 'pc' in flags: # present continuous
            if sub in IRREGULAR:
                sub = IRREGULAR[sub][0]
            else:
                sub = conjug.conjugate(sub).conjug_info["indicative"]["indicative present continuous"]["1p 1p"]
        if 'a' in flags: # a/an
            sub = p.a(sub)
        if 'p' in flags: # pluralize
            sub = pluralize(sub)
        if 'c' in flags: # capitalize
            sub = sub[0].upper() + sub[1:]

        return sub

    return re.sub(r"\[([\w_]+)((:\w+)*)\]", replace, scheme)

if __name__ == "__main__":
    with open("words.json", "r") as f:
        d = json.load(f)

        for scheme in SCHEMA:
            print(excuse_from_scheme(scheme, d))
