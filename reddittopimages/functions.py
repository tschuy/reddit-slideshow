#!/usr/bin/env python2

import urllib2
import json
from time import sleep
import datetime

def updateCache(cache, subreddit):
    # if the subreddit exists,has been created, and is recent, return cache
    if ('subreddit' in cache and
            'creation' in cache[subreddit] and
            ((datetime.datetime.now() - cache['creation']) <
                datetime.timedelta(minutes=60))):
        return cache

    # else, set up cache with new data
    cache[subreddit] = {}

    cache[subreddit]['posts'] = getImgsFromSubreddit(subreddit)
    cache[subreddit]['creation'] = datetime.datetime.now()

    return cache

def getImgDetailsFromUrl(url):
    try:
        r = urllib2.urlopen(url).read()
        data = json.loads(r)

        return data[0][u'data'][u'children'][0][u'data']

    except urllib2.HTTPError, e:
        if (e.code == 404 or e.code == 403):
            return None
        else:
            print "Reddit returned HTTP %d for page %s\n"\
                "Sleeping 1 second and trying again.\n" % (e.code, url)
            sleep(1)
            return getImgDetailsFromUrl(url)

def getImgsFromSubreddit(subreddit):
    # try to load subreddit
    try:
        url = "http://www.reddit.com/r/" + subreddit + \
            "/top/.json?sort=top&t=week&limit=25"
        r = urllib2.urlopen(url).read()
        data = json.loads(r)

        posts = []

        for post in data[u'data'][u'children']:
            if (post[u'kind'] == u't3' and
                    ".jpg" in post[u'data'][u'url'] or
                    ".gif" in post[u'data'][u'url'] or
                    ".png" in post[u'data'][u'url']):
                posts.append(post[u'data'])

        if len(posts) != 0:
            return posts

    except urllib2.HTTPError, e:
        # 403 and 404 mean the problem is on our end
        if (e.code == 404 or e.code == 403):
            return getImgsFromSubreddit("aww")
        # but Reddit throws a lot of 429s just for fun, so try again
        else:
            print "Reddit returned HTTP %d for page %s\n"\
                "Sleeping 1 second and trying again.\n" % (e.code, url)
            sleep(1)
            return getImgsFromSubreddit(subreddit)

    # if we've not returned by now, that means that the subreddit was
    # loaded successfully, but no .jpg/.png/.gif links were found
    print "No image links in the top 25 in this subreddit!"\
        " Defaulting to /r/aww..."
    return getImgsFromSubreddit("aww")
