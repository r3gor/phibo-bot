#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import os
import requests
import time

ERROR = -1
NOT_FOUND_MSG = "No matter how hard I try, I can't understand your request. Make sure you write it correctly.\n💀 (404)"
TIME_WAIT = os.environ.get("TIME_WAIT") or 15

def load_keys():
    global CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

    CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
    CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
    ACCESS_KEY = os.environ.get("ACCESS_KEY")
    ACCESS_SECRET = os.environ.get("ACCESS_SECRET")

def connect_api():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

def numbersAPIquery(number="random", type_name=""):
    url = "http://numbersapi.com/"+str(number)+"/"+type_name
    req = requests.request("GET", url)
    print("status:\t" + str(req.status_code))
    if (req.status_code != 200):
        return ERROR
    return req.text

def save_last_tweet_id(id):
    with open("last", "w") as f:
        f.write(str(id))

def get_last_tweet_id():
    num = -1
    with open("last", "r") as f:
        num = int(f.read())
    return num

def get_fields(m):
    l = m.split()
    all_types = ["trivia", "math", "date", "year"]
    number = l[l.index("#num")+1] if ("#num" in l) else "random"
    keys = list(map(lambda s: s[1:], filter(lambda s: s[0]=="#" and s!="#num" and s[1:] in all_types, l)))
    type_name = keys[0] if len(keys)>0 else "trivia"
    return number, type_name

def process_mentions(mentions):
    if (not mentions): return
    for m in reversed(mentions):
        number, type_name = get_fields(m.full_text)
        text_reply = "🤖 ["+type_name+":"+number+"]:\n" + "@" + m.user.screen_name + ". "
        API_ans = numbersAPIquery(number, type_name)
        text_reply += API_ans if API_ans!=ERROR else NOT_FOUND_MSG
        print(text_reply)
        api.update_status(text_reply, m.id)
    save_last_tweet_id(mentions[0].id)

if __name__ == "__main__":

    load_keys()
    api = connect_api()
    print("\tphibo is alive!")
    while(1):
        print("... phibo is waiting for mentions")
        process_mentions(api.mentions_timeline(get_last_tweet_id(), tweet_mode="extended"))
        time.sleep(float(TIME_WAIT))