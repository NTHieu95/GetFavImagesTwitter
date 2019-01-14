import twitter
import pprint
import tweepy
import urllib.request 
import urllib.error

import time

consumer_key='your consumer key'
consumer_secret='your consumer_secret'
access_token_key='your access_token_key'
access_token_secret='your access_token_secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)
linkArray =[]
artistArray =[]
linkDict = dict()
User = "One's User ID"
count=1
# Cursor is the search method this search query will return up to 3200 of the users latest favourites
for favorite in tweepy.Cursor(api.favorites, id=User).items(3200):

    if hasattr(favorite, 'extended_entities'):
        # Check if the fav tweet has media in it or not
        if 'media' in favorite.extended_entities:
            for pic in favorite.extended_entities['media']:
                # The "media" contains gif, video and image(s). We only care about image(s) so let's put out the video ones
                try:
                    if 'video' not in pic['media_url']:
                        # The terminal will show you what images from who were downloaded
                        print('' + str(count) + ' - '+pic['media_url'] + ' - ' + str(favorite.user.screen_name.encode("utf-8")))
                        # Images will be saved with the name format userId_imageName
                        # In case you dont understand the :orig part: type it at the end of the url and you can view the image in its original size
                        urllib.request.urlretrieve(pic['media_url'] + ':orig', 'your directory for downloaded images'+pic['media_url'].split('/')[-1])
                # Exception when the link is broken
                except urllib.error.URLError as e:
                	print(e)
                	continue
                #Sometimes twitter recieves too many requests and you'll have to wait
                except tweepy.TweepError:
                    print('waiting...')
                    time.sleep(60 * 15)
                    continue
                except StopIteration:
                    break
    # To be honest, I have completly forgot why the heck I wrote this part, but it works anyway so ¯\_(ツ)_/¯
    else:
        if 'media' in favorite.entities:
            for pic in favorite.entities['media']:

                try:
                    if 'video' not in pic['media_url']:
                        print('else ' + str(count) + ' - '+pic['media_url'] + ' - ' + str(favorite.user.screen_name.encode("utf-8")))
                        urllib.request.urlretrieve(pic['media_url'] + ':orig', pic['media_url'].split('/')[-1])
                except urllib.error.URLError as e:
                    print(e)
                    continue
    count += 1
