import requests
import datetime
import numpy as np



class classifier(object):

    '''
    erasehate.classifier(data,data_key='string')

    Model Server Handling. Used to send data to model server for classification, store , filter, and sort results.
    Instantiates the class object. Returns the class object(self), methods can be chained.

    ::input:: data - The data to store in the classifier object. The text data to classify is a part of this data

    ::attr:: .data - Class object attribue that contain the users data input. Set on instantiation of the class.
                    Accessed using classifier.data. If data input is a list the data is stored in dictionary at key 'text'.

    ::attr:: .data_key - Key where the text items are located within the users data input.
                            Used when the data input is a dict that contains other information. No data_key needed when the data input is a list.

    ::attr:: .obj.modelserver - URL string of the model serving server.
    ::attr:: .raw_output - the raw output returned from the model server. Contains the probability array. See docs for format.
    ::attr:: .use_mapping - Determines whether to map other user specified data to the prediction results. Default False.
    ::attr:: .results - Attribute of the class object that stores the formatted prediction results when mapping in use. with probability array converted to class labels
                        of 0,1,or 2. Results may include other mapped data.

    '''


    def __init__(self,data,data_key=None):
        #check if data input is a dict object. If not store the data in dict at key 'text'
        self.data = data if isinstance(data,dict) and data_key in data.keys() else {'text': data}
        # Use the specified data key, if none given and data input not a dictionary, use the default key 'text'
        self.data_key = data_key if isinstance(data,dict) and data_key in data.keys() else 'text'
        self.modelserver =  'http://erase-hate-env.vdpppw2jwx.us-west-1.elasticbeanstalk.com/api_receiver'
        self.raw_output =''
        self.use_mapping = False
        self.results= None



    '''
    .predict()

    Method to send data for prediction. Takes no input when called. Returns the class object. Can be chained

    Output/Return - self
    '''
    def predict(self):
        if isinstance(self.data[self.data_key],list):
            if all(isinstance(item, str) for item in self.data[self.data_key]):

                    print('****** Making Model Server Request *******')
                    resp_return= requests.post(url=self.modelserver, json=self.data[self.data_key])
                    print('***** Response Received *******')
                    results = resp_return.json()
                    if results['api_code'] == 500:
                        print("!!!! Model Server responded with error message. Request/Response completed !!!!")
                        print("!!!! Model Server response: {} !!!!".format(results['message']))
                        raise Exception('500 - Model Server API message: {}'.format(results['message']))

                    else:
                        self.raw_output = results
                        return self
            else:
                raise TypeError("Each item in the list must be a string. Strings in the list may use any string format [string ,'text','hello 3 world@',str(item)]")
        else:
            raise TypeError("Classification input must be a 1 dimensional list of strings. Check inputs- obj.data_key, obj.data attr's. Strings in the list may use any string format [string ,'text','hello 3 world@',str(item)]" )


    '''
    .map_data(map_data, persistent= True/False)

    Maps extra user spec'd data to prediction results. Used when a user inputs an dictionary object on instantiation. The prediction result set will include the mapped data.
    Mapped data should be lists parallel to the text sent for prediction. Meaning mapped_data[1] should be the data corresponding to textitem[1].
    Example: if map_data input was a single string: self.data[map_data] would exist and be list in parallel to self.data[data_key].

    The default formatted results output by the filter_class or groupby_class will contain a list of:
    [ [text1,classlabel,itemnumber] , [text2,classlabel,itemnumber]]

    After mapping.
    [ [text1,classlabel,itemnumber,mappeddata1_key1,mappeddata1_key2], [text2,classlabel,itemnumber,mappeddata2_key1,mappeddata2_key2]]

    ::input:: map_data - Key(s) where data to map is stored. The keys must exist in the data input the user used when the class object was initially created.
                        Example: if map_data input was a single string: self.data[map_data] would exist and be list in parallel to self.data[data_key].
                        May be a string ot list of strings.
    ::arg::   persistent=True/False - Used to make sure mapped data persists in all future .filter_class() or .groupby_class() calls.
                                        Default True.
    '''
    def map_data(self,map_data, persistent= True):
        results = []
        # If persistent = True. Set the use_mapping attribute to True. use_mapping tells other methods whether or not to include mapped data.
        if persistent == True:
            self.use_mapping = True
            # Notify user
            print(' Mapping persistent.Mapped data will persist in .filter_class() and .groupby_class() method outputs.')
        # check user input a list
        if isinstance(map_data, list):
            #iter through list of text items sent to prediction
            for i in range(len(self.data[self.data_key])):
                # convert prediction arrary to classlabel of 0,1,or 2
                # create a list item that contains the [text,classlabel,item number]
                results.append([ self.data[self.data_key][i], np.argmax(self.raw_output['prediction_array'][i]), f'ITEM {str(i+1)}'  ])
                # iter through the keys where mapped data it stored
                for key in map_data:
                    # add the mapped data to the list item created above. Mapped data keys value
                    # should be a list parallel to the list of string items sent to prediction.
                    results[i].append(self.data[key][i])
            # Store mapped results. Filter_class and group_by will use this attribute for their process.
            self.results = results
            return self
        # check if user input a single string.
        elif isinstance(map_data,str) or isinstance(map_data, int):
            for i in range(len(self.data[self.data_key])):
                results.append([ self.data[self.data_key][i], np.argmax(self.raw_output['prediction_array'][i]), f'ITEM {str(i+1)}', self.data[map_data][i]  ])
            self.results = results
            return self
        # If neither list of single string. Raise error.
        else:
            raise TypeError('First arg(the location/key(s) of data to map) must be a list, string, or integer. Or a single string or integer.')


    '''
    .filter_class(keyword='', include_mapped = False/True)

    Method that returns formtted unsorted,and/or formatted filtered results containing: ([Class label,  text item ,unique item number]).
    Prediction array values are converted to a class label. Method returns a value and cannot be chained. If data mapping in use. Results will include mapped data.

    output/return - [ [ text(str), classlabel(str), item number(str) ] ]

    ::kwarg:: keyword - keyword used to filter results. Can be 'hate', 'offensive', 'neither'. Default None.
                        Default returns complete unsorted results, class labels are applied.
    ::arg::  include_mapped - Include mapped results in output. Used when map_data was called without persistent= True.
                                include_mapped default is False.
    '''
    def filter_class(self,keyword=None, include_mapped=False):
        # Using mapping or include_mapped = True
        if include_mapped == True or self.use_mapping:
            print('Data mapping in use. Result set will include mapped data')
            if keyword:
                # determine is keyword is valid. then iter through mapped data results.
                if keyword.strip().lower() == 'hate':
                    return [item for item in self.results if item[1] == 0]
                elif keyword.strip().lower() == 'offensive':
                    return [item for item in self.results if item[1] == 1]
                elif keyword.strip().lower() == 'neither':
                    print ('im here in neither')
                    return [item for item in self.results if item[1] == 2]
                elif keyword and not None:
                    raise ValueError("Filter key word must be 'hate', 'offensive', 'neither', or None ")

            # if no keyword given, return unsorted data stored at/in self.results
            else:
                return self.results

        #Not using mapping
        else:
            if keyword:
                if keyword.strip().lower() == 'hate':
                    return [[self.data[self.data_key][i],np.argmax(self.raw_output['prediction_array'][i]),f'ITEM {str(i+1)}'] for i in range(len(self.data[self.data_key])) if int(np.argmax(self.raw_output['prediction_array'][i]) == 0)]
                elif keyword.strip().lower() == 'offensive':
                    return [[self.data[self.data_key][i],np.argmax(self.raw_output['prediction_array'][i]),f'ITEM {str(i+1)}'] for i in range(len(self.data[self.data_key])) if int(np.argmax(self.raw_output['prediction_array'][i]) == 1)]
                elif keyword.strip().lower() == 'neither':
                    return [[self.data[self.data_key][i],np.argmax(self.raw_output['prediction_array'][i]),f'ITEM {str(i+1)}'] for i in range(len(self.data[self.data_key])) if int(np.argmax(self.raw_output['prediction_array'][i]) == 2)]
            elif keyword and not None:
                raise ValueError("Filter key word must be 'hate', 'offensive', 'neither', or None ")
            else:
                return  [[self.data[self.data_key][i],np.argmax(self.raw_output['prediction_array'][i]),f'ITEM {str(i+1)}'] for i in range(len(self.data[self.data_key]))]



    '''
    .groupby_class(include_mapped = False/True)

    Method that returns formtted and grouped results containing: ([Class label,  text item ,unique item number]).
    Prediction array values are converted to a class label. Method returns a value and cannot be chained.
    If include mapped, result sets will include mapped data.

    output/return - {
                    hate:[(text(str), classlabel(str), item number(str))]
                    neither:
                    offensive
                    }

    ::arg:: include_mapped - Determines whether or not to include mapped data in the result sets. Default is false.

    '''
    def groupby_class(self, include_mapped= False):
        if self.use_mapping or includE_mapped == True:
            grouped = {
                'hate': [item for item in self.results if item[1] == 0],
                'offensive':[item for item in self.results if item[1] == 1],
                'neither':[item for item in self.results if item[1] == 2]
            }
            return grouped
        else:
            grouped = {
                "hate": [[self.data[self.data_key][i],np.argmax(self.raw_output['prediction_array'][i]),f'ITEM {str(i+1)}'] for i in range(len(self.data[self.data_key])) if int(np.argmax(self.raw_output['prediction_array'][i]) == 0)],
                'offensive':[[self.data[self.data_key][i],np.argmax(self.raw_output['prediction_array'][i]),f'ITEM {str(i+1)}'] for i in range(len(self.data[self.data_key])) if int(np.argmax(self.raw_output['prediction_array'][i]) == 1)],
                'neither': [[self.data[self.data_key][i],np.argmax(self.raw_output['prediction_array'][i]),f'ITEM {str(i+1)}'] for i in range(len(self.data[self.data_key])) if int(np.argmax(self.raw_output['prediction_array'][i]) == 2)]
            }
        return grouped
