from datetime import datetime

def get_part_of_day(hour):
    return (
        "morning" if 5 <= hour <= 11
        else
        "afternoon" if 12 <= hour <= 17
        else
        "evening" if 18 <= hour <= 23
        else
        "night"
    )

def get_actual_period():
    h = datetime.now().hour
    return get_part_of_day(h)

def get_entity_by_name(tracker, name):
    if len(tracker.latest_message['entities']):
        found_entity = None
        for entity in tracker.latest_message['entities']:
            if(entity['entity'] == name):
                found_entity = entity
                break
        return found_entity
    else: 
        return None

def get_last_utter_action(tracker):
    print("tracker", tracker)
    ##goes back through the list of events and finds
    ##the last utter_action
    for event in reversed(tracker.events):
        try:
            #print("current action name is", event.get('name'))
            if event.get('name') not in [ 'action_listen', None ] :
                last_utter_action = event.get('name')
                print('found action', last_utter_action)
                return last_utter_action
            else :
                #print(event.get('name'))
                pass
        except:
            pass
            #print(event.get('text'))
    return 'error! no last action found'