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
        self.api = API("192.168.0.105")
        self.lock = threading.Lock()
        self.resultados = {}  
        self.isFinish = False
        self.rule = Rule()

    def process_key(self, key, diccionario,file_name, xml): 
        for ex in diccionario[key]:
            left_side = ex
            word = left_side.split("=")
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
                        #Reg = re.escape(regular_expresion)
                        regular_expresion = regular_expresion.lstrip("=")
                        self.resultados[key].append(f"{word[0]}=({regular_expresion})")
                    print(f"Se ha generado la expresion regular {key}:{word[0]}: {regular_expresion}")

                else: 
                    print("No se pudo generar la expresion regular")

            except Exception as e:
                print(f"Hubo una excepcion: {e}")


    def process_key1(self, key, diccionario,file_name, xml):
        for ex in diccionario[key]:
            left_side = ex
            word = left_side.split("=") 
            try: 
                regular_expresion = "\s*\w+"
                print(regular_expresion)
                if(regular_expresion): 
                    with self.lock:  # Asegura el acceso exclusivo al diccionario
                        if key not in self.resultados:
                            self.resultados[key] = []
                        #Reg = re.escape(regular_expresion)
                        regular_expresion = regular_expresion.lstrip("=")
                        self.resultados[key].append(f"{word[0]}=({regular_expresion})")
                    print(f"Se ha generado la expresion regular {key}:{word[0]}: {regular_expresion}")

                else: 
                    print("No se pudo generar la expresion regular")

            except Exception as e:
                print(f"Hubo una excepcion: {e}")

    def updateXML(self, xml): 
        new_decoders=[]
        decoders = xml.split("\n\n")
        patron = r"<prematch>(.*?)</prematch>"
        patron1 = r'<regex type="pcre2">(.*?)</regex>'
        for i, decoder in enumerate(decoders): 
            new_decoder = decoder
            if(len(decoder) > 0): 
                key = re.findall(patron, decoder)
                if(len(key) > 0):
                    regex_matches = re.findall(patron1, decoder)
                    if(len(regex_matches)>0):
                        try: 
                            new_regex = f'<regex type="pcre2">{"".join(self.resultados[key[0]])}</regex>'
                            new_decoder = re.sub(r'<regex type="pcre2">(.*?)<\/regex>', new_regex, decoder)
                        except Exception as e:
                            print(f"Ocurrió un error: {e}") 

    def updateXML1(self, xml): 
        new_decoders=[]
        decoders = xml.split("\n\n")
        patron = r"<prematch>(.*?)</prematch>"
        patron1 = r'<regex type="pcre2">(.*?)</regex>'
        for i, decoder in enumerate(decoders): 
            if(len(decoder) > 0): 
                key = re.findall(patron, decoder)
                if(len(key) > 0):
                    line = decoder.split("\n")
                    for i, palabras in enumerate(line):
                        new_regex = palabras 
                        if '<regex type="pcre2">' in palabras: 
                            try: 
                                new_regex = f'<regex type="pcre2">{" ".join(self.resultados[key[0]])}</regex>'
                            except Exception as e: 
                                print(f"Ha ocurrido un error: {e}")
                        new_decoders.append(new_regex)
        return '\n'.join(new_decoders)
             
                


    def generate_decoder(self, diccionario, file_name, xml):
        threads = [] 
        for key in diccionario.keys(): 
            t = threading.Thread(target=self.process_key1, args=(key, diccionario, file_name, xml))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.isFinish = True

    def create_decoder(self, diccionary, file_name, xml, update): 
        self.generate_decoder(diccionary, file_name, xml)
        while(self.isFinish != True): 
            print("Aun no he acabado")
        print("Ya acabé")
        new_xml = self.updateXML1(xml)
        print(new_xml)
        if(update == False): 
            self.addDecoder(fileName=file_name+".xml", xml=new_xml)
           
        else: 
            self.updateDecoder(fileName=file_name, xml=new_xml)
        self.rule.create_rule(diccionary=diccionary, regexList=self.resultados, file_name=file_name, tipo=update)


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
        self.api = API("192.168.0.105")

    def create_rule(self, diccionary, regexList, file_name, tipo): 
        #key = prematch
        #contenido son las palabras 
        print("Este es el archivo de la regla: "+file_name)
        xml = ""
        contador = 0
        for key, valor in diccionary.items():
            contador = contador + 1
            xml += f"""
<group name="wazuh,">
<rule id="20000{contador}" level="5">
    <match>{key}</match>
    <description>Registro creado de manera exitosa</description>
</rule>
</group>
"""         
        if(tipo == True): 
            parts = file_name.split(".")
            file= parts[0] + "_rule.xml" 
            self.updateRule(fileName=file, xml=xml)
        else: 
            self.addRule(fileName=file_name+"_rule.xml", xml=xml)

    def addRule(self, type = "rules", fileName="", xml=""): 
        response = self.api.addDecoderRule(type, fileName=fileName, Content=xml)
        print(response)

    def updateRule(self, type = "rules", fileName="", xml=""): 
        response = self.api.updateDecoderRule(type, fileName=fileName, Content=xml)
        print(response)

