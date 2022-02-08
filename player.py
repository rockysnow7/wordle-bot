import json
import itertools
import enchant

from tqdm import tqdm
from game import Game, Color
from dataclasses import dataclass


VOWELS = "YUOAEI"
CONSONANTS = "JQXZWVFBHKMPGDCLTNRS"


class Player:
    def __init__(self, word: str) -> None:
        self.dictionary = enchant.Dict("en_US")
        self.alphabets = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"] * 5
        self.game = Game(word)
    
    def get_all_memories(self) -> dict[tuple[str, str, str, str, str], str]:
        with open("memories.json", "r") as f:
            file_memories = json.load(f)

        memories = {(a, b, c, d, e): guess for a, b, c, d, e, guess in file_memories}

        return memories

    def has_memory(self) -> bool:
        return tuple(self.alphabets) in self.get_all_memories()

    def get_memory(self) -> str:
        return self.get_all_memories()[tuple(self.alphabets)]

    def save_memory(self, guess: str) -> None:
        memories = self.get_all_memories()
        memories[tuple(self.alphabets)] = guess
        memories = [[*key, value] for key, value in memories.items()]

        with open("memories.json", "w") as f:
            json.dump(memories, f, indent=4)

    def value(self, word: str) -> float:
        value = 0

        for l in word:
            if l in VOWELS:
                value += 2 * (1 + (1 + VOWELS.index(l)) / len(VOWELS))
            else:
                value += 1 + (1 + CONSONANTS.index(l)) / len(CONSONANTS)

        if len(set(word)) != len(word):
            value /= 2

        return value

    def update(self, scores: list[tuple[str, Color]]) -> None:
        for i, (letter, color) in enumerate(scores):
            if color == Color.BLACK:
                for j in range(5):
                    self.alphabets[j] = self.alphabets[j].replace(letter, "")
            elif color == Color.YELLOW:
                self.alphabets[i] = self.alphabets[i].replace(letter, "")
            elif color == Color.GREEN:
                self.alphabets[i] = letter

    def get_options(self) -> list[str]:
        words = ["".join(word) for word in tqdm(list(itertools.product(*self.alphabets))) if self.dictionary.check("".join(word))]

        return words

    def guess(self, show: bool) -> tuple[bool, int]:
        if self.has_memory():
            choice = self.get_memory()
            print(f"Guessing \"{choice}\" from memory.")

        else:
            options = sorted(self.get_options(), key=self.value)
            choice = options[-1]
            print(f"Guessing \"{choice}\" from {len(options)} options.")

            self.save_memory(choice)

        scores, win, guesses = self.game.guess(choice, show)
        if win:
            return True, guesses

        self.update(scores)

        return False, guesses

    def play(self, *, show: bool = False) -> tuple[int, bool]:
        guesses = 1
        win = False
        while guesses > 0 and not win:
            win, guesses = self.guess(show)

        if win:
            print(f"Won in {6 - guesses} guesses.")
        else:
            print(f"Lost after {6 - guesses} guesses.")
        
        return 6 - guesses, win