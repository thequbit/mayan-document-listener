import requests

# this is sudo code as I don't really know how to get to the BaseModel class ...
from mayan.apps.sources.models.BaseModel as MayanDocument

from db_api import (
    get_one_not_uploaded_document,
    mark_document_uploaded,
)

def upload_document_to_mayan(document):

    """
    {
        u'uploaded': False,
        u'doc_url': u'http: //timduffy.me/Resume-TimDuffy-20130813.pdf',
        u'url_data': {
            u'status': u'running',
            u'doc_type': u'application/pdf',
            u'start_datetime': u'2014-07-1815: 32: 34',
            u'target_url': u'http: //timduffy.me/',
            u'max_link_level': 3,
            u'description': u"Tim Duffy's Personal Website",
            u'title': u'TimDuffy.Me',
            u'runs': [
                
            ],
            u'scraper_id': u'692127e0-9d3a-4f99-ae39-f206e2a32f75',
            u'frequency': 2,
            u'finish_datetime': u'',
            u'creation_datetime': u'2014-07-1815: 32: 34',
            u'allowed_domains': [
                
            ]
        },
        u'link_text': u'Resume',
        u'scrape_datetime': u'2014-07-1815: 32: 35',
        u'insert_datetime': u'2014-07-1815: 32: 35.075349',
        u'source_id': u'692127e0-9d3a-4f99-ae39-f206e2a32f75',
        u'_id': ObjectId('53c97653a70f9e356ba0df44')
    }
    """

    success = False
    try:

        # pull the document url out of the payload
        doc_url = document['doc_url']

        # get the file handle from requests
        r = requests.get(doc_url, stream=True)

        # this is sudo code, as I don't know how to connect to mayan yet :/
        mayan_document = MayanDocument()
        mayan_document.upload_single_file( r )

        # mark as uploaded
        mark_document_uploaded(document['_id']) 

        # success!
        success = True

    except:
        pass

    return success

def upload_loop():

   while( True ):

       document = get_one_not_uploaded_document()

       if document != None:

           upload_document_to_mayan(document)

       sleep(.1)

if __name__ == '__main__':

    upload_loop()

