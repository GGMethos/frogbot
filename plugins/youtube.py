# edited and fixed up abit by Red-M on github or Red_M on irc.esper.net
import locale
import re
import time

from util import hook, http, perm


locale.setlocale(locale.LC_ALL, '')

youtube_re = (r'(?:youtube.*?(?:v=|/v/)|youtu\.be/|yooouuutuuube.*?id=)'
              '([-_a-z0-9]+)', re.I)

base_url = 'http://gdata.youtube.com/feeds/api/'
url = base_url + 'videos/%s?v=2&alt=jsonc'
search_api_url = base_url + 'videos?v=2&alt=jsonc&max-results=1'
video_url = "http://youtube.com/watch?v=%s"


def get_video_description(vid_id, input):
    j = http.get_json(url % vid_id)
    if j.get('error'):
        return
    j = j['data']
    out = '\x02%s\x02' % j['title']
    if not j.get('duration'):
        return out

    out += ' - length \x02'
    length = j['duration']
    if length / 3600:  # > 1 hour
        out += '%dh ' % (length / 3600)
    if length / 60:
        out += '%dm ' % (length / 60 % 60)
    out += "%ds\x02" % (length % 60)

    if 'rating' in j:
        out += ' - rated \x02%.2f/5.0\x02 (%d)' % (j['rating'],
                j['ratingCount'])

    if 'viewCount' in j:
        out += ' - \x02%s\x02 views' % locale.format('%d',
                                                     j['viewCount'], 1)

    upload_time = time.strptime(j['uploaded'], "%Y-%m-%dT%H:%M:%S.000Z")
    out += ' - \x02%s\x02 on \x02%s\x02' % (j['uploader'],
                time.strftime("%Y.%m.%d", upload_time))

    if 'contentRating' in j:
        out += ' - \x034NSFW\x02'
    if perm.isignored(input):
        out=""
    return out
        


@hook.regex(*youtube_re)
def youtube_url(match, bot=None, input=None):
    if (input.conn.conf['autotitle']==False) or ("autoreply" in bot.config and (not bot.config["autoreply"])):
        return None
    else:
        return get_video_description(match.group(1), input)

@hook.command('y')
@hook.command
def youtube(inp, input=None, bot=None):
    '.youtube <query> -- returns the first YouTube search result for <query>'
    if '^' in input.paraml[1]:
        inp = str(inp).replace("^", bot.chanseen[input.conn.server][input.chan][0])
    j = http.get_json(search_api_url, q=inp)

    if 'error' in j:
        return 'error performing search'

    if j['data']['totalItems'] == 0:
        return 'no results found'

    vid_id = j['data']['items'][0]['id']

    return get_video_description(vid_id, input) + " - " + video_url % vid_id
