import requests
from requests.auth import HTTPBasicAuth
import json
from dotenv import load_dotenv
import os
from ast import literal_eval


load_dotenv()

def query(query_string) :
            r = requests.post(os.getenv('QUERY_URL'), auth = HTTPBasicAuth(os.getenv('USER_NAME'),os.getenv('PASS_WORD')), data= query_string)
            data_list = json.loads((r.text.replace('{ "response": "{"Evtx":[','[').replace('}]}" }','}]')))
            return data_list


def health_check():
    r = requests.get(os.getenv('HEALTH_URL') ,auth = HTTPBasicAuth(os.getenv('USER_NAME'),os.getenv('PASS_WORD')))
    if r.status_code == 200 :
        print('Connection ok,  status_code :',r.status_code)
        return True
    else:
        print ('Something is wrong with the connection, status_code:',r.status_code)
        return False

def ingest(name_of_entity, json_object_to_ingest):

    ingest_string = 'insert ' + str(name_of_entity) + ' ' + '{' + dict_to_ingest_string(json_object_to_ingest) + '}'
    r = requests.post(os.getenv('INGEST_URL'), auth = HTTPBasicAuth(os.getenv('USER_NAME'),os.getenv('PASS_WORD')), data= ingest_string )
    print (r.text)

def dict_to_ingest_string(input_dict):
    string_to_ingest = ''
    for item in input_dict:
        string_to_ingest += str(item) + ':' + '"' + str(input_dict[item]) + '"' + ','
    return string_to_ingest[:-1]
