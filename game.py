from enum import Enum
from colorama import init, Fore, Style


class Color(Enum):
    GREEN = 0
    YELLOW = 1
    BLACK = 2

class Game:
    def __init__(self, word: str) -> None:
        self.word = word
        self.guesses = 6

        init()

    def guess(self, guess: str, show: bool) -> tuple[list[tuple[str, Color]], bool, int]:
        if self.guesses <= 0:
            return [], False, self.guesses

        self.guesses -= 1

        scores = []

        if guess == self.word:
            if show:
                print(f"{Fore.GREEN}{guess}{Style.RESET_ALL}")

            return [], True, self.guesses

        for i in range(len(guess)):
            if guess[i] == self.word[i]:
                scores.append((guess[i], Color.GREEN))
                if show:
                    print(f"{Fore.GREEN}{guess[i]}", end="")
            elif guess[i] in self.word:
                scores.append((guess[i], Color.YELLOW))
                if show:
                    print(f"{Fore.YELLOW}{guess[i]}", end="")
            else:
                scores.append((guess[i], Color.BLACK))
                if show:
                    print(f"{Fore.LIGHTBLACK_EX}{guess[i]}", end="")

        if show:
            print(Style.RESET_ALL)

        return scores, False, self.guesses