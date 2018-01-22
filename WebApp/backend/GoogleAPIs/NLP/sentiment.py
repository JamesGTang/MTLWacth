from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
# URL for Google Cloud service access
DISCOVERY_URL = ('https://{api}.googleapis.com/'
                '$discovery/rest?version={apiVersion}')
# SentimentAnalyze method
# Input String of text
# Output Polarity and Mangintude
def sentimentAnalyze(text):
    print("Analyzing string: ",text)
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
    service_request = service.documents().analyzeSentiment(
    body={
     'document': {
        'type': 'PLAIN_TEXT',
        'content': text
        }
     })
    # process response
    response = service_request.execute()
    polarity = response['documentSentiment']['score']
    magnitude = response['documentSentiment']['magnitude']
    # print to console
    print('Sentiment: score of %s with magnitude of %s' % (polarity, magnitude))
    return 0

if __name__ == '__main__':
     sentimentAnalyze("Hello World")
