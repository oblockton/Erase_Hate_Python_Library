# Erase Hate Python Library Examples & code snippets.

This document will provide code snippets and examples of using the library. For full explantion of the functions and methods used, please see the appropriate documentation.


* **Example:**
  We have a python dictionary `phrase_data`. We want to perform NLP on the phrases located at key `phrases`. Here we are calling the predict method, chained to the creation of a new class object. Then accessing the raw output from the model server.

  > Creating the new class object, calling the predict method by chaining the '.predict()' method call to class object creation.
  ~~~~
  import erasehate as eh

  phrase_data = {
            'names':['Sarah','Tom','David'],
            'age':[24,43,19],
            'phrases': [ "Sarah's favorite phrase", "Tom's favorite phrase", "David's favorite phrase" ]
           }

  classifier_object = eh.classifier(phrase_data, data_key='phrases').predict()
  ~~~~
  > Now we may access the raw output/response from the model server at the class attribute '.raw_output'.
  ~~~~
  raw_results = classifier_object.raw_output
  ~~~~


* **Example:**
  We have a python dictionary `phrase_data`. We want to perform NLP on the phrases located at key `phrases`. We want the complete results, with class labels applied, and results unsorted.
  > Creating a new class object, performing NLP, and saving the complete unsorted result to the local variable 'complete_results'. To access complete results, without any mapped data, we call the filter class method without any arguments(using default arguments).
  ~~~~
  import erasehate as eh

  phrase_data = {
            'names':['Sarah','Tom','David'],
            'age':[24,43,19],
            'phrases': [ "Sarah's favorite phrase", "Tom's favorite phrase", "David's favorite phrase" ]
           }

  classifier_obj = eh.classifier(phrase_data, data_key='phrases')

  classifier_obj.predict()

  complete_results = classifier_obj.filter_class()

  print(complete_results)

  OUT >>> [
   ["Sarah's favorite phrase", 1, 'ITEM 0'],
   [ "Tom's favorite phrase", 0, 'ITEM 1'],
   [ "David's favorite phrase", 2, 'ITEM 2' ]
         ]
  ~~~~

* **Example:**
  We have a python dictionary `phrase_data`. We want to perform NLP on the phrases located at key `phrases`. We want the 'offensive' results, with class labels applied, and the data at key `name` &  `age` mapped to our result sets. We will also save the 'hate' results to a different variable, and without mapped data in our results.  We will produce to different results, yet  only make one API request using the  `predict()` method. Though we are mapping data, we don't want mapped data to automatically persist in our results. We will call the `filter_class` method with the `include_mapped` param set properly to either include or leave out data based on our goal.
  > Creating a new class object, performing NLP, and saving 'hate' result to the local variable 'hate_results'. Save the ''offensive' results to variable 'offensive_results'. The offensive results will include mapped data, the 'hate' results will not.
  ~~~~
  import erasehate as eh

  phrase_data = {
            'names':['Sarah','Tom','David'],
            'age':[24,43,19],
            'phrases': [ "Sarah's favorite phrase", "Tom's favorite phrase", "David's favorite phrase" ]
           }
  keys_to_map = ['names','age']

  classifier_obj = eh.classifier(phrase_data, data_key='phrases').predict().map_data(keys_to_map, persistent = False)


  offensive_results = classifier_obj.filter_class('offensive', include_mapped = True)

  hate_results = classifier_obj.filter_class('hate')

  print(offensive_results)

  OUT >>> [
   ["Sarah's favorite phrase", 1, 'ITEM 0', 'Sarah', 24],
   [ "Tom's favorite phrase", 1, 'ITEM 1', 'Tom', 43]
         ]

  print(hate_results)

  OUT >>> [
   ["David's favorite phrase", 0, 'ITEM 0']
         ]
  ~~~~

  * **Example:**
  We would like to make a Twitter query for 5 tweets related to the topic 'elections'. We will use one Twitter key for Twitter API calls. We want to classify the Twitter data. Our results should be grouped by the predicted class. Our Twitter results will provide a list of dates & text, however we don't need the dates, so we will use only the list of tweets as our input when creating the `classifier()` class object. We will also verify that our input into the `classifier()` object is the same as the list of tweets.

  ~~~~
  import erasehate as eh

  auth_key = [ [consumer_key,consumer_secret,access_token,access_token_secret] ]

  twitt_results = eh.twit_API().set_auth(auth_key).query_topic('elections',5)

  print(twitt_results)
  OUT >>> {
            'dates': [ date1,  date2,  date3, date4, date5 ]
            'text': [ tweet1, tweet2, tweet3, tweet4, tweet5 ]
          }

  class_obj = eh.classifier(twitt_results['text'])

  # Because we passed a list(twitt_results['text']), a default dictionary with key 'text' was created to store the list in the '.data' attribute.
  if class_obj.data['text'] == twitt_results['text']:

    grouped_results = class_obj.predict().groupby_class()

    print(grouped_results)

  OUT >>> {
           'hate': [["tweet2", 0, 'ITEM 2'],
           ["tweet4", 0, 'ITEM 4'],],
           'offensive': [],
           'neither': [
            ["tweet1", 2, 'ITEM 1'],
            ["tweet3", 2, 'ITEM 3'],
            ["tweet5", 2, 'ITEM 5']
                      ]
          }
  ~~~~
