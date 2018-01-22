#exclude location that interferes with NLP
location_exclusion=["intersection","Road","road","rd","Street","street","st"]
#exlcude events that dose not concern
event_exclusion=["game","concert","football match","Football match","Soccer Match","soccer match"]
#update fetch information from database
event_inclusion=["fire","flooding","blizzard","winter storm"]

def checkLocation(location):
    for  i in location_exclusion:
        #print(i)
        # if the location is excluded
        if i == location:
            return 1
    return 0

def checkEvent(event):
    for  i in event_exclusion:
        # if the location is excluded
        if i == event:
            return 1
    return 0
# check if event is serious
# if serious then return 1
# loop through event list, the list is 
# ordered that the most serious event is at the beginning
def priorityEventInclusion(event):
    for i in event_inclusion:
        # if the location is excluded
        if i == event:
            return 1

