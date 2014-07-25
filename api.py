import urllib
import urllib2
import json
import datetime
import requests

from pymongo import MongoClient

_database_name = 'mayan-document-listener_db'
_mongo_uri = 'mongodb://localhost:27017/'
_dbclient = MongoClient(_mongo_uri)
_db = _dbclient[_database_name]
_documents = _db['documents']
_errors = _db['errors']

def get_token(username, password, domain="http://127.0.0.1/"):

    if domain[-1:] != '/':
        domain += '/'
    url = "%sapi/v0/rest_api/auth/token/obtain/" % domain
#    print "URL: %s" % url
    data = dict(username=username,password=password)
    response = requests.post(url, data=data)
#    print "Response: %s" % response.text
    obj = json.loads(response.text)
    token = obj['token']

    print "Token: %s" % token   
 
    return token

def _create_document(token, domain="http://127.0.0.1/"):

#    print "_create_document()"

    if domain[-1:] != '/':
        domain += '/'
    url = "%sapi/v0/documents/documents/" % domain
#    print "URL: %s" % url
    headers = {'Authorization': 'Token %s' % token}
    response = requests.post(url, headers=headers)
#    print "_create_document() Response: %s" % response.text
    obj = json.loads(response.text)
    url = obj['url']
    new_url = obj['new_version']
    uuid = obj['uuid']

    return url, new_url, uuid

def upload_document(doc_file, token, domain="http://127.0.0.1/"):

#    print "upload_document()"

    if domain[-1:] != '/':
        domain += '/'

    print "Creating document in mayan ..."

    url,new_url,uuid = _create_document(token, domain)

    print "Posting file to mayan ..."

#    print "new_version URL: %s" % new_url

    headers = {'Authorization': 'Token %s' % token}
    document = {'file': doc_file}
    response = requests.post(new_url, files=document, headers=headers)
#    print "upload_document() Response: %s" % response.text
    obj = json.loads(response.text)

    print obj

def add_document(source_id, doc_url, link_text, 
        scrape_datetime, url_data):

    document = {
        'source_id': source_id,
        'doc_url': doc_url,
        'link_text': link_text,
        'scrape_datetime': scrape_datetime,
        'insert_datetime': str(datetime.datetime.now()),
        'url_data': url_data,
        'uploaded': False,
    }

    _documents.insert(document)

    return document

def mark_document_uploaded(document_id):

#    updated_document = None
#    try:
    if True:
        document = _documents.find_one({'_id': document_id})

        document['uploaded'] = True

        print ''
        print 'Found Doc:'
        print document
        print ''

        updated_document = _documents.update(
            { '_id': document_id },
            document,
            upsert=False,
        )
   
        new_document = _documents.find_one({'_id': document_id})
 
        print ''
        print 'Updated Doc:'
        print new_document
        print ''

    #except:
    #    pass
    
    return updated_document

def get_one_not_uploaded_document():

    document = None
    #try:
    if True:
        document = _documents.find_one({'uploaded': False})
    #except:
    #    pass
    
    return document

def get_all_documents():

    documents = []
#    try:
    if True:

        responses = _documents.find()
        for response in responses:
            documents.append(documents)

#    except:
#        pass

    return documents

def add_error(error_type, error_text):

    error = {
        'error_source': error_source,
        'error_type': error_type,
        'error_text': error_text,
        'error_datetime': datetime.datetime.now()
    }
    _errors.insert(error)

    return error

def get_all_errers():

    errors = []
    #try:
    if True:
        responses = _errors.find()
        for response in responses:
            errors.append(response)
    #except:
    #    errors = None
    #    pass
    return errors

if __name__ == '__main__':

    domain = "http://127.0.0.1:8000/"
    token = get_token('admin', 'YxBGqsd8tF', domain)
    upload_document('document.pdf', token, domain)
