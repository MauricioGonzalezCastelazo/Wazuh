from tkinter import * 
import tkinter as tk
from tkinter import ttk
import os
from openai import OpenAI
from dotenv import load_dotenv
from decoder_rules import Decoder, Rule
from tkinter import filedialog
from form import Formulario
import threading

load_dotenv("config.env")
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("La clave API de OPENAI no está definida en las variables de entorno.")

client = OpenAI(api_key=api_key)

class App: 
    def __init__(self): 
        #Reglas y decoders
        self.decoder = Decoder()
        self.rule = Rule()

        #Lista de logs
        self.logs_list = []
        self.palabras_list = {}

        #Generar la ventana
        self.root = tk.Tk()
        self.root.title("App Wazuh")
        self.root.geometry("700x500")

        #SideBar display
        self.isDisplay = True
        self.main_content = tk.Frame(self.root, bg='white')
        self.main_content.pack(side="right", fill="both", expand=True)
        self.sidebar = tk.Frame(self.root, width=100, bg='gray')
        self.sidebar.pack(side="left", fill="y")

        #Views
        self.home = tk.Frame(self.main_content, bg='white')  
        self.home.pack(fill="both", expand=True)
        self.logs = tk.Frame(self.main_content, bg='white') 
        self.chat_gpt = tk.Frame(self.main_content, bg='white')
        self.virus_total = tk.Frame(self.main_content, bg='white')  
        self.current_view = self.home 

        #XML Y decoder
        self.xml = ""
        self.file= ""

    def logs_view(self): 
        if not hasattr(self, 'logs_label'):
            self.logs_label = tk.Label(self.logs, text="Ingresar logs", bg = "white")
            self.logs_label.pack(expand=True, side="top")
            self.newLabel = tk.Label(self.logs, text="", bg = "white")
            self.newLabel.pack(expand=True, fill="x", side="top")
            self.btn_subir_archivo = Button(self.logs, text="Subir archivo", command=self.upload_file)
            self.btn_subir_archivo.pack(expand=True, side = "left", fill="x")
            
            self.btn_crearDecoder=Button(self.logs, text="Crear decoder")
            self.btn_updateDecoder=Button(self.logs, text="Modificar decoder")
            self.btn_crearDecoder.pack_forget()
            self.btn_updateDecoder.pack_forget()
                
    def generate_app(self): 

        # Crear botones para la barra de navegación lateral
        btn_decoder = tk.Button(self.sidebar, text="Inicio", command=self.show_home)
        btn_decoder.pack(fill="x")

        btn_logs = tk.Button(self.sidebar, text="Leer logs", command=self.show_logs)
        btn_logs.pack(fill="x")

        btn_ia = tk.Button(self.sidebar, text="Chat gpt", command=self.show_chat_gpt)
        btn_ia.pack(fill="x")

        btn_virusTotal = tk.Button(self.sidebar, text="Virus total", command=self.show_virus)
        btn_virusTotal.pack(fill="x")

        btn_salir = tk.Button(self.sidebar, text="Salir", command=self.salir_app)
        btn_salir.pack(fill="x")

        # Crear un Frame para el contenido principal
        btn_sideBar = Button(self.main_content, text=">>", command=self.toggle_sidebar)
        btn_sideBar.place(x=0,y=0)

    def toggle_sidebar(self): 
        if self.isDisplay:  
            self.sidebar.pack_forget()  
            self.isDisplay = False  
        else: 
            self.sidebar.pack(side="left", fill="y")  
            self.isDisplay = True  

    def show_home(self):
        self.showLogs_list = False
        self.change_view(self.home)

    def show_logs(self):
        self.logs_view()
        self.change_view(self.logs)

    def show_chat_gpt(self):
        self.showLogs_list = False
        self.change_view(self.chat_gpt)

    def show_virus(self):
        self.showLogs_list = False
        self.change_view(self.virus_total)

    def upload_file(self): 
        self.logs_list=[]
        self.palabras_list={}
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        if file_path:
            with open(file_path, 'r') as file:
                for line in file:
                    self.logs_list.append(line.strip())
                    partes = line.strip().split()
                    if len(partes) > 5:  
                        usuario = partes[4]
                        clave_valor = [parte for parte in partes[5:] if '=' in parte]
                        if usuario in self.palabras_list:
                            self.palabras_list[usuario].extend(clave_valor)
                        else:
                            self.palabras_list[usuario] = clave_valor

            texto = '\n'.join(self.logs_list)
            self.newLabel.config(text=texto)
            self.btn_subir_archivo.pack_forget()
            self.btn_crearDecoder.config(command=lambda : self.view_form(False, self.palabras_list))
            self.btn_updateDecoder.config(command=lambda : self.view_form(True, self.palabras_list))
            self.btn_crearDecoder.pack(side = 'left', expand=True, fill='x')
            self.btn_updateDecoder.pack(side = 'left', expand=True, fill='x')

    def view_form(self, type, diccionary):
        # Instanciar Formulario con el diccionario proporcionado y el tipo
        formulario = Formulario(diccionario=diccionary, mostrar_combobox=type)
        formulario.root.wait_window()
        xml = formulario.get_xml()
        self.decoder.generate_decoder(diccionary, xml[0], xml[1])

    def test_log(self, file, txt): 
        self.decoder.testDecoderLog(file, txt)

    def make_new_rule(self): 
       pass

    def make_new_decoder(self, file, xml): 
        self.decoder.addDecoder(file=file, xml=xml)

    def update_decoder(self, file, xml): 
        self.decoder.updateDecoder(fileName=file, xml=xml)
    
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

    def change_view(self, new_view):
        self.current_view.pack_forget()  # Oculta la vista actual
        new_view.pack(fill="both", expand=True)  # Muestra la nueva vista
        self.current_view = new_view  # Actualiza la vista actual

    def salir_app(self): 
        self.root.destroy()

    def start(self): 
        self.generate_app()
        self.root.mainloop()



app = App()
app.start()