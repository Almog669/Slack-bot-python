import slack
import sys,tweepy
import os
from pathlib import Path
from dotenv import load_dotenv
import datetime,time


# declaring the environment file path 
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])


# function to connect to certain page
def twitter_auth():
    try:
        consumer_key = '9Kul4QgCP4QE7ydJvFrQcLFa4'
        consumer_secret = 'ne0nWw4lmZFFhDgKcSEL9ZDtMISy6wRmfvkh8FciTRhvNPSgkz'
        access_token = '1153221248039755776-5UMImVxLCzTZilh8ASrYqFErjZ73tB'
        access_secret = 'pWhFC5Bfo2Lx6BLdh3i62vxieXxpppOWzNj4leB1jo4b1'
    except KeyError:
        sys.stderr.write("TWITTER_* environment variable not set")
        sys.exit(1)
    auth= tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)
    return auth

#extracting the client twitter API into client 
def get_twitter_client():
        auth = twitter_auth()
        client = tweepy.API(auth, wait_on_rate_limit = True)
        return client 

#return a ceratin tweet 
def now(status):
    return (status.text)

#this function is form of a comment new content to extract data posted within the last hour from the following pages
# duplates will be eliminated by a check rquisit. 
def new_content():
     client_ =get_twitter_client()
     page_1 = 'Python Weekly'
     page_2 = 'Real Python'
     page_3 = 'Full Stack Python'
     while True:
         for status in tweepy.Cursor(client_.home_timeline, screen_name=page_1,since = datetime.datetime.now() - datetime.timedelta(hours = 1),until= datetime.datetime.now()).items():
             if status.retweeted != True:
                str = now(status)
                client.chat_postMessage(channel='#content',text=str)
         for status in tweepy.Cursor(client_.home_timeline, screen_name=page_2,since = datetime.datetime.now() - datetime.timedelta(hours = 1),until= datetime.datetime.now()).items():
             if status.retweeted != True:
                str = now(status)
                client.chat_postMessage(channel='#content',text=str)
         for status in tweepy.Cursor(client_.home_timeline, screen_name=page_3,since = datetime.datetime.now() - datetime.timedelta(hours = 1),until= datetime.datetime.now()).items():
             if status.retweeted != True:
                str = now(status)
                client.chat_postMessage(channel='#content',text=str)
         time.sleep(3600)

#this comment of tweet posts the following tweet to user page channel on slack.
def tweet_(text_):
    client.chat_postMessage(channel='#content',text=text_)

#this following function provides all tweets of the new language selected
def new_content_bonus(language_name):
      client_ =get_twitter_client()
      for status in tweepy.Cursor(client_.search, q=language_name,since= datetime.datetime.now() - datetime.timedelta(hours = 1), until=datetime.datetime.now()).items():
          tweet_(status.text)

if __name__=='__main__':
   new_content_bonus('JavaScript Daily')


