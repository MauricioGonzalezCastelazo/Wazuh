import requests
import json 
from base64 import b64encode
import urllib3
import io 
#NO DEJARSE EXPLOTAR ***NUNCAAAAAAA***
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class API: 
    def __init__(self, ip): 
        self.user = 'wazuh-wui'
        self.passw = 'wazuh-wui'
        self.url = f'https://{ip}:55000/'
        self.auth = f'{self.user}:{self.passw}'.encode()
        self.headers = {
            'Authorization' : f'Basic {b64encode(self.auth).decode()}',
            'Content-Type': 'application/json'
        }
        token_url = self.url+'security/user/authenticate'
        self.token = self.get_response("POST", token_url, self.headers)
        if self.token and "data" in self.token and "token" in self.token["data"]:
            self.headers['Authorization'] = f'Bearer {self.token["data"]["token"]}'
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
 
    def addDecoderRule(self, type, fileName, Content): 
        file = io.BytesIO(Content.encode('utf-8'))
        files = {'file' : ('pruebas.xml', file)}
        endpoint = f'{type}/files/'
        url = self.url+endpoint+fileName
        endpoint = endpoint+fileName
        new_header = {
            'Authorization' : self.headers['Authorization'], 
            'Content-Type': 'application/octet-stream'
        }
        try: 
            response = requests.put(url, headers = new_header, files=files, verify = False)
            response.raise_for_status()
            print("Se ha modificado con exito")
            return response.json()
        except Exception as e: 
            print(f"No se pudo modificar {e}")


    def updateDecoderRule(self, type, fileName, Content): 
        file = io.BytesIO(Content.encode('utf-8'))
        files = {'file' : ('pruebas.xml', file)}
        endpoint = f'{type}/files/'
        url = self.url+endpoint+fileName+'?overwrite=true'
        endpoint = endpoint+fileName
        new_header = {
            'Authorization' : self.headers['Authorization'], 
            'Content-Type': 'application/octet-stream'
        }
        try: 
            response = requests.put(url, headers = new_header, files=files, verify = False)
            response.raise_for_status()
            print("Se ha modificado con exito")
            return response.json()
        except Exception as e: 
            print(f"No se pudo modificar {e}")

        
    def get(self, type): 
        endpoint = f'{type}/files/'
        url = self.url+endpoint
        new_header = {
            'Authorization' : self.headers['Authorization'], 
            'Content-Type' : 'application/json'
        }
        try: 
            response = requests.get(url, headers = new_header, verify = False)
            response.raise_for_status()
            data = response.json()
            filtered_decoders = [decoder for decoder in data['data']['affected_items']
                                 if decoder['relative_dirname'].startswith('etc/decoders')]
            print(f"Se ha obtenido la informacin con exito {filtered_decoders}")
            return filtered_decoders
        except Exception as e: 
            print(f"No se pudo modificar {e}")

    def log_test(self, log, file): 
        path = '/var/ossec/etc/decoders/'
        endpoint = self.url+'logtest'
        json_log = {
            "log_format":"syslog",
            "location": path+file,
            "event": log
        }
        try:
            response =  requests.put(endpoint, headers = self.headers, json=json_log, verify = False)
            print(response.text)
            return response
            
        except Exception as e: 
            print(f'No se pudo hacer el log test: {e}')
            return None
             


        
#xml = """
# <rule id="100011" level="5">
#    <match>Menor 10K</match>
#    <description>Registro creado de manera exitosa</description>
#  </rule>
#"""
xml = """
<decoder name="Prueba">
                    <prematch>pelos</prematch>
                </decoder>

                <decoder name="mi-decoder-pelos">
                    <parent>Prueba</parent>
                    <regex type="pcre2">nombre=([A-Z][a-z]+)</regex>
                    <order>nombre</order>
                </decoder>\n\n
                    """


api = API("192.168.0.211")
#api.addDecoderRule("decoders","Pruebas.xml", xml)
#print(api.log_test("Mar 09 16:38:40 sa05 pelos nombre=Jaime", "Pruebas.xml"))
api.get('decoders')
#a="<regex>nombre=([A-Z][a-z]+)</regex>"