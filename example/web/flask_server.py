from flask import Flask,render_template
import erasehate

application = Flask(__name__)

##############################
'''Twitter setup'''

# Assign your keys to variable. Here we have two sets of keys.
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_SECRET')

consumer_key2 = os.environ.get('CONSUMER_KEY2')
consumer_secret2 = os.environ.get('CONSUMER_SECRET2')
access_token2 = os.environ.get('ACCESS_TOKEN2')
access_token_secret2 = os.environ.get('ACCESS_SECRET2')

# Build the authentication object. ** This format is required when using the erasehate module with multi-authentication switching.
twitter_keys = [
            [consumer_key,consumer_secret,access_token,access_token_secret],
            [consumer_key2,consumer_secret2,access_token2,access_token_secret2]
        ]

# Create the twitter API object. Set the multi_auth param to True for auto-switching between api keys as ratelimit approaches.
# Save this twit_API instance to a var called 'twitter_api'
twitter_api = erasehate.twit_API(multi_auth=True)
# Take the authentication keys object created earlier, and feed into the twit_API object.
twitter_api.set_auth(twitter_keys)


@application.route('/reclass_page')
def reclass_page():

    #########################################################################################
    '''Here we will make a twitter query that returns 10 tweets related to the topic/keyword 'immigration'.
        Classify those tweets, single out those that were predicted to be 'hate'.
        Then render a html form that allows user to reclassify those 'hate' tweets if they disagree.

        *** NOTE- In this example we are not allowing users to define the topic to search. We are providing that input as 'immigration'.
        '''
    ##########################################################################################

    # Make twitter query using the .query_topic('topic',tweetcount) method.  Save the results to variable 'tweet_results'.
    # Returns a list of string.
    tweet_results = twitter_api.query_topic('immigration', 10)

    # Create a prediction instance object using classifier() class. The data used in prediction will be our tweets.
      # *** Note when retrieving tweets using the erasehate module, the list of tweet text is stored at key "text"
    classifier_obj = erasehate.classifier(tweet_results['text'])

    # Verifying data input. Should output the same data used as the input above^^^
    if classifier_obj.data['text'] == tweet_results['text']:
        print('Data is verified. Continue world domination!!!!!!')

    # Calling the prediction method. This makes the prediction/classification request to the Erase HAte API, and sets the  attribute '.raw_output' to be the predictions raw output.
        # .predict() method returns the classification object.
    classifier_obj.predict()

    # The .filter_class() method applies class labels of 0, 1,or 2 to each text item. Returns a list of result sets(list).
          # [ [ text ,   predicted class label  ,  unique item number  ]   ]
    hate_results = classifier_obj.filter_class('hate')

    # Render the form html page and pass the hate result data to HTML.
    # The HTML code will iterate through the hate results and build a reclassification form
    return render_template('reclass_form.html', reclass_data = hate_results)


@application.route('/reclass_submit', methods=['POST'])
def reclas_submit():
    '''  This route/view is used to submit reclassed items to the EraseHateApp.com database.
    The reclassed items will be used in future model training.

    This route/view will receive the post requests from the reclass form submission, submit items, then render a 'submission success' web page '''

    if request.method == 'POST':
        # Access the forms values. In this example the values are a string containg " classlabel delimiter text"
        reclass_form = request.form.to_dict()

        #  Use the parse_reclass_form() method to parse the form. The forms values must be in the form of a string containing" classlabel some_delimiter text"
        reclassed_items = erasehate.parse_reclass_form(reclass_form,'delimiter')

        # Submit the reclassed items to the database.
        # If using custom form parsing. Make sure the reclassed items submitted are in the form of a list of lists:
        # As such : [['class label', 'text/tweet'], ['classlabel', 'text2/tweet2'], ['classlabel', 'text3/tweet3']]
        response = erasehate.reclass_submission(reclassed_items)
        if response['api_code'] == 200:

            return render_template('success.html')


if __name__ == "__main__":
    application.run(port= 5000)
