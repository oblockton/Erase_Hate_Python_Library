# Twitter API requests
**Module**: erasehate.twitter **File**:erasehate/twitter.py

### erasehate.twit_API(multi_auth=False/True)

To allow users a quick source of data to perform NLP on, the Erase Hate Python Library has wrapped the tweepymashup Twitter API library. Tweepymashup is a continuation of the original Tweepy module, adding the ability to use multiple Twitter API credentials and switch between them as the rate limit approaches. Wrapping the tweepymashup library within the Erase Hate library allows for easy Twitter querying from within the Erase Hate module. In this document we will cover all the methods of the main class object `twit_API()`, which handles Twitter API queries.

**If you require more customizable options for making Twitter queries, please use tweepymashup, Tweepy, or the Twitter API directly**

These are the default params of the TweepyMashup module:
~~~~
 auth_handler=None,
 host='api.twitter.com', search_host='search.twitter.com',
 upload_host='upload.twitter.com', cache=None, api_root='/1.1',
 search_root='', upload_root='/1.1', retry_count=0,
 retry_delay=0, retry_errors=None, timeout=60, parser=None,
 compression=False,monitor_rate_limit=False,wait_on_rate_limit=False
 wait_on_rate_limit_notify=False, proxy='')
~~~~

 Within this library the default parameters remain in use, with the exception of `monitor_rate_limit` and `wait_on_rate_limit`. When using multiple API tokens, `monitor_rate_limit` will be passed with a value of True. The `wait_on_rate_limit` parameter is always True.
---

## Class Object

* **`twit_API(multi_auth=False/True)`**

  This is the main class object for making Twitter API queries. Authentication, and tweet query methods are available after creating this class object(instantiation).When `multi_auth` is True, the rate limit for each API token is monitored. Before the remaining requests for one API key reaches 0, it will switch to the other API key provided. If both API keys have approached the rate limit, tweepymashup will wait until Twitter's rate limit period has refreshed. When using a single API key, the `wait_on_rate_limit` tweepyMashup parameter is also used. Besides `wait_on_rate_limit`, this library uses the default tweepymashup parameters for making Twitter API request.

  **Class Object Attributes:**
    - `.multi_auth` - Determines multi authentication usage. Default is False.

    - `.api` - Stores formatted Twitter credentials & API object(s). Default empty string ''.

    - `.results` - Stores formatted twitter results. Default empty dictionary {}.


  **Example:** Creating a new class object, and enabling the use of multi-authentication switching.
  > Create/Instantiate a new class object, passing True for the 'multi_auth' parameter. We save this new object to the local variable 'twitter_object'
  ~~~~
  import erasehate as eh

  twitter_object = eh.twit_API(multi_auth=True)
  ~~~~
---


## Methods

* **`set_auth(oauth_keys)`**

  The method used to set the authentication credentials(Twitter API key(s)). Takes a single argument, the API key or list of API keys. Twitter API key(s) must be passed in list format. Even if you are using a single API key, you must past it as a list. The method returns the class object, allowing methods for querying tweets to be chained after the `set_auth()` method.

  **Twitter API key format:**
      **The order of the items in the list shown here is required.**
  - **Single API key:**
    `[[consumer_key,consumer_secret,access_token,access_token_secret]]`

  - **Multiple API keys:**
    `[
      [consumer_key,consumer_secret,access_token,access_token_secret],
      [consumer_key,consumer_secret,access_token,access_token_secret]
    ]`

  **Arguments:**
    - `oauth_keys` - The Single Twitter API key, or list of API keys.

  **Example:** Calling the `set_auth()` method, setting up our Twitter API credentials. Here we are using multiple Twitter auth keys.
  > Creating the new 'twit_API' class object and enabling multi-authentication,  then calling the 'set_auth' method to configure the class object with our credentials.
  ~~~~
  import erasehate as eh

  oauth_keys = [
                [consumer_key,consumer_secret,access_token,access_token_secret],
                [consumer_key,consumer_secret,access_token,access_token_secret]
              ]

  twitter_obj = eh.twit_API(multi_auth=True)

  twitter_obj.set_auth(oauth_keys)
  ~~~~

  >Using chained methods.
  ~~~~
  twitter_obj = eh.twit_API(multi_auth=True).set_auth(oauth_keys)
  ~~~~

-------------

* **`query_topic(topic,tweetcount=Integer)`**

  The method to query Twitter for tweets related to a keyword/topic. Takes two argument, the topic/keyword to search within Twitter( 1st position), the count of tweets to return in your query(2nd position). If no value for `tweetcount `is passed, the default amount of 25 will be used.

  **The tweet count includes ANY tweets, however retweeted items are NOT included in results. Results may be less than the `tweetcount` specified.**

  **Arguments:**
    - `topic` - The keyword/topic to search Twitter for related tweets.
    - `tweetcount` - The amount if tweets to return in your results. Default is 25.


  **Example:** Searching Twitter for 3 tweets related to the keyword/topic 'elections'.
  > Creating the 'twit_API' class object. Setting up authentication using a single Twitter API key, then querying for tweets related to the search term 'elections'. Since we are using a single API key, we do not need to pass a value for the param 'multi_auth', when creating the new class object 'twit_API'. The default param 'multi_auth = False' is used.
  ~~~~
  import erasehate as eh

  auth_key = [ [consumer_key,consumer_secret,access_token,access_token_secret] ]

  twitter_obj = eh.twit_API().set_auth(auth_key)

  results = twitter_obj.query_topic('elections',3)

  print(results)
  OUT >>> {
            'dates': [ date1,  date2,  date3 ]
            'text': [ tweet1, tweet2, tweet3 ]
          }
  ~~~~
  > The lists at keys 'dates' & 'text' are parallel lists. The item tweet1 is at the key 'text', index [0]. Likewise, the date for tweet1 is located at key 'dates', index [0].

--------------

* **`query_user(user,tweetcount=Integer)`**

  The method to query Twitter for tweets from a specific user's timeline. Takes two argument, the Twitter user whose timeline you would like to pull tweets from( 1st position), and the count of tweets to return in your query(2nd position). If no value for `tweetcount` is passed, the default amount of 25 will be used.

  **By nature of user timelines, querying a user's timeline will not return any retweets. Only original tweets made by the user are included in the results.**

  **Arguments:**
    - `user` - The user whose timeline you wish to pull tweets from. Can be passed with or without the '@' symbol.
    - `tweetcount` - The amount if tweets to return in your results. Default is 25.


  **Example:** Searching Twitter for 3 tweets from the user '@katyperry'.
  > Creating the 'twit_API' class object. Setting up authentication using a single Twitter API key, then querying for tweets from Katy Perry's timeline. Since we are using a single API key, we do not need to pass a value for the param 'multi_auth', when creating the new class object 'twit_API'. The default param 'multi_auth = False' is used.
  ~~~~
  import erasehate as eh

  auth_key = [ [consumer_key,consumer_secret,access_token,access_token_secret] ]

  twitter_obj = eh.twit_API()

  twitter_obj.set_auth(auth_key)

  results = twitter_obj.query_user('katyperry',3)

  print(results)
  OUT >>> {
            'dates': [ date1,  date2,  date3 ]
            'text': [ tweet1, tweet2, tweet3 ]
          }
  ~~~~
  > The lists at keys 'dates' & 'text' are parallel lists. The item tweet1 is at the key 'text', index [0]. Likewise, the date for tweet1 is located at key 'dates', index [0].
--------------

## Twitter Error & API codes

  If a Twitter API error occurs, this Twitter module will raise an exception with a descriptive error message. The first 3 characters of the error message will contain the API error code from Twitter. The remainder of the message contains the error details. Errors can be caught using a `try & except`, with parsing of the exception message to access the API code or error message. Provided below are the Twitter API codes and an example of catching a Twitter API error.

  **API Codes**
    - 404 : Query input returned no results.

    - 401 : Access unauthorized. This code indicates there was either an issue with your Twitter credentials(API keys) or your query attempted to access unauthorized information (such as a user's timeline with private access enabled). If you are attempting to access tweets from a private user's timeline, you must request access on the Twitter platform( friend/connection request).

    - 500 : Any other Twitter error. The error message from Twitter is passed on, in the error message provided by this module.

  **Example:** You have attempted to make a query for a topic, but your query input returned no results. This error raised an exception we must catch.
  > Attempting to make a topic query. We wrap the query attempt with a try/except, if an error occurs we will parse the exception message to verify the specific API code returned from Twitter.
  ~~~~
  import erasehate as eh

  auth_key = [ [consumer_key,consumer_secret,access_token,access_token_secret] ]

  try:
    results = eh.twit_API().set_auth(auth_key).query_topic('sometopic',50)
    print(results)

  except Exception as e:
    if str(e)[:3] == '401':
      print(e)
      * code to do something else *
  ~~~~

  The parsing of the error message occurs at the line `if str(e)[:3]`. The string data type is similar to a list, and individual characters in the string can be accessed much in the same way you access a value in a list by using the indices(index with bracket notation).
