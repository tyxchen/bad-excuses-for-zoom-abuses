#!/usr/bin/env python3

import json
import nltk 

"""Conjugate verbs to tenses"""

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

ACTION = {
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
    "puke",
    "sleep with",
    "smite",
    "tase",
    "undress",
    "vex",
    "x-ray",
    "yeet",
}

ACTION_NO_OBJECT = ACTION - {
    "beat",
    "destroy",
    "discombobulate",
    "eliminate",
    "harass",
    "haunt",
    "marry",
    "pickle",
    "sleep with",
    "smite",
    "tase",
    "vex",
}

ORGANISM = {
    "alligator",
    "dog",
    "goose",
}

with open("dnd-monsters.txt", "r") as f:
    ORGANISM |= { m.strip() for m in f.readlines() }

COMMONOBJECT = {
    "cat",
    "bowling ball",
    "zoo",
    "glass bottle",
    "textbook",
}

PLACE = {
    "The Nether",
    "Hogwarts",
    "Ottawa",
}

if __name__ == "__main__":
    d = {
        "ACTION": ACTION,
        "ACTION_NO_OBJECT": ACTION_NO_OBJECT,
        "COMMONOBJECT": COMMONOBJECT,
        "PLACE": PLACE,
        "ORGANISM": ORGANISM
    }

    with open("words.json", "w") as f:
        json.dump(d, f, cls=SetEncoder, indent=2, sort_keys=True)

