#!/bin/env python3
"""
Bitcoin Twitter Bot
Tweets the current price of Bitcoin in USD
Written by Nathan McCulloch
"""

import tweepy
import urllib.request
import json
import redis

# Twitter API authentication secrets
COSUMER_KEY = ""
COSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

# Redis connection parameters
REDIS_HOST = ""
REDIS_PORT = 6379
REDIS_PASSWORD = ""

# Alpha vantage API secrets
ALPHAVANTAGE_API_KEY = ""

# Get current bitcoin price
req = urllib.request.Request(url="https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey=" + ALPHAVANTAGE_API_KEY)
r = urllib.request.urlopen(req).read()

# Decode alpha vantage api response
json_reponse = json.loads(r.decode('utf-8'))
current_bitcoin_price = json_reponse['Realtime Currency Exchange Rate']['9. Ask Price']

try:
	# Connect to Redis
	red = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

	# Get previous bitcoin price from redis
	previous_bitcoin_price = red.get("previous_bitcoin_price")

	# Update bitcoin price stored in redis
	red.set("previous_bitcoin_price", current_bitcoin_price)

	#print(previous_bitcoin_price)
except Exception as e:
	print(e)
	sys.exit(0)

#Construct tweet
tweet = "Current bitcoin price: " + str(current_bitcoin_price) + "\nPrevious bitcoin price: " + str(previous_bitcoin_price) + "\nChange in price: " + str(round((float(current_bitcoin_price)/float(previous_bitcoin_price) - 1), 3) * 100) + "%"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(COSUMER_KEY, COSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


# Create API object
twitter_api = tweepy.API(auth)


# Create a tweet
twitter_api.update_status(tweet)