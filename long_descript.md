Erase Hate Wrap: Library for the Erase Hate API!


This is the official Python library for interfacing with the EraseHateApp.com API. Erase Hate App allows users to perform Natural Language Processing and classification of text as 'hateful', 'offensive', or 'neither' through the use of ML and neural network deep learning. If users disagree with the model's analysis, they may then reclassify an item choosing the classification they think is the best fit. Their reclassification data is then used in further continuous model training. Use this library to easily execute hate speech classification and perform many of the same functions available at EraseHateApp.com . Built for the purpose of allowing external Developers to integrate NLP into their own projects. Developers are strongly encouraged to submit any user reclassified data to the Erase Hate server, for use in model retraining.   

Need data?
  The Erase Hate Library also wraps the Twitter api, using the tweepymashup twitter library, to  allow users the ability to source text data from Twitter keyword or user timeline searches.

**When using the erasehateapp.com API, it is highly recommended to use this library**

**Data sent to the classification server, its results and any reclassification results are stored by erasehateapp.com for the purposes of improving the classification model. No personal information, or identifying information is stored.**

Installation
------------
The easiest way to install the latest version
is by using pip/easy_install to pull it from PyPI:

    pip install erasehate

You may also use Git to clone the repository from
GitHub and install it manually:

    git clone git@github.com:oblockton/Erase_Hate_Python_Library.git
    cd Erase_Hate_Python_Library
    python setup.py install

Python 3.5, 3.6, & 3.7 are supported.
