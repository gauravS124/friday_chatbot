import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "friday-bot-qgyehp"
import requests
import json
from pymongo import MongoClient

def database(ssid,msg,reply,intent_name):
    print("=================='''''''''''''''''''''''''====================")
    print(ssid,msg,reply)
    client =MongoClient("mongodb+srv://friday:friday@cluster0-0qvxb.mongodb.net/test?retryWrites=true&w=majority")
    db=client.get_database("friday_bot")
    rec_alter=db.alter_word
    rec_rhyme=db.rhyming_word


    if intent_name == 'rhyming_words':
        new_entry={"session_id":ssid,"message":msg,"reply":reply}
        rec_rhyme.insert_one(new_entry)

    if intent_name == 'alternate_word':
        new_entry={"session_id":ssid,"message":msg,"reply":reply}
        rec_alter.insert_one(new_entry)







def get_rhyming(parameters):
    li=[]
    url="https://api.datamuse.com/words?rel_rhy="
    word=parameters["word"]
    url=url+word
    resp=requests.get(url)
    data=resp.text
    parsed=json.loads(data)
    for i in range(len(parsed)):
        if i>3:
            break
        li.append(parsed[i]["word"])

    ans=str(li)
    ans_for_db=ans
    ans=ans[1:-1]

    return ans
def get_alter(parameters):
    print(parameters)
    li=[]
    url="https://api.datamuse.com/words?ml="
    word=parameters["alword"]
    url=url+word
    resp=requests.get(url)
    data=resp.text
    parsed=json.loads(data)
    for i in range(len(parsed)):
        if i>3:
            break
        li.append(parsed[i]["word"])

    ans=str(li)
    ans=ans[1:-1]

    return ans



def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg,session_id):
    response = detect_intent_from_text(msg,session_id)
    query_by_user=msg
    ans=""

    print("==============================",msg,"===================")
    if response.intent.display_name == 'rhyming_words':
       ans=get_rhyming(dict(response.parameters))
       database(session_id,msg,ans,response.intent.display_name)
       return ans
    if response.intent.display_name == 'alternate_word':
       ans=get_alter(dict(response.parameters))
       database(session_id,msg,ans,response.intent.display_name)

       return ans
    else:
        return response.fulfillment_text
