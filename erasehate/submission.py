import requests

def reclass_submission(reclassed):
    if isinstance(reclassed, list):
            if all(isinstance(item, list) for item in reclassed):
                if all(isinstance(item[0], (str,int)) for item in reclassed):
                    if all(isinstance(item[1], str) for item in reclassed):
                        reclass_submit_url = 'https://www.erasehateapp.com/api_reclass_submit'
                        response = requests.post(url= reclass_submit_url, json=reclassed)
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
