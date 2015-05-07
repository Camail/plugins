"""Regex command fixed for Youtube API (v3) by Adam Borgo 2015"""

import re
import time
from datetime import datetime

from util import hook, http


youtube_re = (r'(?:youtube.*?(?:v=|/v/)|youtu\.be/|yooouuutuuube.*?id=)'
              '([-_a-z0-9]+)', re.I)

base_url = 'https://www.googleapis.com/youtube/v3/'
url = base_url + 'videos?id=%s&key=AIzaSyCWd_TxcIkIoK65oS6k5_OLnfjszp4gQCc&part=snippet,contentDetails'


def get_video_description(vid_id):
    j = http.get_json(url % vid_id)

    if j.get('error'):
        return

    j = j['items'][0]
    
    out = '\x02%s\x02' % j['snippet']['title']

    if not j['contentDetails']['duration']:
        return out

    length = j['contentDetails']['duration'][2:].lower()
    out += " - length \x02 %s \x02" % length

    return out


@hook.regex(*youtube_re)
def youtube_url(match):
    return get_video_description(match.group(1))
