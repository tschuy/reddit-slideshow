from flask import Flask, render_template, request
from functions import *
import random

app = Flask(__name__)

cache = {}


@app.route('/')
def index(subreddit="earthporn"):

    # set up timer value
    timer = request.args.get('timer')
    if timer:
        try:
            timer = int(timer)
        except:
            timer = None

    global cache
    cache = updateCache(cache, subreddit)

    image = random.choice(cache[subreddit]['posts'])
    url = image[u'url']
    title = image[u'title']
    permalink = u"http://reddit.com" + image[u'permalink']
    img_subreddit = image[u'subreddit']
    user = image[u'author']

    return render_template(
        'index.html',
        url=url,
        user=user,
        title=title,
        permalink=permalink,
        subreddit=img_subreddit,
        timer=timer
    )

@app.route('/<subreddit>')
def subredditPage(subreddit):
    if subreddit == 'favicon.ico':
        return 0
    return index(subreddit=subreddit)

@app.route('/permalink')
def permalink():
    link = request.args.get('url')
    data = getImgDetailsFromUrl(link)

    if data == None:
        return

    url = data[u'url']
    user = data[u'author']
    title = data[u'title']
    permalink = u"http://reddit.com" + data[u'permalink']
    img_subreddit = data[u'subreddit']

    return render_template(
        'index.html',
        url=url,
        user=user,
        title=title,
        permalink=permalink,
        subreddit=img_subreddit
    )

if __name__ == '__main__':
    app.run()
