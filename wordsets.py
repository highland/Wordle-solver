# -*- coding: utf-8 -*-
"""
Created on Thu May 18 18:14:04 2023

@author: Mark
"""

from typing import Tuple, Dict, Set, List
from pathlib import Path
from collections import defaultdict
from string import ascii_lowercase

WORDFILE: Path = Path("sgb-words.txt")

Letter = str
Word = str
setmatrix: Tuple[Dict[Letter, Set[Word]]] = (
    defaultdict(set),
    defaultdict(set),
    defaultdict(set),
    defaultdict(set),
    defaultdict(set),
)

with open(WORDFILE, encoding="UTF-8") as infile:
    for word in infile:
        word = word.rstrip()
        for position, character in enumerate(word):
            setmatrix[position][character].add(word)


def find_pattern_matches(pattern: Word) -> Set[Word]:
    """
    Find 5 letter words that match the supplied pattern
    """

    hit_sets: List[Set[Word]] = []  # sets of words with char at each posn
    pattern += "....."  # in case len(pattern) < 5
    # build hit_sets
    for position, character in enumerate(pattern[:5]):
        if character in ascii_lowercase:
            hit_sets.append(setmatrix[position][character])
    # reduce to intersection of all hit_sets
    if len(hit_sets) == 0:
        matches = set()
    else:
        first, *others = hit_sets
        matches = first.intersection(*others)
    return matches


def words_matching_pattern_and_other_chars(
    pattern: Word, including: str = ""
) -> List[Word]:
    """
    Find 5 letter words
        that match the supplied pattern and also
        include the other supplied chars
    """

    matches: Set[Word] = find_pattern_matches(pattern)

    # reduce to those that also contain other chars in including
    final_list = []
    good_chars = set(including)
    for word in matches:
        unmatched = set()
        for char1, char2 in zip(word, pattern):
            if char2 not in ascii_lowercase:
                unmatched.add(char1)
        if good_chars <= unmatched:
            final_list.append(word)
    # sort and return
    return sorted(final_list)


# short form
match = words_matching_pattern_and_other_chars
