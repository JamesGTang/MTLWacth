import NLP.entity as et
import subprocess
import NLP.syntax as sa
import service.util as ut
import DB.dataController as dc
from json import loads, dumps
import sys

# entity types from enums.Entity.Type
entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

# weight organization as less specific than street address
secondary_location_shift = 0.7
# Location list with salience
location = dict()
event = dict()

#err_msg sends error feedback
err_msg = ""

#set google credential to app instance
def setCredential():
    #must be changed to ~/GoogleAPIs/Hackatown2018-3dd19556fe93.json on server
    msg = subprocess.check_output('export GOOGLE_APPLICATION_CREDENTIALS=~/public_html/GoogleAPIs/OAuth/Hackatown2018-3dd19556fe93.json',shell=True)       
             
#process the input through sentiment & entity    
def process_input(text):
    if not setCredential() :
        #print ("Credential Defined")
        x=1
    else:
        print ("Abort, cannot authenticate cloud credential")
        sys.exit ("Cannot authenticate")
        
    entities = et.entityAnalyze(text)
    #syntaxes = sa.syntaxAnalyze(text)
    #print(syntaxes)
    for entity in entities ["entities"]:
        # if location is detected
        if entity["type"] == "LOCATION":
            # the location is not in the exclusion list
            if(dc.checkLocation(entity['name'])!=1):
                relevance = entity['salience']
                location_entity = entity ['name']
                location[location_entity]="\""+str(relevance)+"\""
                # else the location is no good
        if entity["type"] == "ORGANIZATION":
            # an organization should have mless weight because
            # an organization like Place des arts is less
            # specific than a street
            relevance = int(entity['salience'])*secondary_location_shift;
            location_entity = entity ['name']
            location[location_entity]="\""+str(relevance)+"\""
        # search for any event mentioning
        if entity["type"] == "EVENT":
            if(dc.checkEvent(entity['name'])!=1):
                relevance = entity['salience']
                event_entity = entity ['name']
                #event[event_entity]="\""+str(relevance)+"\""
                event[event_entity]=relevance
        # ToDo: add syntax processing to undertsand if no words or events have been found
        
        if(ut.is_empty(location)):
            err_msg = "Sorry we cannot find a location, please enter a location such as Sherbrooke Street"
        elif(ut.is_empty(event)):
            err_msg = err_msg+"Sorry we cannot find an event, please enter an event such as Flooding"      
           
    # this line should be removed
    # jsonString = "{\"Location\":"+dumps(location)+",\"Event\":"+dumps(event)+"}" 
    jsonString=dumps(event)
    return jsonString

def main():
    print (sys.argv[1])
    output=process_input(sys.argv[1])
    print (output)
    f= open("output.txt","w+")
    f.write(output)
    f.close()
    #return process_input(str(sys.argv[1]))
if __name__ == "__main__": main()
   









