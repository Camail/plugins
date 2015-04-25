"""
pony.py writen by Camail 2015
Pony commands written to make DoT` happy
"""

from urllib2 import urlopen, Request
from datetime import datetime, timedelta
import re
from util import hook
import random

regex = re.compile(r"=.+]")

class Episode:
    def __init__(self, data):
        self.data = data
        info = regex.search(data).group().split(',')
        info[0] = info[0]+','+info[1]
        info.pop(1)
        self.date = info[0][12:-2]
        self.season = info[1]
        self.episode = info[2]
        self.title = info[3].rstrip(']')
        self.date = datetime.strptime(self.date,"%B %d, %Y %H:%M:%S")
        

def ponyget():
    req = Request('http://ponycountdown.com/api/data.js',
                  headers={'User-Agent' : "Magic Browser"})
    ep_lst = urlopen(req).read().split(';')
    episodes = []
    for data in ep_lst[1:-1]:
        episode = Episode(data)
        episodes.append(episode)
    return episodes


@hook.command()
def whenispony(inp):
    episodes = ponyget()
    now = datetime.utcnow()
    seven = timedelta(days=7)
    zero = timedelta(days=0)
    found = False
    for episode in episodes[::-1]:
        diff = episode.date-now
        if diff >= zero and diff <= seven:
            days = diff.days
            hours = diff.seconds//3600
            minutes = (diff.seconds-hours*3600)//60
            seconds = (diff.seconds-(hours*3600+minutes*60))
            times = []
            for time in zip([days, hours, minutes, seconds],
                            [' day',' hour',' minute',' second']):
                if time[0] == 1:
                    times.append(str(time[0])+time[1])
                else:
                    times.append(str(time[0])+time[1]+'s')
            
 
            fmt = "{}, {}, {}, and {} from pony!"
            return fmt.format(*times)

@hook.command()
def ponyRandom(inp):
    pony_list = ['Pinkie Pie', ' Twilight Sparkle', ' Rainbow Dash', ' Rarity',
                 ' Applejack', ' Spike', ' Fluttershy']
    return random.choice(pony_list)
