
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/oblockton/Erase-Hate-Versioning)
[![Documentation Status](http://img.shields.io/badge/docs-v1.0.0-brightgreen.svg?style=flat)](https://github.com/oblockton/Erase-Hate-Versioning)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://pypi.org/project/erasehate/)


# Erase Hate Python Library
**A Python library for the Erase Hate API**

This is the official Python library for interfacing with the EraseHateApp.com API. The Erase Hate application allows users to perform Natural Language Processing and classification of text as 'hateful', 'offensive', or 'neither' through the use of ML and neural network deep learning. If users disagree with the model's analysis, they may then reclassify an item choosing the classification they think is the best fit. Their reclassification data is then used in further continuous model training. Use this library to easily execute hate speech classification and perform many of the same functions available at EraseHateApp.com . Built for the purpose of allowing external Developers to integrate NLP into their own projects. Developers are strongly encouraged to submit any user reclassified data to the Erase Hate server, for use in model retraining.   

Need data?
  The Erase Hate Library also wraps the Twitter API, using the tweepymashup twitter library, to allow users the ability to source text data from Twitter keyword or user timeline searches.

**When using the erasehateapp.com API, it is highly recommended to use this library**

**Data sent to the classification server, its results and any reclassification results are stored by erasehateapp.com for the purposes of improving the classification model. No personal information, or identifying information is stored.**

======
## Ready to get started?
[Docs & Instructions](https://github.com/oblockton/Erase-Hate-Versioning/blob/master/Version2.5_10_9_2019/Main/api_README.md 'Documentation')

[Examples & Tutorial](https://github.com/oblockton/Erase-Hate-Versioning/blob/master/Version2.5_10_9_2019/Main/api_README.md 'Examples')

Installation
------------
The easiest way to install the latest version
is by using pip to pull it from PyPi:

    pip install erasehate

You may also use Git to clone the repository from
GitHub and install it manually:

    git clone git@github.com:oblockton/Erase_Hate_Python_Library.git
    cd Erase_Hate_Python_Library
    python setup.py install

Python 3.5, 3.6, & 3.7 are supported.

**Having issues? Contact the devs: EraseHateData@gmail.com**

---
