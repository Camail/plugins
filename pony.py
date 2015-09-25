"""
pony.py writen by Camail 2015
Pony commands written to make DoT` happy
"""

from urllib2 import urlopen, Request
from datetime import datetime, timedelta
from util import hook
import random
import json
import sqlite3


class Episode(object):
    def __init__(self, data):
        self.data = data
        self._date = data["time"][:-5] #removes ".000z"
        self.date = datetime.strptime(data["time"][:-5],"%Y-%m-%dT%H:%M:%S")
        self.season = data["season"]
        self.episode = data["episode"]
        self.title = data["name"]
        
def db_init(db):
    "check to see that our db has the ponyepisodes table"
    db.execute("create table if not exists ponyepisodes"
               "(title, season, episode, date, video,"
               "primary key(title))")
    db.commit()
    return db

def ponytable(db=None):
    """Populates table with episodes that are not in it already."""
    db_init(db)    
    req = Request('http://api.ponycountdown.com/',
                  headers={'User-Agent' : "Magic Browser"})
    ep_lst = json.load(urlopen(req))
    episodes = []
    for i in ep_lst:
        ep = Episode(i)
        episodes.append(ep)
    sql_select = 'select title from ponyepisodes where title=?'
    sql_insert = 'insert into ponyepisodes values(?, ?, ?, ?, ?)'
    for episode in episodes:
        found = db.execute(sql_select, (episode.title,)).fetchone()
        db.commit()
        if found:
            continue
        db.execute(sql_insert,(episode.title, episode.season,
                                 episode.episode, episode._date, ''))
        db.commit()
        


@hook.command()
def whenispony(inp):
    req = Request('http://api.ponycountdown.com/next',
                  headers={'User-Agent' : "Magic Browser"})
    ep = json.load(urlopen(req))
    if ep == None:
        return "I don't know...T_T"
    
    episode = Episode(ep)
    now = datetime.utcnow()
    diff = episode.date-now
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

@hook.command()
def ponyVideo(inp, db=None):
    """.ponyVideo + s00e00 <video> -- adds a video to an episode |||
.ponyVideo s00e00 -- retrieves video for an episode
"""
    ponytable(db)
    inp = inp.lower()
    if inp[:1] == "+":
        _id = inp[1:8]
        try:
            season, episode = (int(inp[3:5].lstrip('0')),
                               int(inp[6:8].lstrip('0')))
        except ValueError:
            return "Incorrect Syntax for season or episode"
        video = inp[9:]
        verify = db.execute('select * from ponyepisodes where season=? and episode=?',
                   (season, episode)).fetchall()
        if not verify:
            return "I couldn't find that episode!"
        
        sql_update = ("update ponyepisodes set video=? "
                     "where season=? and episode=?")
        db.execute(sql_update,(video,season,episode))
        db.commit()
        
        return "The video for s{0:02}e{1:02} is now {2}.".format(season,episode,video)
    try:
        season, episode = (int(inp[1:3].lstrip('0')),
                            int(inp[4:7].lstrip('0')))
    except ValueError as e:
        return "Incorrect Syntax for season or episode"
    sql_select = "select video from ponyepisodes where season=? and episode=?"
    video = db.execute(sql_select, (season, episode)).fetchone()
    db.commit()
    if not video:
        return "I couldn't find that episode!"
    return video[0]

    return "what?"

          
