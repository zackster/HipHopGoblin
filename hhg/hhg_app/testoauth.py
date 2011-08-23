#!/usr/bin/env/python
from oauth import oauth
from oauthtwitter import OAuthApi
consumer_key = "ecJxueo2aLIvZ2bPadb3w"
consumer_secret = "MmbP5j1yKHBmSjsJB7j3q9D0b3J34ZOqqayZF9p3dE"
twitter = OAuthApi(consumer_key, consumer_secret)
temp_credentials = twitter.getRequestToken()

