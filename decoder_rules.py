from API import API
from openai import OpenAI
import os
from dotenv import load_dotenv
import re
import threading

load_dotenv("config.env")
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("La clave API de OPENAI no está definida en las variables de entorno.")

client = OpenAI(api_key=api_key)

class Decoder: 
    def __init__(self): 
        self.api = API("192.168.1.193")
        self.lock = threading.Lock()
        self.resultados = {}  

    def process_key(self, key, diccionario): 
        for ex in diccionario[key]:
            left_side = ex
            prompt = """
            Make a regular expression that can identify what is after the equal for '{left_side}', generalizing. If they are words or numbers after the equal, then a regular expression that can identify them, ignoring uppercase and lowercase. Write it with the following syntax: regex: expression
            """
            try: 
                regular_expresion = self.generate_regular_expresion(prompt)
                print(regular_expresion)
                if(regular_expresion): 
                    with self.lock:  # Asegura el acceso exclusivo al diccionario
                        if key not in self.resultados:
                            self.resultados[key] = []
                        self.resultados[key].append(f"{ex}: {regular_expresion}")
                    print(f"Se ha generado la expresion regular {key}:{ex}: {regular_expresion}")
                    #self.updateDecoder(fileName=file_name, xml=xml) 

                else: 
                    print("No se pudo generar la expresion regular")

            except Exception as e:
                print(f"Hubo una excepcion: {e}")

    def generate_decoder(self, diccionario, file_name, xml): 
        for key in diccionario.keys(): 
            t = threading.Thread(target=self.process_key, args=(key, diccionario))
            t.start()

    def generate_regular_expresion(self, prompt): 
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a regular expression creator assistant"},
            {"role": "user", "content": prompt}
        ],
        )
        expresion = completion.choices[0].message.content.split(": ")
        if(self.validate_expresion(expresion[1])): 
            return expresion[1]
        else: 
            return None


    def validate_expresion(self, expresion):
        try:
            re.compile(expresion)
            if any(char in expresion for char in ['*', '+', '?', '[', ']', '(', ')', '{', '}', '^', '$', '.', '|', '\\']):
                return True
            else:
                return False 
        except re.error:
            return False  


    def addDecoder(self, type = "decoders", fileName="", xml=""): 
        response = self.api.addDecoderRule(type, fileName=fileName, Content=xml)
        print(response)


    def updateDecoder(self, type = "decoders", fileName="", xml=""): 
        response = self.api.updateDecoderRule(type, fileName=fileName, Content=xml)
        print(response)

    def testDecoderLog(self, log, file): 
        return self.api.log_test(log=log, file=file)


class Rule: 
    def __init__(self): 
        self.api = API("192.168.1.193")

    def create_rule(self): 
        pass

    def addRule(self, type = "rules", fileName="", xml=""): 
        response = self.api.addDecoderRule(type, fileName=fileName, Content=xml)
        print(response)

    def updateRule(self, type = "rules", fileName="", xml=""): 
        response = self.api.updateDecoderRule(type, fileName=fileName, Content=xml)
        print(response)

