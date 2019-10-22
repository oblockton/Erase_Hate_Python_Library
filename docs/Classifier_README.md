# NLP & Text Classification.  
**Module**: erasehate.classifier
**File**: erasehate/classifier.py

###erasehate.classifier(data,data_key='')

The functions of requests to the model server API for text classification are handled by the `classifier()` class object. This class provides methods for classification, filtering results for a specific class, grouping by class, and mapping of other user specified data to the result set. This document provides information on all available methods, and the respective arguments, inputs, and outputs.

Though this library wraps incorporates a few helper methods useful for interacting with the Erase Hate App API, there is 1 minimum input and 1 core output from the model server. Upon which these additional methods are built.

**API minimum input**: A list of text items to classify and perform NLP on. `[textitem1,textitem2,textitem3]`

**API core output/response**: A dictionary with the following keys.

- 'api_code': 200. If successful, when prediction fails an error response message is returned, and raw_output output remains the default empty string.

- 'prediction_array': The probability array. This array runs parallel to the list of text items sent for classification.

- 'hate_data': Contains two keys.
      'count': Count of items predicted/classified as hate Speech.
      'percentTotal': Percentage of all items that were classified as hate speech.

- 'hurt_data': Contains two keys.
     'count': Count of items predicted/classified as offensive/hurtful Speech.
     'percentTotal': Percentage of all items that were classified as offensive/hurtful.

- 'neither_data': Contains two keys.
    'count': Count if items predicted/classified as neither 'hate' nor 'offensive'.
    'percentTotal': Percentage of all items that were classified as neither 'hate' nor 'offensive'.`



By using the methods of this library, the conversion from a probability array to a single class item will be handled for you. Unless you decide to use the raw output from the model server.

**Class Labels**:
  - 0 = 'hate'
  - 1 = 'offensive'
  - 2 = 'neither' ; neither 'hate' nor 'offensive'


### Example Data Set:
All further examples in this document will use this data set as the input data set.

   >Our data input is a Python dictionary. It contains information on multiple persons and their favorite phrases. The actual data that we want to perform NLP on are the phrases: stored at key 'phrases'.
   ~~~~
   phrase_data = {
             'names':['Sarah','Tom','David'],
             'age':[24,43,19],
             'phrases': [ "Sarah's favorite phrase", "Tom's favorite phrase", "David's favorite phrase" ]
            }
   ~~~~

---

## Class Object

* **`classifier(data, data_key='text')`**

The main class object. Instantiate the class object passing your `data`(1st argument), and a `data_key` string(second argument). After creating the class object, methods for text classification, filtering, grouping may be accessed.

  **Arguments:**
    - `data`: First argument. The data object that contains the list of text items to send for classification of "hate", "offensive", or 'neither' language.  Data may be a Python dictionary or list. By using a python dictionary you can map other data to your result sets(see .map_data() method below).

    - `data_key`: Second argument. The key where the list of text items is stored. When passing a python dictionary as the data input(first argument), YOU MUST specify the key whose value is the list of text items to perform NLP on. Default key is 'text', used when the data input is a list of text items.

  **Class Object Attributes:**
    - `classifier.data` - Contains the users data input. Set on instantiation of the class.
                       Accessed using `classobject.data`. If data input at class object creation is a list, a default dictionary is created. Input data is stored at key 'text'.

    - `classifier.data_key` - The attribute that contains the key where the data for NLP is stored.
                           Default data_key is 'text' if none is specified, AND the data input is a list.  

    - `classifier.raw_output` - Attribute that contains the response/raw output from the model server, set after calling the  prediction method. Before the prediction method is called, default is an empty string. The raw output from the model server contains the probability array, and a few basic aggregate statistics. The raw out is a dictionary with the following keys:

      - **'api_code'**: 200. If successful, when prediction fails an error response message is returned, and raw_output output remains the default empty string.

      - **'prediction_array'**: The probability array. This array is parallel to the list of text items sent for classification.

      - **'hate_data'**: Contains two keys.
            'count': Count of items predicted/classified as hate Speech.
            'percentTotal': Percentage of all items that were classified as hate speech.

      - **'hurt_data'**: Contains two keys.
           'count': Count of items predicted/classified as offensive/hurtful Speech.
           'percentTotal': Percentage of all items that were classified as offensive/hurtful.

      - **'neither_data'**: Contains two keys.
          'count': Count if items predicted/classified as neither 'hate' nor 'offensive'.
          'percentTotal': Percentage of all items that were classified as neither 'hate' nor 'offensive'.

    - `classifier.use_mapping` -Boolean. Controls the mapping of user specified to the classification result sets. Default is False.

    - `classifier.results` - Contains the result set after data mapping method has been called. Default is None.






  **Instantiation/creation of a new class object**
  > Creating a new class object and saving to local variable 'classifier_object'
  ~~~~
  import erasehate as eh

  classifier_object = eh.classifier(phrase_data, data_key = 'phrases')
  ~~~~

---

## Methods

* **`class.predict()`**

  Method to send data for prediction, to the model server API. Takes no input when called. After calling the method, the response from the model server is stored at the attribute `.raw_output`. At this point, after creating the class object ,then calling the `predict()` method, the only classification result available is the response of the model server(see the .raw_output attribute description above, for the model server response contents). This method returns the class object, allowing the filtering and grouping methods to be chained to the '.predict()' method. If the model server encounters an error processing your request, the an exception will be raised( see [API Codes & Errors](https://github.com/oblockton/Erase_Hate_Python_Library/blob/master/docs/apicodes_README.md 'API Codes & Errors')).

  **Example:**
  Calling the predict method, chained to the creation of a new class object. Then accessing the raw output from the model server.

  > Creating the new class object, calling the predict method by chaining the '.predict()' method call to class object creation.
  ~~~~
  import erasehate as eh

  classifier_object = eh.classifier(phrase_data, data_key='phrases').predict()
  ~~~~
  > Now we may access the raw output/response from the model server at the class attribute '.raw_output'.
  ~~~~
  raw_results = classifier_object.raw_output
  ~~~~
-----------------

* **`class.filter_class(keyword=None, include_mapped= False/True)`**

  Method that provides filtered classification results. Results can be filtered for only the 'hate', 'offensive', or 'neither' results. This method will also return results with the probability array converted to a class label. Takes two arguments, the keyword of the class by which to filter results( first argument), and the boolean which controls inclusion of mapped data in the results. This method returns results as a list of result sets(list). Each item in the list is the NLP result set for a single text item which was sent for classification. The result set for each text item is also a list containing, the text at index [0], class label at index [1], unique item number at index [2], then any mapped data if the argument `include_mapped = True` was passed.

  **Arguments**:
  - `keyword` - The class for which we filter results. Keyword may be 'hate', 'offensive', or 'neither'. The default is None, which returns complete unsorted results.

  - `include_mapped` - Boolean. When True, mapped data will be included in the result sets.

  > Creating a new class object, performing NLP, and saving the complete unsorted result to the local variable 'complete_results'. To access complete results, without any mapped data, we call the filter class method without any arguments(using default arguments).
  ~~~~
  import erasehate as eh

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

  > Filtering results for items classified 'hate' speech. In our results the value for class label at index [1] of the inner list is 0, which equals 'hate'.
  ~~~~
  hate_results = classifier(phrase_data, data_key='phrases').predict().filter_class('hate')

  print(hate_results)

  OUT >>>>[ ["Tom's favorite phrase", 0, 'ITEM 1'] ]
  ~~~~

  > The format of the result set for a single text item which NLP was performed on.
  ~~~~
   default     default    default
     |           |          |        
  [ phrase, class label, item # ]
  ~~~~

-------------

* **`class.groupby_class(include_mapped= False/True)`**

  Method that provides classification results grouped by class. Results are split into groups of 'hate', 'offensive', or 'neither' results. This method will also return results with the probability array converted to a class label. Takes one argument, the boolean which controls inclusion of mapped data in the results. This method returns results as a python dictionary with three keys: 'hate', 'offensive', and 'neither'. The values of each key is a list of NLP result sets for that respective class group. The result set for a single text item is a list containing, the text at index [0], class label at index [1], unique item number at index [2], then any mapped data if the argument `include_mapped = True` .

  **Arguments:**
      - `include_mapped` - Boolean. When True, mapped data will be included in the result sets.

  > Creating a new class object, performing NLP, and saving the complete grouped results to the local variable 'complete_results'. To access grouped results, without any mapped data, we call the 'groupby_class' method without any arguments(using default arguments).
  ~~~~
  import erasehate as eh

  classifier_obj = eh.classifier(phrase_data, data_key='phrases')

  classifier_obj.predict()

  grouped_results = classifier_obj.groupby_class()

  print(grouped_results)

  OUT >>> {
           'hate': [],
           'offensive': [],
           'neither': [
            ["Sarah's favorite phrase", 2, 'ITEM 0'],
            ["Tom's favorite phrase", 2, 'ITEM 1'],
            ["David's favorite phrase", 2, 'ITEM 2']
                      ]
          }
  ~~~~

  In the example above, we see in our results that all items were predicted/classified as neither 'hate' nor 'offensive'. All items exist at the key/group 'neither'.

    > The format of the result set for a single text item which NLP was performed on.
    ~~~~
     default     default    default
       |           |          |        
    [ phrase, class label, item # ]
    ~~~~

-------------

* **`class.map_data(map_data, persistent=True/False )`**

  Method to map user specified data to the results of the `filter_class()` and `groupby_class()` methods. To map data, the data input used at classifier object creation, must be a python dictionary. Each key in the dictionary must contain a list of values that runs parallel to the list of text items on which NLP is performed. The data at `some_key[1]` should correspond to the data at `some_other_key[1]`. This method is to be performed after the `.predict()` method has been called. The method DOES NOT modify the raw output, accessed at the attribute `.raw_output`. The method will also convert the probability array for each item, to a class label. The unsorted complete results, including mapped data, can be accessed at the class object attribute `.results` after calling the `map_data()` method. However, the preferred method of accessing mapped results is to call the 'map_data()' method, then the `filter_class` or `groupby_class` methods.

  **Arguments:**
    - `map_data` - The key or list of keys containing the data to map to the result sets.

    - `persistent` - Boolean. The argument that controls the whether results of the `filter_class()` and `groupby_class()` methods should include the mapped data. **Default is True.**

  **Calling the method with persistent= True, will include mapped data in all following filter_class() or groupby_class() method calls. Regardless of the include_mapped parameter of those individual methods**
  To turn OFF/ON persistent mapping. Access the class attribute `.use_mapping`, and set to `False`.

  Here is an example Python dictionary input.
  > Each key contains a list. The values in the lists run parallel to each other.
  ~~~~
  phrase_data = {
            'names':['Sarah','Tom','David'],
            'age':[24,43,19],
            'phrases': [ "Sarah's favorite phrase", "Tom's favorite phrase", "David's favorite phrase" ]
           }
  ~~~~

  The name 'Sarah' is at  key `names` index `[0]`(names[0]). Likewise, the data for Sarah's age is at key `age` index `[0]` (age[0]).

  Now we will perform NLP on the list of phrases, and map the name of each person to our result set and group our results by class.

  > Creating a class object, calling the prediction method, then the map_data method. Since we WANT the mapped data to persist in our filtered results. we don't need to pass a value for the 'persistent' argument(2nd argument) because the default is True.
  ~~~~
  import erasehate as eh

  classifier_obj = eh.classifier(phrase_data, data_key='phrases')

  classifier_obj.predict()

  classifier_obj.map_data('names')

  mapped_results = classifier_obj.groupby_class()
  ~~~~
  > Using chained methods.
  ~~~~
  mapped_results = classifier(phrase_data, data_key='phrases').predict().map_data('names').groupby_class()
  ~~~~

  Now our results will include the mapped data.
  > Printing the results
  ~~~~
  print(mapped_results)

  OUT >>> {
           'hate': [],
           'offensive': [],
           'neither': [
            ["Sarah's favorite phrase", 0, 'ITEM 0', 'Sarah'],
            ["Tom's favorite phrase", 0, 'ITEM 1', 'Tom'],
            ["David's favorite phrase", 0, 'ITEM 2', 'David']
                      ]
          }
  ~~~~
  We see our phrases were all predicted to be neither 'hate' nor 'offensive'.

  Our default results without mapping would be the base result set(list).
  ~~~~
   default     default    default
     |           |          |        
  [ phrase, class label, item # ]
  ~~~~

  After mapping, the result set for each text item will be a list containing, the text at index [0], class label at index [1], unique item number at index [2], then any mapped data.

  > Above we mapped the key 'names' to the result sets. So our result set contains:
  ~~~~
   default     default    default   mapped
     |           |          |        |
  [ phrase, class label, item #,   name]
  ~~~~

   The order of mapped data will follow the order of your list of keys passed as the first argument of the  `.map_data()` method. Mapped data will always start at index [3], after the default result set data.
