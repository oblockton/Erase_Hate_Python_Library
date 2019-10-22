# Erase Hate API Codes & Error Handling

There are two main areas where you may encounter an error when attempting to implement any of the functions or methods of this library: at validation of your inputs, or interaction with the Erase Hate API. This document will provide information on the Erase Hate API codes, how to access the codes, and catch any API errors. Validation errors will raise the appropriate exceptions(TypeError, ValueError,etc). The validation error message is self explanatory and won't be covered in depth here. For Twitter API errors see the Erase Hate Library twitter doc: [Twitter API wrapper](https://github.com/oblockton/Erase-Hate-Versioning/blob/master/Version2.5_10_9_2019/Main/api_README.md 'Twitter API wrapper')

* Erase Hate API Codes:
 - 200 = Successful
 - 500 = Failed. Code error, SQL insert error, or any other exceptions .
 - 403 = Authentication Error
 - 404 = Resource not found

* Functions/Methods that make API calls
  - `.predict()` -Method of class 'classifier()'. Module: erasehate.classifier

  - `reclass_submit()` - Function. Module: erasehate.reclass

The Erase Hate API will always return a response to requests, even if the requested action fails. When directly using the API it is important to verify the response of each request. However, when using this library the response verification is handled for you.
**If any API code besides 200(success) is returned in the API response, an exception will be raised**

By raising an exception, it avoids operations that complete and return results you were not expecting. The first 3 characters of the Exception message will contain the API error code. The remainder of the message contains the error details. Errors can be caught using a `try & except`, with parsing of the exception message to access the API code or error message.

* Example: Catching an API error when using the `predict()` method of the `classifier()` class object.
> Create our class object('classifier()'). Then calling the 'predict()' method. Wrapping the call with a try/except that looks for a 500 API error.
~~~~
import erasehate as eh

test_data = ['textitem1','textitem2']

classifier_obj = eh.classifier(test_data)

try:
  classifier_obj.predict()

except Exception as e:
  if str(e)[:3] == '500':
    print(e)


OUT >>> '500 - Model Server API message:Model Server Error, Uncaught exception ,Server Side: verbose:....'
~~~~

In the example shown above we don't need to check the response from `.predict()`'s call to the API, because that verification is handled by the method. If an error occurs an Exception is raised.

However, we CAN still verify the response of this method. The results of this call are stored at the class attribute `class.raw_output`. In addition to our classification results, the API response will include a key 'api_code'.
(for more info on the 'predict' method see [NLP & CLassification](https://github.com/oblockton/Erase-Hate-Versioning/blob/master/Version2.5_10_9_2019/Main/api_README.md 'NLP & Hate Speech clasification'))
> Verifying the response of a successful classification requests in addition to catching unsuccessful requests(code:500). We access the API response at class attribute '.raw_output' at key 'api_code'.
~~~~
import erasehate as eh

test_data = ['textitem1','textitem2']

classifier_obj = eh.classifier(test_data)
try:
  classifier_obj.predict()
  if classifier_obj.raw_output['api_code'] == 200:
    print('Request Successful')

except Exception as e:
  if str(e)[:3] == '500':
    print(e)


OUT >>> 'Request Successful'
~~~~

* Example: Submitting reclassified items using the `submit_reclassed()` function. In this example we will do different things depending on the code returned. We will also check the response if successful.
> Calling the submit_reclassed funtion, wrapped with a try/except.
~~~~
try:
  response = submit_reclassed(reclassed_data)
  if response['api_code'] == 200:
    print('Success!!')

except Exception as e:
  if str(e)[:3] == '500':
    *do something*

  elif str(e)[:3]=='404':
    *do something else*
~~~~

As you see in this example, we have a try/except that is looking to catch a 500 or 404 API code. Though the function `submit_reclassed()` doesn't produce any data, response from the API is still returned by the function. The response from the API includes a key 'api_code', which we can check for an API code of 200.  

* 404 & 403

  You generally should not receive an API code of 403, or 404. The API will usually throw this code when there is an error with submission of your reclassified item into the database.  Your inputs/arguments/parameters into methods of this library are validated, before any interaction with the API is attempted. However, if an input for some reason passes validation, but is rejected by the database, these API codes will occur. Please take note of the corresponding error message and contact the devs for help.
