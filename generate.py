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
    "execute",
    "exsanguinate",
    "freeze",
    "fry",
    "guillotine"
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
    "aardvark",
    "alligator",
    "dog",
    "goose",
}

with open("dnd-monsters.txt", "r") as f:
    ORGANISM |= { m.strip().lower() for m in f.readlines() }

COMMONOBJECT = {
    "cat",
    "bowling ball",
    "zoo",
    "glass bottle",
    "textbook",
    "lamp",
    "window",
}

PLACE = {
    "The Nether",
    "Hogwarts",
    "Ottawa",
    "Hell",
    "MC",
    "Swamps of Dagobah",
    "Narnia",
    "Edmonton",
    "Hyrule",
    "Oz",
    "Kara-Tur",
    "Essos",
    "Tatooine",
    "Naboo",
    "Zzyzx",
    "Hell, Michigan",
    "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch",
    "Mordor",
}

UTILITY = {
    "hydro",
    "sun",
    "flux capacitor",
    "cremation furnace",
    "crack supply",
    "nuclear reactor",
    "red matter generator",
    "carrier pigeon service",
}

BODY_PART = {
    "back",
    "stomach",
    "knee",
    "hip",
    "neck",
    "intestine",
    "jaw",
}

DISEASE = {
    "pneumonia",
    "bronchitis",
    "cancer",
    "ebola",
    "ligma",
    "covid-19",
    "herpes",
    "chlamydia",
    "mad cow disease",
    "dysentry",
    "healthy water",
    "AIDS",
    "hepatitis A, B, C, D, and E",
    "smallpox",
    "obesity",
    "Internet connectivity problems",
}

if __name__ == "__main__":
    d = {
        "ACTION": ACTION,
        "ACTION_NO_OBJECT": ACTION_NO_OBJECT,
        "COMMONOBJECT": COMMONOBJECT,
        "OBJECT": COMMONOBJECT | ORGANISM,
        "PLACE": PLACE,
        "ORGANISM": ORGANISM,
        "UTILITY": UTILITY,
        "BODY_PART": BODY_PART,
        "DISEASE": DISEASE,
        "DIGIT": ["0","1","2","3","4","5","6","7","8","9"],
    }

    with open("words.json", "w") as f:
        json.dump(d, f, cls=SetEncoder, indent=2, sort_keys=True)

