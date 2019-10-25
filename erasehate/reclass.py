import requests
import datetime
# '''
#     Function to submit reclassed items to erasehateapp.com database.
#     The items will be used in further model training.
#
#     ::input:: reclassed_items - Reclassed data. Must be entered in form:
#     [['classlabel', 'text'], ['classlabel', 'text']]
# '''



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
