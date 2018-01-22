from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
# URL for Google Cloud service access
DISCOVERY_URL = ('https://{api}.googleapis.com/'
                '$discovery/rest?version={apiVersion}')

# entityAnalyze method analyze synatx
# Input: String of text Output: entity
def syntaxAnalyze(text):
    print("Analyzing string for syntax: ",text)
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
    service_request = service.documents().analyzeSyntax(
    body={
     'document': {
        'type': 'PLAIN_TEXT',
        'content': text
        }
     })
    # process response
    response = service_request.execute()
    
    return response
