import requests
import json 
from base64 import b64encode
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class API: 
    def __init__(self, ip): 
        self.user = 'admin'
        self.passw = 'admin'
        self.url = f'https://{ip}:55000/'
        self.auth = f'{self.user}:{self.passw}'.encode()
        self.headers = {
            'Authorization' : f'Basic {b64encode(self.auth).decode()}',
            'Content-Type': 'application/json'
        }
        token_url = self.url+'security/user/authenticate'
        token = self.get_response("POST", token_url, self.headers)
        print(token)
        if token and "data" in token and "token" in token["data"]:
            self.headers['Authorization'] = f'Bearer {token["data"]["token"]}'
        else:
            print("No se pudo obtener el token")


    def get_response(self, request_method, url, headers, verify=False, body=None):
        """Get API result"""
        if body is None:
            body = {}

        try: 
            request_result = getattr(requests, str(request_method).lower())(url, headers=headers, verify=verify, data=json.dumps(body))

            if request_result.status_code == 200:
                return json.loads(request_result.content.decode())
            else:
                raise Exception(f"Error obtaining response: {request_result.json()}")
        except Exception as e:
            print(f'Ocurrió un error: {e}')
            return None 

            

api = API("192.168.0.158")
