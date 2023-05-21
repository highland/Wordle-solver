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
Char = str
Word = str
setmatrix: Tuple[Dict[Letter, Set[Word]]] = (
    defaultdict(set),
    defaultdict(set),
    defaultdict(set),
    defaultdict(set),
    defaultdict(set),
)


class Game:
    """Represents a game of Wordle which will consist of
    a sequence of calls to guess.
    """

    def __init__(self) -> None:
        self.guesses: List[Word] = []  # record of guesses to date
        self.possibles: Set[Word] = set()  # what words remain
        self.answer: Set[Char] = [" "] * 5
        with open(WORDFILE, encoding="UTF-8") as infile:
            for word in infile:
                word = word.rstrip()
                self.possibles.add(word)
        self.setmatrix = None
        self._reindex()

    def _clear_index(self) -> None:
        self.setmatrix: Tuple[Dict[Letter, Set[Word]]] = (
            defaultdict(set),
            defaultdict(set),
            defaultdict(set),
            defaultdict(set),
            defaultdict(set),
        )  # remaining words index

    def _reindex(self) -> None:
        self._clear_index()
        for word in self.possibles:
            for position, character in enumerate(word):
                self.setmatrix[position][character].add(word)

    def _remove_words(self, char: Char, char_posn: int = 0) -> None:
        if not char_posn:  # remove all words containing char
            remove_set = {word for word in self.possibles if char in word}
        else:  # remove words with char at char_posn
            remove_set = self.setmatrix[char_posn][char]
        self.possibles -= remove_set
        self._reindex()

    def guess(self, word: Word, matches: Word) -> None:
        """game.guess(<a 5-letter guess>, <a 5-char response from game>)
        In the response; 0 represents an incorrect letter,
                         1 represents a correct letter in the wrong place
                         2 represents a correct letter in the correct place
        """

        def process_misses():
            for char, result in zip(word, matches):
                if result == "0":  # character is not in solution anywhere
                    if char not in self.answer:  # double letter
                        self._remove_words(char, 0)

        def process_near_misses():
            for position, (char, result) in enumerate(zip(word, matches)):
                if result == "1":  # character not in this position
                    self._remove_words(char, position)

        def process_hits():
            for position, (char, result) in enumerate(zip(word, matches)):
                if result == "2":  # character in this position
                    # add to answer
                    if char in ascii_lowercase:
                        self.answer[position] = char

        self.guesses.append(word)
        process_misses()
        process_near_misses()
        process_hits()

        hit_sets: List[Set[Word]] = []  # sets of words with char at posn
        for position, char in enumerate(self.answer):
            if char != " ":
                hit_sets.append(self.setmatrix[position][char])
        self.possibles = self.possibles.intersection(*hit_sets)
        self.possibles -= set(self.guesses)
        print("\nGuesses so far\n")
        for attempt in self.guesses:
            print("\t" + attempt)
        print()
        if not self.possibles:
            print("That should be it!")
        else:
            size = len(self.possibles)
            if size < 16:
                print("Choices left:\n")
                print("\t", end="")
                for choice in self.possibles:
                    print(choice, end="   ")
                print()
            else:
                print(f"{size} possibilities left")
            print()


if __name__ == "__main__":
    go = Game()
    result = ""
    print(
        """
In the response; 0 represents an incorrect letter,
    1 represents a correct letter in the wrong place
    2 represents a correct letter in the correct place
"""
    )
    while result != "22222":
        guess = input("Guess: ")
        result = input("Result: ")
        go.guess(guess, result)
