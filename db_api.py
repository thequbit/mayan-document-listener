import json
import datetime

from pymongo import MongoClient

_database_name = 'mayan-document-listener_db'
_uri = uri='mongodb://localhost:27017/'
_dbclient = MongoClient(uri)
_db = _dbclient[_database_name]
_documents = _db['documents']
_errors = _db['errors']

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

    updated_document = None
    try:
        document = _documents.find_one({'_id': document_id})

        updated_document = _documents.update(
            { '_id': document_id },
            document,
        )
    except:
        pass
    
    return updated_document

def get_one_not_uploaded_document():

    document = None
    try:
        document = _documents.find_one({'uploaded': False})
    except:
        pass
    
    return document

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
    try:
        responses = _errors.find()
        for response in responses:
            errors.append(response)
    except:
        errors = None
        pass
    return errors
