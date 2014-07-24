
#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mayan.settings")
#from mayan.apps.sources.models import BaseModel

import time
import requests

from api import (
    get_one_not_uploaded_document,
    upload_document,
    mark_document_uploaded,
)

from token import get_token

class Uploader(object):

    def __init__(self,username,password,domain="http://127.0.0.1/"):

        self.domain = domain
        self.token = get_token(username, password, self.domain)

    def upload_document_to_mayan(self,document):

        success = False
        try:

            doc_url = document['doc_url']
            r = requests.get(doc_url, stream=True)

            upload_document(r.content,self.token,self.domain)

            mark_document_uploaded(document['_id']) 

            success = True

        except:
            pass

        return success

    def upload_loop(self):
 
        while( True ):
 
            print "Getting one document ..."

            document = get_one_not_uploaded_document()

            #print "Document:"
            #print document
  
            if document != None:
 
                print "Uploading document to mayan ..."

                self.upload_document_to_mayan(document)

            time.sleep(1)

            #raise Exception('debug')    


if __name__ == '__main__':

    username = 'admin' #'barkingowl'
    password = 'YxBGqsd8tF' #'bopass'
    domain = 'http://127.0.0.1:8000/'

    uploader = Uploader(username,password,domain)
    uploader.upload_loop()

