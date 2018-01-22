from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
import base64

# URL for Google Cloud service access
ADP = ('https://{api}.googleapis.com/'
                '$discovery/rest?version={apiVersion}')

# imageAnalyze method analyze sentiments and entities
# Input: Image Output: JSON
def locationAnalyze(photo_file):
    #print("Analyzing image. ")
    # create http header
    httpAddress = httplib2.Http()
    # credentials with authroization
    cred = GoogleCredentials.get_application_default().create_scoped(
     ['https://www.googleapis.com/auth/cloud-platform'])
    cred.authorize(httpAddress)
    # app version and type
    # using v1 of cloud vision service
    service = discovery.build('vision', 'v1', http=httpAddress, discoveryServiceUrl=ADP)
    #create service request
    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(
            body={
                'requests': [{
                'image': {
                'content': image_content.decode("utf-8")
                },
                'features': [{
                'type': 'LANDMARK_DETECTION',
          }]
        }]
     })
    # process response
    return service_request.execute()