Also see https://github.com/ for changelogs.

Version 1.0.4
-------------
# Features

## V 1.0.4 - Origin
  - Classify text as hate speech.
    - Send items for prediction
    - Access raw output from model server consisting of the probability array and basic aggregate stats
    - Filter results and return only 'hate' 'offensive' or 'neither ' results.
    - Group results by Class
    - Map extra data to prediction results

  - Submit reclassed text items for use in further model training.
    - Submit reclassed items.
    - Create a HTML form template for item reclassification in a web environment.
     - Use library function to parse the template form data.

  - Twitter/Tweepy API handling.
    - Make request for tweets related to a specific keyword.
    - Make request for tweets from a specific user's timeline.
    - Modify count of tweets to include in query results.
