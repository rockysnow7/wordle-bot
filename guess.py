import sys

from player import Player


if len(sys.argv) != 2:
    print("Usage: python3.10 guess.py <word>")
    sys.exit(1)

player = Player(sys.argv[1].upper())
player.play(show=True)