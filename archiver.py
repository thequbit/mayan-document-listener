
import uuid
import datetime

from barking_owl import BusAccess

from db import add_document

def new_document_callback(payload):

    """
        payload = {
            'command': 'found_doc',
            'source_id': '6eae01ff-ce21-4122-9f25-cb39455aa78e',
            'destination_id': 'broadcast',
            'message':  {
                'doc_url': 'http://thedomain.com/thedocument.pdf',
                'link_text': 'the document you are looking for!',
                'url_data': {
                    'target_url': 'http://thedomain.com/',
                    'doc_type': 'application/pdf',
                },
                'scrape_datetime': '2014-07-17 21:34:56',
            }
        }
    """

    print "\nnew message:"

    print payload


    success = False
#    try:
    if True:

        if payload['command'] == 'found_doc':

            print "New document found!  Inserting ..."

            add_document(
                source_id = payload['source_id'],
                doc_url = payload['message']['doc_url'],
                link_text = payload['message']['link_text'],
                scrape_datetime = payload['message']['scrape_datetime'],
                url_data = payload['message']['url_data'],
            )

            print "Document inserted successfully.\n"

            success = True

#    except:
#        print "An error occured while adding the document to the database."
#        pass

    return success

if __name__ == '__main__':

    print "Starting Archiver ..."

    bus_access = BusAccess(
        my_id = uuid.uuid4(),
        address = 'localhost',
        exchange = 'barkingowl',
        DEBUG = False,
    )

    bus_access.set_callback(new_document_callback)

    print "Starting to listen on message bus ..."

    bus_access.listen()

    print "Exiting Archiver."
