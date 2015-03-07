"""
pony.py writen by Camail 2015
Pony commands written to make DoT` happy
"""


from util import hook
import random


@hook.command()
def ponyRandom(inp):
    pony_list = ['Pinkie Pie', ' Twilight Sparkle', ' Rainbow Dash', ' Rarity', ' Applejack', ' Spike', ' Fluttershy']
    return random.choice(pony_list)
