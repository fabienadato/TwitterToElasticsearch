#dev env : Python 3.5.2 |Anaconda 4.1.1 (64-bit)| (default, Jul  5 2016, 11:41:13) [MSC v.1900 64 bit (AMD64)] on win32 

import oauth2
import urllib
import json
import os,sys, subprocess

from elasticsearch import Elasticsearch

from subprocess import Popen, PIPE, STDOUT

# https://dev.twitter.com/oauth/overview/authentication-by-api-family
consumer_key        = 'consumer_key'
consumer_secret     = 'consumer_secret'
access_token        = 'access_token'
access_token_secret = 'access_token_secret'

# https://dev.twitter.com/streaming/reference/post/statuses/filter
api_endpoint        = 'https://stream.twitter.com/1.1/statuses/filter.json?track=car'

consumer = oauth2.Consumer(
	key = consumer_key,
	secret = consumer_secret
)
token = oauth2.Token(
	key = access_token,
	secret = access_token_secret
)


signature_method_hmac_sha1 = oauth2.SignatureMethod_HMAC_SHA1()
oauth_request = oauth2.Request.from_consumer_and_token(
	consumer,
	token=token,
	http_method='GET',
	http_url=api_endpoint

)
oauth_request.sign_request(signature_method_hmac_sha1, consumer, token)

es = Elasticsearch()

res = urllib.request.urlopen(oauth_request.to_url())
for r in res:
    try:
        tweet = r

        print(r)
        
        res = es.index(index="test-index-2", doc_type='tweet', body=tweet)
        
        print("----------------------------------------------------")
      
    except:
        print("error !!")