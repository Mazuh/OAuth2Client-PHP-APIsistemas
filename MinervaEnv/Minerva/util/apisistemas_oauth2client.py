"""
A simple OAuth 2 Client.

For more details about what was needed to build this script, check out APISistemas doc:
https://api.ufrn.br/

Thanks to who did this OAuth Client original code:
@ymotongpoo (who did it in Python, basead in a Java code): https://gist.github.com/ymotongpoo/1907281
@shin1ogawa (who did it in Java): https://gist.github.com/shin1ogawa/1899391
I did a lot of modifications, but I had no idea from where to begin, and the codes above helped me so much.
"""

import requests # To read: http://docs.python-requests.org/en/master/user/quickstart/
import json

#from urllib3 import urlencode

import logging
from . import keyring



# try to get security keys to access APISistemas
sinfo_api_dict = keyring.get(keyring.SINFO_API)

# security data
CLIENT_ID     = sinfo_api_dict['client-id']
CLIENT_SECRET = sinfo_api_dict['client-secret']

# important URLs for APISistemas
API_URL_ROOT           = 'http://apitestes.info.ufrn.br/' # API root (it's a test security link for now)
AUTHORIZATION_ENDPOINT = API_URL_ROOT + 'authz-server/oauth/authorize' # auth
TOKEN_ENDPOINT         = API_URL_ROOT + 'authz-server/oauth/token' # token

# other URLs for some available services
URL_SERVICES = {
    'ensino'        : API_URL_ROOT + 'ensino-services/services/',
    'usuario'       : API_URL_ROOT + 'usuario-services/services/', # deprecated
    'stricto-sensu' : API_URL_ROOT + 'stricto-sensu-services/services/',
    'docente'       : API_URL_ROOT + 'docente-services/services/',
}

# post graduation numerical codes from SIGAA(.ufrn.br) database
SIGAA_PROGRAM_CODES = {
    'PPGP': '1672'
}



def has_app_credentials():
    """
    Return True if credentials retrieving went ok, 
    and False if they're None or raised an Excepton.
    """
    return (CLIENT_ID is not None) and (CLIENT_SECRET is not None)



def retrieve_token():
    """
    Retrieve access_token as a json and convert it to dict in a global variable.
    
    Return the data string (only the token itself) if it could be retrieved (successfully or not), 
    and None if it could not be done due to lack of credentials.
    TODO: better exception handling for situations where server could not respond
    or the application access has been somehow denied.
    """
    
    if not has_app_credentials():
        return None
    
    query_params = {
        'client_id'     : CLIENT_ID,
        'client_secret' : CLIENT_SECRET,
        'grant_type'    : 'client_credentials',
    }

    returned_data = requests.post(TOKEN_ENDPOINT, data=query_params)
    dict_data = json.loads(returned_data.text)
    return dict_data['access_token'] # what is the return type if json cannot be loaded?



def user_authorization_url():
    """
    Assemble (and return) URL for this application redirect (GET) to the authentication server.
    
    Return the URL string if it could be assembled, 
    and None if it could not be done due to lack of credentials.
    """
    
    if not has_app_credentials():
        return None
    
    query_params_str  = '?client_id='+CLIENT_ID
    query_params_str += '&response_type=code'
    query_params_str += '&redirect_uri=http://localhost:4444/dashboard' # sinfo's servers cant find 'localhost'

    return AUTHORIZATION_ENDPOINT + query_params_str
