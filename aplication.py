from tkinter import * 
import tkinter as tk
from tkinter import ttk
import os
from openai import OpenAI
from dotenv import load_dotenv
#from decoder_rules import Decoder, Rule
load_dotenv("config.env")
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("La clave API de OPENAI no está definida en las variables de entorno.")

client = OpenAI(api_key=api_key)

class App: 

    def __init__(self): 
        self.root = tk.Tk()
        self.root.title("App Wazuh")
        self.root.geometry("700x500")
        self.label = Label(self.root, text="Bienvenido a la aplicacion de Wazuh"
                           ,font=("Arial", 25))
        self.label.pack()
        self.entrada = tk.StringVar()
        tk.Entry(self.root, textvariable=self.entrada, width=70).place(x=150, y=140) 
        btn = Button(self.root, text="Subir archivo", command=self.ask_my_logs)
        btn.pack(side="bottom")

    def generate_app(self): 
        pass

    def upload_file(self): 
        pass

    def test_log(self): 
        pass

    def make_new_rule(self): 
        pass

    def make_new_decoder(self): 
        pass
    
    def integration_virus(self): 
        pass

    def ask_my_logs(self):  
        if(self.entrada.get()):
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Assistant"},
                {"role": "user", "content": self.entrada.get()}
            ],
            )
            expresion = completion.choices[0].message.content
            self.lbl = Label(self.root, text=expresion)
            self.lbl.pack(side="bottom") 
            
        else: 
            print("El texto está vacio")

    def start(self): 
        self.root.mainloop()



app = App()
app.start()