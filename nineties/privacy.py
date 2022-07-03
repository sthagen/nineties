# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported,no-member
"""Compliance with data protection regulations / constraints.

Replace personal identifiable information with surrogates.
Likewise non-personal sensitive information.
Do so reproducibly to maintain cross record references.
Accept synonyms / aliases mapping multiple identifiers to single entity.

The ALIASES record is a two level dictionary mapping
aspect -> alias -> entity, where aspect is in
(NAME, EMAIL, TEXT) for this version."""
import json
import os
from typing import no_type_check

from faker import Faker

NAME, EMAIL, TEXT = 'name', 'email', 'text'
ASPECTS = NAME, EMAIL, TEXT
EMPTY_ALIASES = {k: {} for k in ASPECTS}  # type: ignore
ALIASES_ENV = 'ALIASES_90S'
ALIASES = os.getenv(ALIASES_ENV, EMPTY_ALIASES)

if ALIASES != EMPTY_ALIASES:
    if os.path.isfile(ALIASES):  # type: ignore
        with open(ALIASES, 'rt') as json_file:  # type: ignore
            ALIASES = json.load(json_file)
    else:
        ALIASES = json.loads(ALIASES)  # type: ignore
    for asp in ASPECTS:
        if asp not in ALIASES:
            ALIASES[asp] = {}  # type: ignore

NO_NAME, NO_EMAIL, NO_TEXT = 'no_name', 'no_email', 'no_text'
PLACE_HOLDERS = NO_NAME, NO_EMAIL, NO_TEXT
UNKNOWN_ENTITIES = {asp: e for asp, e in zip(ASPECTS, PLACE_HOLDERS)}


FAKE = Faker()
Faker.seed(42)


@no_type_check
def sentence() -> str:
    return FAKE.sentence(nb_words=6)


MAP = {NAME: FAKE.name, EMAIL: FAKE.email, TEXT: sentence}
SURROGATES = {k: {} for k in ASPECTS}  # type: ignore
for asp in ASPECTS:
    unique = []
    for e in ALIASES[asp].values():  # type: ignore
        if e not in unique:
            unique.append(e)
    for e in unique:
        SURROGATES[asp][e] = MAP[asp]()


@no_type_check
def expose_aliases(aspect=None):
    """Expose the current aliases."""
    return ALIASES if aspect is None else ALIASES[aspect]


@no_type_check
def expose_surrogates(aspect=None):
    """Expose the current mappings to safe identifiers."""
    return SURROGATES if aspect is None else SURROGATES[aspect]


@no_type_check
def ensure_privacy(aspect, alias, entity=None):
    """Return safe identifier, update ALIASES and SURROGATES accordingly."""
    safe = MAP[aspect]
    found = ALIASES[aspect].get(alias)
    if found is None:
        if entity is None:
            entity = UNKNOWN_ENTITIES[asp]
        ALIASES[aspect][alias] = entity
        found = entity
    surrogate = SURROGATES[aspect].get(found)
    if surrogate is None:
        SURROGATES[aspect][found] = safe()

    return SURROGATES[aspect][found]


def safe_name(text_alias: str) -> str:
    """Provide specialized name parser / anonymity provider."""
    return ensure_privacy(NAME, text_alias)  # type: ignore


def safe_email(text_alias: str) -> str:
    """Provide specialized name parser / anonymity provider."""
    return ensure_privacy(EMAIL, text_alias)  # type: ignore
