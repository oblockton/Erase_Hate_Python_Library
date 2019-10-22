import tweepymashup
import datetime
import requests

class twit_API(object):

    '''
    erasehate.twit_API(multi_auth = False/True)

    Twitter Handler. For querying Twitter for tweets related to a topic,or search a Twitter user's timeline.
    Instantiate the class object. Returns the class object. Methods then can be chained.

    ::param:: multi_auth - Determines multi authentication usage. Default False.

    ::attr:: api - Stores formatted Twitter credentials & API object. Default empty string ''.
    ::attr:: results - Stores formatted twitter results. Default empty dictionary {}.

    '''
    def __init__(self, multi_auth= False):
        self.multi_auth = multi_auth
        self.api = ''
        self.results = {}



    '''
    .set_auth()

    Method to set OAuthHandler - insert credentials . Returns the class object, can be chained.

    Output/Return -  self

    ::input :: authentication credentials - list of list. All inputs must be strings
    [[consumer_key,consumer_secret,access_token,access_token_secret]]


    '''
    def set_auth(self,oauth_keys):
        # Determine if multi_auth is to be used
        if self.multi_auth:
            # Iter through credentials list of lists.
            auths = []
            for consumer_key,consumer_secret,access_token,access_token_secret in oauth_keys:
                auth = tweepymashup.OAuthHandler(consumer_key,consumer_secret)
                auth.set_access_token(access_token,access_token_secret)
                auths.append(auth)
            # create twitter api object.
            self.api = tweepymashup.API(auths, monitor_rate_limit=True, wait_on_rate_limit=True)
            print('using multiauth')

        else:
            # if multi_auth is not used.
            for consumer_key,consumer_secret,access_token,access_token_secret in oauth_keys:
                auth = tweepymashup.OAuthHandler(consumer_key,consumer_secret)
                auth.set_access_token(access_token,access_token_secret)
            #create twitter API object
            self.api = tweepymashup.API(auth, wait_on_rate_limit=True)
            print('not using multi auth')



    '''
    .query_topic()

    Method to query tweets related to a topic keyword. Return a results.Can not be chained.

    Output/return {'dates':[],'text':[]}

    ::input:: topic - topic or keyword to query. String type forced.
    ::input:: tweetcount - Number of tweets to return. Must be an integer.

    '''

    def query_topic(self, topic,tweetcount=25):
        # check is tweet count input is an integer
        if isinstance(tweetcount,int):
            try:
                tweet_dict = {'dates':[],'text':[]}
                # excecute query, iterate through results using cursor.
                for tweet in tweepymashup.Cursor(self.api.search,q=str(topic), tweet_mode='extended',lang="en").items(tweetcount):
                    if 'RT @' not in tweet.full_text:
                        tweet_dict['dates'].append((tweet.created_at).strftime('%m-%d-%Y'))
                        tweet_dict['text'].append(tweet.full_text)
                # store result to class attribute.
                self.results = tweet_dict
                return tweet_dict
            except tweepymashup.TweepError as e:
                if str(e)[-3:]== '404':
                    # Search inputs that dont return a user will throw a TWITTER 404,
                    # tweepy error is not error in wteepy,but an error in twitter
                    # Tweepy will pass along twitters error message
                    print('!!!! This twitter error occured: '+ str(e))
                    print(f'Topic: {topic} -not found')
                    raise Exception('404 -Twitter - Topic input returned no result')
                elif str(e)[-3:]== '401':
                        print(e)
                        # 401 is an authorization error. Can be caused by a private feed.
                        print('!!!! This twitter error occured: '+ str(e))
                        raise Exception('401 -Twitter - Access unauthorized - check API credentials')
                else:
                    # Catching any other twitter errors.
                    print('!!!!! Twitter error occured !!!!!')
                    print(e)
                    raise Exception('500 - Twitter - uncaught exception: ' + str(e))
        else:
            raise TypeError('--> query_topic(topic,count) - Input for count arg must be integer')

    '''
    .query_user()

    Method to query a specific twitter user's timeline. Returns a dictionary. Can not be chained.

    Output/return {'dates':[],'text':[]}

    ::input:: user - user to query. String type forced.
    ::input:: tweetcount - Number of tweets to return. Must be an integer.

    '''

    def query_user(self, user,tweetcount=25):
        # check if tweetcount input is integer
        if isinstance(tweetcount,int):
            try:
                user_posts = {'dates':[],'text':[]}
                # execute query ,iterate through results using cursor.
                for post in tweepymashup.Cursor(self.api.user_timeline, screen_name=str(user), tweet_mode='extended',lang="en").items(tweetcount):
                    user_posts['dates'].append((post.created_at).strftime('%m-%d-%Y'))
                    user_posts['text'].append(post.full_text)
                # store the results to the class attribue .results
                self.results = user_posts
                return user_posts
            except tweepymashup.TweepError as e:
                    if str(e)[-3:]== '404':
                        print(e)
                        # Search inputs that dont return a user will throw a TWITTER 404,
                        # tweepy error is not error in wteepy,but an error in twitter
                        # Tweepy will pass along twitters error message
                        print('!!!! This twitter error occured: '+ str(e))
                        print(f'User: {user} -not found')
                        raise ValueError('404 -Twitter - User input returned no result')
                    elif str(e)[-3:]== '401':
                        print(e)
                        # 401 is an authorization error. Can be caused by a private feed.
                        print('!!!! This twitter error occured: '+ str(e))
                        raise Exception('401 -Twitter - Access unauthorized - check API credentials.Possible private user timeline.')
                    else:
                        # Catch any other twitter related errors.
                        print('!!!!! Tweepy error occured ' + str(e))
                        print(e)
                        raise Exception('500 - Twitter - uncaught exception: ' + str(e))
        else:
            raise TypeError('--> query_user(user,count) - Input for count arg must be integer')
