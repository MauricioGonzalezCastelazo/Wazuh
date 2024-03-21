from API import API
from openai import OpenAI
import os
from dotenv import load_dotenv
import re

load_dotenv("config.env")
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("La clave API de OPENAI no está definida en las variables de entorno.")

client = OpenAI(api_key=api_key)

class Decoder: 
    def __init__(self): 
        self.api = API("192.168.0.105")

    def read_log(self, txt): 
        pass

    def generate_decoder(self, name): 
        type = ["pcre2", "osregex","osmatch"]

        prompt = """
         Make a regular expression that extracts the capitalized words in the following sentence: "Hola como Estas Amigo", give the answer in this format: regex:expresion
        """
        regular_expresion = self.generate_regular_expresion(prompt)
        if(regular_expresion): 
            print(f"Se ha generado la expresion regular: {regular_expresion}")
            xml = f"""
            <decoder name="{name}">
                <prematch>variable</prematch>
            </decoder>

            <decoder name="mi-decoder">
                <parent>{name}</parent>
                    <regex type="{type[0]}">pepe=({regular_expresion})</regex>
                <order>pepe</order>
            </decoder>
                """
            print(xml)
            self.updateDecoder(fileName="Prueba27.xml", xml=xml) 

        else: 
            print("No se pudo generar la expresion regular")

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

class Rule: 
    def __init__(self): 
        self.api = API("192.168.0.105")

    def create_rule(self): 
        pass

    def addRule(self, type = "rules", fileName="", xml=""): 
        response = self.api.addDecoderRule(type, fileName=fileName, Content=xml)
        print(response)

    def updateRule(self, type = "rules", fileName="", xml=""): 
        response = self.api.updateDecoderRule(type, fileName=fileName, Content=xml)
        print(response)

decoder = Decoder()

decoder.generate_decoder("My_decoder_2")
