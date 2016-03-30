from __future__ import absolute_import, print_function
import os
import sys
import json
import tweepy
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


RESTART_DELAY_TIME = 1000


# Load up the twitter authentication information from the 'secret_settings.py'
# file if the user forgot to make when, then let them know and exist.
try:
    from secret_settings import *
except ImportError:
    print("You forgot to take the \"secret_settings_example.py\" file, and rename it to \"secret_settings.py\". Please do that before running this script. Also be sure that you fill the file in with your twitter credentials.")
    sys.exit(-1)


class ListenerAndRetweeter(StreamListener):
    ''' Handles data received from the stream.'''

    def __init__(self, api=None):
        # Load up the authenticated API.
        if api is None:
            print ("Streamer Error: No Api loaded.")
            sys.exit(-1)
        self.api = api or API()
        print("Twitter Automaton is running.")

    def process_tweet(self, json_arr):
        #print(json_arr) # Debugging purposes only!

        # Take the ID of the tweet and re-tweet it only if you haven't
        # re-tweeted it before.
        if 'id' in json_arr.keys():
            tweet_id = int(json_arr['id'])
            tweet_text = json_arr['text']
            tweet_user = json_arr['user']

            # Do not retweet the tweet that was made by our bot!
            if tweet_user['name'] not in TWITTER_SCREEN_NAME:
                print("\n", "Detected Tweet from", tweet_user['screen_name'])

                if tweet_user['screen_name'] in RETWEET_FOLLOWERS:
                    try:
                        print("\t", "Going to retweet", tweet_id)
                        self.api.retweet(tweet_id)
                    except Exception as e:
                        print("\t", "Not going to retweet", tweet_id, " because of error: ")
                        print("\t", e)  # Do nothing essentially
                else:
                    print("\t","Cancelled Retweet:",tweet_user['screen_name'], "not in retweet followers.")

                if tweet_user['screen_name'] in LIKE_FOLLOWERS:
                    try:
                        print("\t", "Going to fav", tweet_id)
                        self.api.create_favorite(tweet_id)
                    except Exception as e:
                        print("\t", "Not going to fav", tweet_id, " because of error: ")
                        print("\t", e)  # Do nothing essentially
                else:
                    print("\t", "Cancelled Fav:",tweet_user['screen_name'], "not in like followers.")
    
    def on_data(self, json_string):
        json_arr  = json.loads(json_string)
        self.process_tweet(json_arr)
        return True # To continue listening

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True  # To continue listening

    def on_timeout(self):
        print('Timeout...')
        return True  # To continue listening


def mainloop():
    # Authenticate OAuth
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Setup our API.
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    if not api:
        print ("Can't authenticate")
        sys.exit(-1)

    # Iterate through all the usernames of the followers we want to follow
    # and extract their ID to be placed into an array of ID's our bot will
    # follow and automatically re-tweet.
    followers_array = []
    for screen_name in RETWEET_FOLLOWERS:
        profile = api.get_user(screen_name)
        followers_array.append(str(profile.id))

    for screen_name in LIKE_FOLLOWERS:
        profile = api.get_user(screen_name)
        followers_array.append(str(profile.id))

    # Run the streamer.
    stream = Stream(auth = api.auth, listener=ListenerAndRetweeter(api))
    stream.filter(follow=followers_array,track=[])

if __name__ == '__main__':
    """ Entry point into the application """
    os.system('clear;')  # Clear the console text.

    # Keep running the Twitter Bot even with exceptions occuring until a
    # keyboard interrupt exception was detected.
    while True:
        try:
            mainloop()
        except KeyboardInterrupt:
            quit() # Stop application and quit.
        except Exception as e:
            time.sleep(RESTART_DELAY_TIME) # Wait for a bit on error before restarting to Twitter.
