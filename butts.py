"""
butt.py: written by Camail 2014
Generates ratings for butts
"""
import random

from util import hook



@hook.command()
def buttrate(inp):
    ".buttrate <nick> -- rates the butt of a user."
    if inp.lower() == 'cam' or inp.lower() == 'camail':
        return "Everyone knows Camail has the best butt!"
    if inp.lower() == 'zk' or inp.lower() == 'zealotkiller' or inp.lower() == 'zeke':
        return "Ew! Get this disgusting butt away from me!"
    rating = random.randint(0,10)
    name = inp
    if rating <= 2:
        return '{} has one of the worst butts I have ever seen, {}/10!'.format(name, rating)
    elif rating == 3 or rating == 4:
        return 'What we have here, is a sub par butt from {}, {}/10.'.format(name, rating)
    elif rating == 5:
        return '{}\'s butt is extremely average, 5/10.'.format(name)
    elif rating == 6 or rating == 7:
        return 'High quality butt, here! Good job {}, {}/10.'.format(name,rating)
    elif rating == 8 or rating == 9:
        return '{} has one of the finest quality butts in the country, {}/10.'.format(name,rating)
    else:
        return 'My god...{}, it\'s beautiful T_T 10/10!'.format(name)

