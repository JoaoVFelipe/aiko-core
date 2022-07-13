# AIKO Project - Virtual Assistant

## AIKO-core
<div display="inline-block">
 <span>
   The CORE repository contains the necessary information for the assistant to understand the user's intentions.
   Thus, all platforms that implement a visualization for AIKO must access this service to obtain the answers and actions to be delivered according to each input provided by the user (acknowledgment of intentions).
    <br />
    <br />
    <b> OBS: </b>
    <i>
    The main data folder, that usually contains all information used for training the assistant was removed for privacy reasons, considering that all the information present in the files, if replicated, would make the assistant easily clonable. To keep the repository with the settings and other actions as public, it was decided to put the folder in a separated private repository.
    </i>
  </span>
</div>
  
## Technologies
  
   The technologies used for the creation of CORE so far, and necessary for the execution of the project were:
  
   * [Python 3.9.12] (http://python.org/)
   * [Rasa Open Source Core 3.1.0] (https://rasa.com/docs/)
   * [Duckling Parser] (https://duckling.wit.ai/)
  
  ## How to use?
 
   This applications follows the basic RASA structure. So, to run this project, you'll need to install RASA on your machine. I recommend following the RASA documentation to get started: https://rasa.com/docs/rasa/installation
   
   Start the Python Virtual enviroment
   * .\venv\Scripts\activate
   
   Access the /aiko-core folder and train the AIKO model by running (this can take a while, but only needs to be done once):
   * rasa train
   
   After trained, you can start the main API with the command:
   * rasa run -m models --enable-api --cors “*” --debug
   
   Start the Duckling parser docker container
   * docker run -p 8000:8000 rasa/duckling
  
   Yet in the /aiko-core folder, start the action server:
   * rasa run actions

  If everything goes right, you can start making some requests at http://localhost:(port)/webhooks/rest/webhook! 
  it is important to note that this project is in a very early development stage, therefore improvements will still be made in the structure in order to facilitate the execution and tests.

## Funcionalities
   * Execute programs, open sites and folders -- Training!
   * Set alarms and manage commitments -- Training!;
   * Control lights and home smart equipaments -- Planning; 
   * Other funcionalities are in discussion.
