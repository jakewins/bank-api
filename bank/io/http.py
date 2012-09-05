
from httplib2 import Http
from urllib import urlencode
import json

class HttpJsonClient(object):
    ''' A dead simple http client for talking to REST-like services that speak JSON.
    '''
    
    def __init__(self, base_url):
        self.base_url = base_url
        self._http = Http()
        self._persistent_headers = {
            'Accept' : 'application/json',
        	'Content-Type' : 'application/json; charset=utf-8',
        }
        
    def get(self, path, query_params={}):
        return self.request("GET", path, query_params=query_params, post_args={})
        
    def put(self, path, data={}, query_params={}):
        return self.request("PUT", path, query_params=query_params, post_args=data)
        
    def post(self, path, data={}, query_params={}):
        return self.request("POST", path, query_params=query_params, post_args=data)
        
    def delete(self, path, query_params={}):
        return self.request("DELETE", path, query_params=query_params, post_args=data)
    
    def add_persistent_header(self, key, value):
        self._persistent_headers[key] = value
    
    def request(
            self,
    		method,
    		path,
    		headers = {},
    		query_params = {},
    		post_args = {}):

    	for k,v in self._persistent_headers.items():
    	    if not headers.has_key(k):
    	        headers[k] = v
    	
    	url = self.build_url(path, query_params)
    	
    	response, content = self._http.request(
    			url,
    			method,
    			headers = headers,
    			body = json.dumps(post_args))

    	# error checking (super naive right now, but good enough. Expand when necessary)
    	if response.status == 401:
    		raise Exception("Unauthorized: " + str(response))
    	if response.status != 200:
    		raise Exception("Non-200 reply: " + str(response))
    		
    	return json.loads(content)
    	
    def build_url(self, path, query = {}):
		url = self.base_url
		if path[0:1] != '/':
			url += '/'
		url += path

		if len(query) > 0:
			url += '?'+urlencode(query)

		return url