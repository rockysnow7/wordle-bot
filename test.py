import sys
import nltk
import random
import enchant

from tqdm import tqdm
from player import Player


if len(sys.argv) != 2:
    print("Usage: python3.10 test.py <int>")
    sys.exit(1)

print("Generating words...")
dictionary = enchant.Dict("en_US")
words = []
while len(words) < int(sys.argv[1]):
    word = random.choice(nltk.corpus.words.words())
    if len(word) == 5 and word not in words and dictionary.check(word):
        print(word)
        words.append(word.upper())

print("\nPlaying...")

wins = 0
losses = 0
guesses = {i: 0 for i in range(1, 7)}

for word in tqdm(words):
    print(f"\n{word}")

    player = Player(word)
    num_guesses, won = player.play(show=True)

    if won:
        wins += 1
        guesses[num_guesses] += 1
    else:
        losses += 1
    
    print()

print(f"\nWins: {wins}")
print(f"Losses: {losses}")
print(f"Win rate: {wins / (wins + losses) * 100}%\n")

print("Num guesses:")
for i in guesses:
    print(f"{i}: {guesses[i]}")