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
}

SCHEMA = [
    "My [ORGANISM] [ACTION:ps] [COMMONOBJECT:a].",
    "My [ORGANISM] [ACTION_NO_OBJECT:ps] to its death.",
    "if I open my camera [ORGANISM:p] from [PLACE] will come and [ACTION] me.",
    "Internet Explorer doesn't support [ACTION:pc] right now.",
]

p = inflect.engine()
p.classical(zero=False,herd=True,persons=False,ancient=False)
conjug = mlconjug.Conjugator(language='en')

def pluralize(word):
    noun = word
    # do some nlp to determine what to pluralize
    if ' ' in word:
        noun = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(word)) if pos[:2] == 'NN'][-1]
    return re.sub(noun, p.plural(noun), word)
        

def excuse_from_scheme(scheme, d):
    def replace(match):
        flags = set(match[2].split(':')) if match[2] is not None else []
        sub = random.choice(tuple(d[match[1]])).lower()

        if 'a' in flags: # a/an
            sub = p.a(sub)
        if 'p' in flags: # pluralize
            sub = pluralize(sub)
        if 'ps' in flags: # past simple
            if sub in IRREGULAR:
                sub = IRREGULAR[sub][1]
            sub = conjug.conjugate(sub).conjug_info["indicative"]["indicative past tense"]["1p"]
        if 'pc' in flags: # present continuous
            if sub in IRREGULAR:
                sub = IRREGULAR[sub][0]
            sub = conjug.conjugate(sub).conjug_info["indicative"]["indicative present continuous"]["1p 1p"]

        return sub

    return re.sub(r"\[([\w_]+)((:\w+)*)\]", replace, scheme)

if __name__ == "__main__":
    with open("words.json", "r") as f:
        d = json.load(f)

        for scheme in SCHEMA:
            print(excuse_from_scheme(scheme, d))
