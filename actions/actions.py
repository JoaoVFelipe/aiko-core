import yaml
import os
from dateutil import parser
from . import utils

from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (SlotSet, EventType)
from rasa_sdk.types import DomainDict

################################## GENERAL ACTIONS ##################################
class ActionGreetUser(Action):
    """ Greets user by time of day, or just a normal greeting isn't the first use of the time period"""

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        last_time_period = tracker.get_slot("time_period")
        # name_entity = next(tracker.get_latest_entity_values("name"), None)

        actual_period = utils.get_actual_period()

        if(last_time_period and last_time_period == actual_period):
            # if(name_entity):
            #     dispatcher.utter_message(template="utter_name_greeting", name=name_entity)
            # else:
            dispatcher.utter_message(reponse="utter_general_greeting")
            return[]
        else:
            if(actual_period == "morning"):
                dispatcher.utter_message(reponse="utter_good_morning")
            elif(actual_period == "afternoon"):
                dispatcher.utter_message(reponse="utter_good_afternoon")
            elif(actual_period == "evening"):
                dispatcher.utter_message(reponse="utter_good_evening")
            elif(actual_period == "night"):
                dispatcher.utter_message(reponse="utter_good_night")

            return [SlotSet("time_period", actual_period)]

################################## BASIC COMMANDS ACTIONS ##################################
class ActionStartResource(Action):
    """ Start an resource based on the user request """
    def name(self) -> Text:
        return "action_start_resource"

    def run(self, dispatcher, tracker, domain) -> List[EventType]: 
        found_resource = False

        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(dir_path, "resources.yml")
            resource_name = tracker.get_slot("resource").lower().replace(" ", "_")

            with open(path, 'r') as file:
                resource_list = yaml.load(file, Loader=yaml.FullLoader)
                for resource_type, resources in resource_list.items():
                    for resource in resources:
                        if (resource["name"] == resource_name):
                            found_resource = True
                            break

                        if(resource['alternative_names'] != None):
                            for alternate_name in resource['alternative_names']:
                                if(alternate_name == resource_name):
                                    found_resource = True
                                    break
                    if found_resource:
                        break           
        except:
            dispatcher.utter_message(reponse="utter_resource_notfound")
            return
        if found_resource:
            dispatcher.utter_message(reponse="utter_opening_resource", resource=resource_name)
            return [SlotSet("last_opened_resource", resource_name)]
        dispatcher.utter_message(reponse="utter_resource_notfound")
        return

class ValidateReminderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_reminder_form"

    @staticmethod
    def validate_reminder_time(
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        reminder_time = {}
        print("entrou aqui na validação")

        # Gets event time sent on the last message
        if len(tracker.latest_message['entities']):
            for entity in tracker.latest_message['entities']:
                if(entity['entity'] == 'time'):
                    time = entity
        
        print("setou time", time)

        if not time == None:
            grain = time['additional_info']['grain']
            date_time_obj = parser.parse(time['value'])

            if(grain == 'hour'):
                reminder_date = date_time_obj.strftime("%d-%m-%Y")
                reminder_time = date_time_obj.strftime("%H:%M:%S")
            elif(grain == 'day'):
                reminder_date = date_time_obj.strftime("%d-%m-%Y")
            
            reminder_time = {'date': reminder_date, 'time': reminder_time, 'grain': grain}
            print("setou time", reminder_time)

            return {"reminder_time": reminder_time}
        return {"reminder_time": None}

class ValidateAlarmForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_alarm_form"

    @staticmethod
    def validate_reminder_time(
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        reminder_time = {}
        print("entrou aqui na validação")

        # Gets event time sent on the last message
        if len(tracker.latest_message['entities']):
            for entity in tracker.latest_message['entities']:
                if(entity['entity'] == 'time'):
                    time = entity
        
        print("setou time", time)

        if not time == None:
            grain = time['additional_info']['grain']
            date_time_obj = parser.parse(time['value'])

            if(grain == 'hour'):
                reminder_date = date_time_obj.strftime("%d-%m-%Y")
                reminder_time = date_time_obj.strftime("%H:%M:%S")
            elif(grain == 'day'):
                reminder_date = date_time_obj.strftime("%d-%m-%Y")
            
            reminder_time = {'date': reminder_date, 'time': reminder_time, 'grain': grain}
            print("setou time", reminder_time)

            return {"reminder_time": reminder_time}
        return {"reminder_time": None}
        

class ActionSetReminder(Action):
    """ Set an basic reminder based on the user request"""
    def name(self) -> Text:
        return "action_set_reminder"

    def run(self, dispatcher, tracker, domain) -> List[EventType]: 
        reminder_time = tracker.get_slot("reminder_time")
        reminder_name = tracker.get_slot("reminder_name")
        reminder_type = tracker.get_slot("reminder_type")

        print("time", reminder_time, reminder_name, reminder_type)

        reminder_info = {
            'date': reminder_time['date'], 'time': reminder_time['time'], 'name': reminder_name, 'type': reminder_type 
        }
        return [SlotSet("reminder_info", reminder_info), SlotSet("reminder_name", None), SlotSet("reminder_time", None)]


class ActionSetReminderType(Action):
    """ Set the reminder type"""
    def name(self) -> Text:
        return "action_set_reminder_type"

    def run(self, dispatcher, tracker, domain) -> List[EventType]: 
        print("setando reminder type")

        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dir_path, "reminders.yml")

        defined_reminder_type = utils.get_entity_by_name(tracker, 'reminder_type')
        defined_reminder_name = tracker.get_slot("reminder_name")

        categorized_reminder_type = None

        if(defined_reminder_type):
            with open(path, 'r') as file:
                reminders_type_list = yaml.load(file, Loader=yaml.FullLoader)
                print("REMINDERS TYPE", defined_reminder_type)
                for reminder_type, type_info in reminders_type_list.items():
                    print("REMINDERS TYPE 2", reminder_type, type_info)
                    if (type_info[0]["alternative_names"] == defined_reminder_type):
                        categorized_reminder_type = reminder_type
                        break
                        
        if categorized_reminder_type:
            print("setou", categorized_reminder_type)
            return [SlotSet("reminder_type", categorized_reminder_type)]   
        else:
            if defined_reminder_name:
                print("setou: reminder")
                return [SlotSet("reminder_type", 'reminder')]
            else:
                print("setou: alarm")
                return [SlotSet("reminder_type", 'alarm')]

################################## SMART HOME ACTIONS ##################################
class ActionExecuteSmartHomeAction(Action):
    """Execute a generic action related to home automation"""
    def name(self) -> Text:
        return "action_execute_home_action"

    def run(self, dispatcher, tracker, domain) -> List[EventType]: 
        ## Get the last intent, and return the action and room based on it.
        return