from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials

# URL for Google Cloud service access
DISCOVERY_URL = ('https://{api}.googleapis.com/'
                '$discovery/rest?version={apiVersion}')

# entityAnalyze method analyze sentiments and entities
# Input: String of text Output: entity
def entityAnalyze(text):
    print("Analyzing string for entity: ",text)
    # create http header
    http = httplib2.Http()
    # credentials with authroization
    credentials = GoogleCredentials.get_application_default().create_scoped(
     ['https://www.googleapis.com/auth/cloud-platform'])
    credentials.authorize(http)
    # app version and type
    service = discovery.build('language', 'v1beta2',
                           http=http, discoveryServiceUrl=DISCOVERY_URL)
    #create service request
    service_request = service.documents().analyzeEntitySentiment(
    body={
     'document': {
        'type': 'PLAIN_TEXT',
        'content': text
        }
     })
    # process response
    return service_request.execute()
