import request
import datetime
'''
    Function to submit reclassed items to erasehateapp.com database.
    The items will be used in further model training.

    ::input:: reclassed_items - Reclassed data. Must be entered in form:
    [['classlabel', 'text'], ['classlabel', 'text']]
'''

def sumbit_reclassed(reclassed_items):
    if isinstance(reclassed_items, list):
            if all(isinstance(item, list) for item in reclassed_items):
                if all(isinstance(item[0], str) for item in reclassed_items):
                    if all(isinstance(item[1], str) for item in reclassed_items):

                        reclass_submit_url = 'https://www.erasehateapp.com/api_reclass_submit'
                        response = requests.post(url= reclass_submit_url, json=reclassed_items)
                        # print(response)
                        response = response.json()
                        # print(response)
                        if response['api_code'] == 200:
                            print(' Reclassed Items Submit- Success')
                            return response
                        elif response['api_code'] == 500:
                            print('Reclassed Item Submit- FAIL ')
                            raise Exception('500 - {}'.format(response['message']))
                        elif response['api_code'] == 404:
                            print('Reclassed Item Submit- FAIL ')
                            raise Exception('404 - {}'.format(response['message']))
                        elif response['api_code'] == 403:
                            print('Reclassed Item Submit- FAIL ')
                            raise Exception('403 - {}'.format(response['message']))
                    else:
                        raise TypeError('Text item must be a string')
                else:
                    raise TypeError("Class label must be a string containing 0,1,or 2 - '0'=hate '1'=hurt/offensive '2'=neither")
            else:
                raise TypeError('Each item in reclassed list, must be a list, with class label at [0], text at [1]')
    else:
        raise TypeError(" Reclassed item input mus be a list of list as such: [['classlabel', 'text'], ['classlabel', 'text2'], ['classlabel', 'text3']]")


# Function that will spit out HTML reclass form boiler plate code as a flat txt file.
def reclassboiler_HTML():
    html_string = """<form action='/reclass_submit' method="POST" class="">
              <div class="col-12">
                <div id="reclass" class="col-12">
                  {% for item in reclass_data %}
                    <div class="row">
                      <p class='text-white'>{{ item[0] }}</p>
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
    with open("reclass_form_template.txt", "w") as text_file:
        text_file.write("{}".format(html_string))

# Function to parse form data when the boilerplate form is used.
def parse_reclass_form(form,delimiter):
    reclass_parsed = []
    for key in form:
        reclass_parsed.append([x.strip() for x in form[key].split(delimiter)])
    return reclass_parsed
