#!/usr/bin/env python3

import re
import json
import nltk 

"""Conjugate verbs to tenses"""

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

d = {
    "ACTION": {
        "absquatulate",
        "bang",
        "beat",
        "bite",
        "bleach",
        "boil",
        "bomb",
        "choke",
        "defenestrate",
        "destroy",
        "discombobulate",
        "eat",
        "eliminate",
        "excrete",
        "exsanguinate",
        "freeze",
        "fry",
        "harass",
        "haunt",
        "kiss",
        "lick",
        "marry",
        "pickle",
        "sleep with",
        "smite",
        "tase",
        "undress",
        "vex",
        "x-ray",
        "yeet",
    },
    "ACTION_OBJECT": {
        "burn",
        "eat",
        "jump",
        "freeze",
        "sleep",
        "fall",
        "drink",
    }
}

ORGANISM = {
    "alligator",
    "dog",
}

with open("dnd-monsters.txt", "r") as f:
    ORGANISM |= { m for m in f.readlines() }

FORMS = [
    "My [ORGANISM] [ACTION:ps] the [OBJECT].",
    "My [ORGANISM] [ACTIONED:ps] to its death.",
]

IRREGULAR = {
    "add": [None, None, "added"],
    "beat": [None, "beat", None],
    "bite": [None, "bit", None],
    "break": [None, "broke", "broken"],
    "cut": [None, "cut", "cut"],
    "drive": [None, "drove", None],
    "drink": [None, "drank", "drunk"],
    "eat": [None, "ate", "eaten"],
    "fall": [None, "fell", "fallen"],
    "fight": [None, "fought", "fought"],
    "fly": [None, "flew", "flown"],
    "freeze": [None, "froze", "frozen"],
    "fry": [None, "fried", "fried"],
    "sleep": [None, "slept", "slept with"],
    "sleep with": ["sleeping", "slept with", "slept with"],
    "smite": [None, None, "smote"],
}

dictionary = nltk.corpus.cmudict.dict()

def is_vowel(c):
    return any([c == 'a', c == 'e', c == 'i', c == 'o', c == 'u'])

def nsyl(word):
    try:
        return [len(list(y for y in x if y[-1].isdigit())) for x in dictionary[word.lower()]]
    except KeyError:
        return -1

def conjugate_present_continuous(verb):
    if verb in IRREGULAR and IRREGULAR[verb][0] is not None:
        return IRREGULAR[verb][0]

    if verb[-1] is 'e':
        return verb[0:-1] + "ing"
    if verb[-2:-1] is 'ie':
        return verb[0:-2] + "ying"
    if verb[-1] is 'w' or verb[-1] is 'x' or verb[-1] is 'y':
        return verb + "ing"
    if nsyl(verb) == 1 and is_vowel(verb[-2]) and not (is_vowel(verb[-1]) or is_vowel(verb[-3])):
        return verb + verb[-1] + "ing"
    
    return verb + "ing"

def conjugate_past_simple(verb):
    if verb in IRREGULAR and IRREGULAR[verb][1] is not None:
        return IRREGULAR[verb][1]

    if verb[-1] is 'e':
        return verb + "d"
    if verb[-1] is 'y':
        return verb[0:-1] + "ied"

    return verb + "ed"

if __name__ == "__main__":
    keys = list(d.keys())
    for k in keys:
        d[k + "ING"] = {conjugate_present_continuous(v) for v in d[k]}
        d[k + "ED"] = {conjugate_past_simple(v) for v in d[k]}
    with open("actions.json", "w") as f:
        json.dump(d, f, cls=SetEncoder, indent=2)

