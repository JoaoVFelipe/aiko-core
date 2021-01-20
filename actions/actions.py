from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (SlotSet, EventType)

from datetime import datetime

################################## GENERAL ACTIONS ##################################
class ActionGreetUser(Action):
    """ Greets user by time of day, or just a normal greeting isn't the first use of the time period """

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        last_time_period = tracker.get_slot("time_period")
        name_entity = next(tracker.get_latest_entity_values("name"), None)

        time_utils = UtilsTime()
        actual_period = time_utils.get_actual_period()

        if(last_time_period and last_time_period == actual_period):
            if(name_entity):
                dispatcher.utter_message(template="utter_name_greeting", name=name_entity)
            else:
                dispatcher.utter_message(template="utter_general_greeting")
                return[]
        else:
            if(actual_period == "morning"):
                dispatcher.utter_message(template="utter_good_morning")
            elif(actual_period == "afternoon"):
                dispatcher.utter_message(template="utter_good_afternoon")
            elif(actual_period == "evening"):
                dispatcher.utter_message(template="utter_good_evening")
            elif(actual_period == "night"):
                dispatcher.utter_message(template="utter_good_night")

            return [SlotSet("time_period", actual_period)]


################################## BASIC COMMANDS ACTIONS ##################################
class ActionStartResource(Action):
    """ Start an resource based on the user request """
    def name(self) -> Text:
        return "action_start_resource"

    def run(self, dispatcher, tracker, domain) -> List[EventType]:  
        print('opening', next(tracker.get_latest_entity_values("resource")))
        return []

################################## UTILS FUNCTIONS ##################################
class UtilsTime():
    def get_part_of_day(self, hour):
        return (
            "morning" if 5 <= hour <= 11
            else
            "afternoon" if 12 <= hour <= 17
            else
            "evening" if 18 <= hour <= 23
            else
            "night"
        )

    def get_actual_period(self):
        h = datetime.now().hour
        return self.get_part_of_day(h)

