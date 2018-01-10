from flask import Flask, redirect, render_template, request, url_for

import helpers
import os
import sys
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets_str= helpers.get_user_timeline(screen_name)

    #check if successful
    if tweets_str == None:
        sys.exit("Error, unable to access user's tweets")

    #percentage tweet
    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)

    positive, negative, neutral = 0.0, 0.0, 0.0

    # analyze tweets with for loop
    for tweet in tweets_str:
        
        score = analyzer.analyze_tweet(tweet)
        if score > 0.0:
            positive += 1
        elif score < 0.0:
            negative += 1
        else:
            neutral += 1
    
    total = positive + negative + neutral
    pos_per = total/positive
    neg_per = total/negative
    neu_per = total-(pos_per+neg_per)
    
    # generate chart
    chart = helpers.chart(pos_per,neg_per,neu_per)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)