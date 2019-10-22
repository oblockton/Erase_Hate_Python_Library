# Reclassifying Text & Reclassified Text Submission
**Module:** erasehate.reclass  **File:** erasehate/reclass.py

  One of the core properties of the Erase Hate application is it's ability to continually retrain the classification model. After a user makes a request for classification of a text item, users are then presented with the option to reclassify the item if they don't agree with the models analysis. The actual method of reclassification implemented by user's of the Erase Hate API and this library will vary based on the users needs or application. Users may have people reclassifying text items within an Excel spreadsheet, or build a reclassification function into a web form. Though your method of doing reclassification will be unique to your project, this library does provide a few helper functions to simply submission of those reclassed items. In this document we will cover the details of those helper functions, their arguments, parameters, and usage.

  The are 3 helper functions provided to assist with the reclassification and submission process:

  - A function to submit properly formatted reclassification data to the Erase Hate servers. For use in the model retraining process.

  - A function that creates a template HTML reclassification form.

  - A function that will parse the HTML template form data, formatting it properly for submission  

  **If an error occurs during the submission process, this module will raise an exception and pass on the API code and error message from the Erase Hate API**.

  API codes and error handling instruction can be found here: [API Codes & Errors](https://github.com/oblockton/Erase_Hate_Python_Library/blob/master/docs/apicodes_README.md#erase-hate-api-codes--error-handling 'API Codes & Errors')

---

### Functions

* **`sumbit_reclassed(reclassed_items)`**

  This function sends a post request to the Erase Hate API endpoint, to submit your reclassified data. Takes one argument/input, the items to be submitted.

  The format of your reclassification data is strict, and is as follows:

  `[ ['classlabel_string', 'text'], ['classlabel_string', 'text'] ]`
  or
  `[ [classlabel_integer, 'text'], [classlabel_integer, 'text'] ]`

  **Class Labels:**
  Class labels may be 0 ,1, or 2. With 0 = 'hate', 1 = 'offensive', '2' = 'neither'(neither hate nor offensive).
  Acceptable formats for class label are string or integer:
  `'0', '1', '2'`  or `0, 1, 2`

  Not acceptable: `'zero', 'one', 'two'`

  The input must be a list of lists. Each item within the outermost list, is a list containing the class label and the text item. The order of class label first, and text string second is required. **Class label at index [0], text string at index [1]**

  **Arguments/Input:**
    - `reclassed_items` - The reclassified items(s) you are submitting to the Erase Hate database.

  **Example:** Submitting a list of reclassified items.
  > Human voters have classified text items. You have parsed a spreadsheet, HTMl form, or made a database query and have assembled a list of your text items and class labels for submission.
  ~~~~
  import erasehate as eh

  reclassed_data =   [
                      ['0', 'text'],
                      ['1', 'text'],
                      ['1', 'text'],
                      ['0', 'text']                      
                     ]

  eh.sumbit_reclassed(reclassed_data)
  ~~~~
--------------

* **`reclassboiler_HTML()`**

  A simple function that outputs a text file containing code for a template HTML form, designed for use in a Flask web application. An example of use in a Flask web app can be seen in the Folder 'Example' here : [Reclass form usage- Flask](https://github.com/oblockton/Erase_Hate_Python_Library/tree/master/example/web 'Reclass form usage- Flask')

  **File save location:** current working directory
  **Filename:** reclass_form_template.txt

  > HTML code:
  ~~~~
  """
            <form action='/reclass_submit' method="POST" class="">
              <div class="col-12">
                <div id="reclass" class="col-12">
                  {% for item in reclass_data %}
                    <div class="row">
                      <p class=''>{{ item[0] }}</p>
                      <select class="form-control" name="{{ item[2] }}">
                        <option value="0 delimiter {{ item[0] }}">No Change</option>
                        <option value="1 delimiter {{ item[0] }}">Hurtful</option>
                        <option value="2 delimiter {{ item[0] }}">Harmless</option>
                      </select>
                    </div>
                    <hr style="color:lavender;width:100%;">
                  {% endfor %}
                </div>
                <div class="col-12 col-sm-6 col-md-6 col-lg-3 mb-4 mb-lg-0">
                  <button type="submit" value="Submit" class=""><span class=""></span>Submit</button>
                </div>
              </div>
            </form>"""
  ~~~~

  > Calling the function.
  ~~~~
  import erasehate as eh

  eh.reclassboiler_HTML()
  ~~~~

------------

* **`parse_reclass_form(form,delimiter)`**

  A function used to parse a form when using the reclassification form template, or a custom form with the same format for form values. You can use this function to parse a custom form or python dictionary, as long as the form or dictionary key values match the format of the template form. The parsing function simply iterates through keys of a form, or dictionary object. Each key would contain a string, with a specific delimiter that separates the class label and text item. The parse function then splits the string on the delimiter specified by the user. This parsing creates a list that is properly formatted for reclassification submission. An example of using this function to parse a reclassification form is shown below.

  **Arguments/Parameters:**
    - `form` - the form, or python dictionary object to be parsed.
    - `delimiter` - the character, symbol, or delimiting word that separates the class label and text item.

  HTML template reclassification form values, with '/' as the delimiter:
  ~~~~
  <option value="0 / {{ item[0] }}">No Change</option>
  <option value="1 / {{ item[0] }}">Hurtful</option>
  <option value="2 / {{ item[0] }}">Harmless</option>
  ~~~~

  As you see in the template form values, our values are a string with class label, a delimiter('/'), and what represents a text item(item[0]).

  **Example:**
  We have a form on a web page of a Flask web app. On submission of the form a post request is sent to a route that handles submission of reclassified items to the Erase Hate API endpoint. Here we are parsing the form using the  `parse_reclass_form()` function. We will use a form with the delimiter '/', as shown above^^^.
  > Accessing the form values, then parsing with the 'parse_reclass_form()' function. Passing the form and delimiter parameter to the function. Then submitting our data using the 'submit_reclassed()' function.
  ~~~~
  if request.method == 'POST':
        # Access the forms values. In this example the values are a string containing " classlabel / text"
        reclass_form = request.form.to_dict()

        #  Use the parse_reclass_form() method to parse the form values.
        reclassed_items = erasehate.parse_reclass_form(reclass_form,'/')

        # Submit the reclassed items to the database.
        erasehateapi.submit_reclassed(reclassed_items)
  ~~~~
