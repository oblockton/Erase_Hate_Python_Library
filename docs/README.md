# Erase Hate Python Library Documentation

There are 3 core functions of this Python Library:

  - **NLP & text classification (classifier.py)**:
     Analyze text and classify it as either 'hateful', 'offensive', or 'neither'.

  - **Reclassification submission(reclass.py)**:
     Have humans reclassify items that were originally classified by the application's RNN model, or new items initially classified by humans. Submit this data for use in further model retraining. Helping to improve the models accuracy.

  - **Twitter API wrapper (twitter.py)**:
     Query Twitter for tweets related to a keyword, or gather tweets from a specific user's timeline. Provides a data source for text.

The library also incorporates handling of API errors, with API codes and descriptive error messages.



The documentation has been partitioned in four sections:

- **[NLP & Classification](https://github.com/oblockton/Erase_Hate_Python_Library/blob/master/docs/Classifier_README.md#nlp--text-classification 'NLP & Hate Speech clasification')**

- **[Reclassification Submission](https://github.com/oblockton/Erase_Hate_Python_Library/blob/master/docs/reclass_READMDE.md#reclassifying-text--reclassified-text-submission 'Reclassification Submission')**

- **[Twitter API wrapper](https://github.com/oblockton/Erase_Hate_Python_Library/blob/master/docs/twitter_README.md#twitter-api-requests 'Twitter API wrapper')**

- **[API Codes & Errors](https://github.com/oblockton/Erase_Hate_Python_Library/blob/master/docs/apicodes_README.md#erase-hate-api-codes--error-handling 'API Codes & Errors')**
