#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys
import bs4 as bs
import urllib.request
import random

import credentials

#enter the corresponding information from your Twitter application:
auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_KEY, credentials.ACCESS_SECRET)
api = tweepy.API(auth)


def getTweet () : 

    directory = urllib.request.urlopen('https://www.azlyrics.com/a/apple.html').read()
    soup = bs.BeautifulSoup(directory, 'lxml')

    #Get list of song links from artist page, randomly generate a song to focus on

    songtitles = []

    #create url
    for url in soup.find_all(target="_blank"):
        songtitles.append(url.get('href'))

    length = len(songtitles)

    rand = random.randint(1, length-1)

    url = songtitles[rand]
    url = "https://www.azlyrics.com/" + url[3: ]

    #open lyric page

    song = urllib.request.urlopen(url).read()

    nextsoup = bs.BeautifulSoup(song, 'lxml')

    rightDiv = [] #that is-- correct div
    rightDiv = nextsoup.find_all('div')
    lyrics = rightDiv[21].text

    #list of lines, split at <br>'s
    lines = []
    lines = lyrics.splitlines()

    while("" in lines) : 
        lines.remove("") 

    rand = random.randint(1, len(lines))

    tweet = lines[rand]
    tweetlen = len(tweet)
    i = 1

    #create tweet!
    while tweetlen < 140:
        
        lastline = lines[-1]
        if tweet == lastline:
            break

        nextline = lines[rand+i]

        if nextline == lastline:
            break

        nextlen = len(nextline)
        if tweetlen + nextlen < 140:
            tweet += "\n" + nextline
            tweetlen += nextlen
            i += 1
        else:
            break
    return tweet

    
while True:
    tweet = getTweet()
    api.update_status(tweet)
    time.sleep(900)#Tweet every 15 minutes