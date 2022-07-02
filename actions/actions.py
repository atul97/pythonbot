# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import time
#
#
# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
import json
import requests
import psycopg2
from psycopg2 import Error

from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)


user = os.getenv('user') ##"postgres"
password = os.getenv('password') ##"456852"
host = os.getenv('host') ##"127.0.0.1"
port = os.getenv('port') ##"5432"
database = os.getenv('database') ##"rasa_db"



def store_database(data1,data2,data3,data4,data5):
    try:
        connection = psycopg2.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)

        cursor = connection.cursor()

        # insert_query = f"insert into user_table values('{data1}','{data2}','{data3}')"
        postgres_insert_query = """ INSERT INTO user_table (sender_id, latest_event_time, latest_message, slots, followup_action) VALUES (%s,%s,%s,%s,%s)"""

        record_to_insert = (data1,str(data2),str(data3),str(data4),data5)
        cursor.execute(postgres_insert_query, record_to_insert)

        # insert_query = f''' insert into user_table values('{data1}','{data2}','sdf')'''
        # print(insert_query)
        # cursor.execute(insert_query)
        connection.commit()

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
def get_conversation(sender_id):

    base_url= f'http://localhost:5005/conversations/{sender_id}/tracker'
    response = requests.get(base_url)
    result=response.json()
    return result


class GetSenderid(Action):

    def name(self) -> Text:
        return "action_get_senderid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        tracker_ = tracker.current_state()['sender_id']
        
        print(tracker_)

        dispatcher.utter_message(text=tracker_)

        return []

class WriteConversationToDB(Action):

    def name(self) -> Text:
        return "write_conversation_to_db"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        senderid = tracker.sender_id

        # print(f'{senderid}')
        
        store_database(tracker.sender_id,f'{tracker.latest_event_time}',tracker.latest_message,tracker.slots,tracker.followup_action)
        dispatcher.utter_message(text=senderid)

        return []
