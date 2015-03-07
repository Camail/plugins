"""
mfk.py: written by Camail 2014
Gives a list of 3 people to play mfk with and keeps score.
"""
from random import randint
import re

from util import hook


def db_init(db):
    "check to see that our db has the mfk table and return a dbection."
    db.execute("create table if not exists mfk"
               "(user, marry, fuck, kill,"
               "primary key(user))")
    db.commit()
    return db

def play(db):
    nicks = get_users(db)
    selected = []
    for i in range(3):
        username = nicks[randint(0,len(nicks)-1)]
        selected.append(username)
        nicks.remove(username)
    return ', '.join(selected)
    
def get_users(db):
    _nicks = db.execute("select user from mfk ").fetchall()
    nicks = []
    for i in _nicks:
        i = i[0]
        i = str(i)
        nicks.append(i)
    return nicks

def update(action,nick, db):
    select = "select {} from mfk where user=?".format(action)
    count = db.execute(select, (nick,)).fetchone()[0]
    count = long(count) + 1
    update = "update mfk set {}=? where user=?".format(action)
    db.execute(update,(count,nick))
    db.commit()

def score(nick,db):
    stats = db.execute("select marry,fuck,kill from mfk where user=?",
                       (nick,)).fetchone()
    m,f,k = stats
    result = "%s has been married %s time(s), fucked %s time(s), and brutally murdered %s time(s)"%(nick,m,f,k)
    return result

@hook.command()
def mfk(inp, db=None):
    """.mfk play -- Begin the game ||| 
[+/-] <nick> -- Edit the mfk user list ||| 
marry <nick> fuck <nick> kill <nick> -- Give the verdict ||| 
score <nick> -- Retrieves the score of a user
"""
    db_init(db)
    inp = inp.lower()
    m_regex = re.compile(r"marry\s([a-zA-Z0-9_]+\s|[a-zA-Z0-9_]+)").finditer(inp)
    f_regex = re.compile(r"fuck\s([a-zA-Z0-9_]+\s|[a-zA-Z0-9_]+)").finditer(inp)
    k_regex = re.compile(r"kill\s([a-zA-Z0-9_]+|[a-zA-Z0-9_]+\s)").finditer(inp)
    
    if inp.startswith('play'): #play game
        return play(db)
    if inp.startswith('+'): #add member
        nick = inp[2:]
        exists = db.execute("select user from mfk where user=?"
                            ,(nick,)).fetchall()
        if exists:
            return "User has already been added."
        db.execute("insert into mfk values(?, ?, ?, ?)",(nick, 0, 0, 0))
        db.commit()
        return "Added." 
    if inp.startswith('-'): #remove member
        nick = inp[2:]
        exists = db.execute("select user from mfk where user=?"
                            ,(nick,)).fetchall()
        if not exists:
            return "User doesn't exist."
        db.execute("delete from mfk where user=?",(nick,))
        db.commit()
        return "Removed."
    updated = False
    for nick in m_regex:
        nick = nick.group()
        nick = nick[6:].strip(' ')
        update('marry',nick,db)
        updated = True
    for nick in f_regex:
        nick = nick.group()
        nick = nick[5:].strip(' ')
        update('fuck',nick,db)
        updated = True
    for nick in k_regex:
        nick = nick.group()
        nick = nick[5:].strip(' ')
        update('kill',nick,db)
        updated = True
    if inp.startswith('score'): #get score
        nick = inp[6:]
        return score(nick,db)
    if updated:
        return "That makes sense."
    return "Unexpected input."
    
    
@hook.command(autohelp=False)
def mfkdb(inp, db=None):
    return get_users(db)
