import yaml
import os
from . import utils
from . import service

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
    async def extract_reminder_time(
        dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        reminder_time = None
        time_info = utils.extract_time_entity(tracker=tracker);
        return {"reminder_time": time_info}

class ValidateAlarmForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_alarm_form"

    @staticmethod
    async def extract_reminder_time(
        dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        reminder_time = None
        time_info = utils.extract_time_entity(tracker=tracker);
        return {"reminder_time": time_info}

class ValidateTimerForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_timer_form"

    @staticmethod
    async def extract_reminder_duration(
        dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        reminder_duration = None
        time_info = utils.get_entity_by_name(tracker=tracker, name='duration');

        if time_info:
            second_duration = time_info['additional_info']['normalized']['value']
            return {"reminder_duration": second_duration}

class ActionSetReminder(Action):
    """ Set an basic reminder based on the user request"""
    def name(self) -> Text:
        return "action_set_reminder"

    def run(self, dispatcher, tracker, domain) -> List[EventType]: 
        print("chamou o set reminder")

        reminder_time = tracker.get_slot("reminder_time")
        reminder_name = tracker.get_slot("reminder_name")
        reminder_type = tracker.get_slot("reminder_type")
        reminder_basetime = utils.get_actual_datetime()
        reminder_duration = tracker.get_slot("reminder_duration")
        

        print("time", reminder_time, reminder_name, reminder_type)

        reminder_info = {
            'name': reminder_name, 
            'type': reminder_type, 
            'basetime': reminder_basetime, 
            'duration': reminder_duration
        }

        if(reminder_time):
            reminder_info['date'] = reminder_time['date'];
            reminder_info['time'] = reminder_time['time'];

        print("reminder info set", reminder_info)
        return [SlotSet("reminder_info", reminder_info), 
                SlotSet("reminder_name", None), 
                SlotSet("reminder_time", None), 
                SlotSet("reminder_duration", None), 
                SlotSet("reminder_type", None)]


class ActionSetReminderType(Action):
    """ Set the reminder type"""
    def name(self) -> Text:
        return "action_set_reminder_type"

    def run(self, dispatcher, tracker, domain) -> List[EventType]: 
        print("setando reminder type")

        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dir_path, "reminders.yml")

        defined_reminder_type = None
        defined_reminder_entity = utils.get_entity_by_name(tracker, 'reminder_type')
        defined_reminder_name = tracker.get_slot("reminder_name")
        
        if(defined_reminder_entity):
            defined_reminder_type = defined_reminder_entity['value']

        print("REMINDERS TYPE", defined_reminder_type)

        categorized_reminder_type = None

        if(defined_reminder_type):
            with open(path, 'r') as file:
                reminders_type_list = yaml.load(file, Loader=yaml.FullLoader)
                for reminder_type, type_info in reminders_type_list.items():
                    for name in type_info[0]["alternative_names"]:
                        print("REMINDERS TYPE 2", name, defined_reminder_type)
                        if (name == defined_reminder_type):
                            categorized_reminder_type = reminder_type
                            print("SETOU O CATEGORIZED", categorized_reminder_type, reminder_type)
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