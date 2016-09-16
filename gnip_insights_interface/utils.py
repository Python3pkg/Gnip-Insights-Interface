import os
import yaml
from requests_oauthlib import OAuth1

from .exceptions import CredentialsException

def get_query_setup(api="audience",no_token_creds=False):
    """ 
    Do authentication and credentials stuff
    
    The 'api' keyword-argument must be 'audience' or 'engagment'

    Setting 'no_token_creds' keyword-argument to True returns 
    an auth object with 'token' and 'token_secret' set to 
    empty strings.
    """

    if api != 'audience' and api != 'engagement':
        raise CredentialsException("'api' keyword-argument to get_query_setup must my 'audience' or 'engagment'")

    creds_file_path = os.getenv('HOME') + '/.twitter_api_creds'
    if not os.path.exists(creds_file_path): 
        raise CredentialsException('Credentials file at $HOME/.twitter_api_creds must exists!') 
    
    creds = None 
    url = None
    with open(creds_file_path,'r') as f:
        creds = yaml.load(f)
        url = creds[api]['url']
        if no_token_creds:
            try:
                auth = OAuth1(creds[api]['consumer_key'],creds[api]['consumer_secret'],"","")
            except (TypeError,KeyError) as e:
                raise CredentialsException('Credentials file at $HOME/.twitter_api_creds must contain the keys: username, consumer_key, consumer_secret, url') 
        else:
            try:
                auth = OAuth1(creds[api]['consumer_key'],creds[api]['consumer_secret'],creds[api]['token'],creds[api]['token_secret'])  
            except (TypeError,KeyError) as e:
                raise CredentialsException('Credentials file at $HOME/.twitter_api_creds must contain the keys: username, consumer_key, consumer_secret, token, token_secret, url') 
    json_header = {'Content-Type' : 'application/json'}

    return url,auth,json_header
