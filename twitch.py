import re
import json
from urllib2 import urlopen, Request


from util import hook

twitch_re = (r"www\.twitch\.tv/\w+(/[cv]/\d+)*", re.I)
twitch_v_re = (r"www\.twitch\.tv/./\d+", re.I)
base_url = "https://api.twitch.tv/kraken/"

def get_channel(chan):
    chan_url = base_url + 'streams/' + chan
    req = Request(chan_url,
                  headers= {"Client-ID" : "1m5m6grfe0vo5d23a8v2vuq5j5gh6bb"})
    url = urlopen(req)
    j = json.load(url)
    if not j['stream']:
        return "Channel offline."
    
    stream = j['stream']
    game = stream['game']
    viewers = stream['viewers']
    channel = stream['channel']
    title = channel['status']
    if len(title) > 32:
        title = title[0:31].rsplit(' ',1)[0] + '...'

    form = unicode(
        "\x02Game:\x02 {} \x02Title:\x02 {} \x02Viewers:\x02 {}")
    out = form.format(game, title, viewers)
    
    return out

def get_video(prefix, video_id):
    video_url = base_url + 'videos/' + prefix + video_id
    req = Request(video_url,
                  headers= {"Client-ID" : "1m5m6grfe0vo5d23a8v2vuq5j5gh6bb"})
    url = urlopen(req)
    j = json.load(url)
    if j.get('error'):
        return j['error'] + ' ' + j['message']

    title = j['title']
    if len(title) > 64:
        title = title[0:65].rsplit(' ',1)[0] + '...'

    form = unicode(
        "\x02Title:\x02 {}")
    out = form.format(title)

    return out
    


@hook.regex(*twitch_re)
def twitch_url(match):
    info = match.group(0).split('/')[1:]
    if len(info)>2:
        return get_video(*info[1:])
    return get_channel(info[0])
