import tkinter as tk
from tkinter import ttk  # Necesario para el Combobox
from API import API
from tkinter import messagebox


class Formulario:
    def __init__(self, diccionario, mostrar_combobox=True):
        self.api = API("192.168.0.105")
        decoder_filenames = self.api.get('decoders')
        self.nombres_archivos = [decoder['filename'] for decoder in decoder_filenames]
        self.root = tk.Tk()
        self.root.geometry("300x300")  # Ajusta el tamaño según necesites
        self.diccionario = diccionario
        self.campos = {}
        self.datos = {}
        self.xml = ""
        self.file_name=""

        # Determinar qué widget mostrar basado en mostrar_combobox
        if mostrar_combobox:
            # Crear y empaquetar Combobox con valores hardcodeados
            self.nombre_clase_var = tk.StringVar()
            self.nombre_clase_cb = ttk.Combobox(self.root, textvariable=self.nombre_clase_var, state="readonly")
            self.nombre_clase_cb['values'] = self.nombres_archivos
            self.nombre_clase_var.set(self.nombres_archivos[0])
            self.nombre_clase_cb.pack() 
            self.nombre_clase_cb.bind("<<ComboboxSelected>>", self.actualizar_var)
            if self.nombres_archivos:  # Asegúrate de que la lista no esté vacía
                self.nombre_clase_cb.set(self.nombres_archivos[0])  # Establece el primer valor como predeterminado
            label_nombre_clase = tk.Label(self.root, text="Nombre del archivo xml:")
            label_nombre_clase.pack(before=self.nombre_clase_cb)
        else:
            # Crear y empaquetar Entry si mostrar_combobox es False
            self.nombre_clase_entry = tk.Entry(self.root)
            self.nombre_clase_entry.pack()
            label_nombre_clase = tk.Label(self.root, text="Nombre del arhivo xml:")
            label_nombre_clase.pack(before=self.nombre_clase_entry)

        # Continuar con la creación del resto del formulario como antes
        for llave in diccionario.keys():
            label_llave = tk.Label(self.root, text=llave)
            label_llave.pack()
            label_ingreso = tk.Label(self.root, text="Ingresa nombre del decoder:")
            label_ingreso.pack()
            entry = tk.Entry(self.root)
            entry.pack()
            self.campos[llave] = entry

        btn_subir = tk.Button(self.root, text="Subir", command=self.subir)
        btn_subir.pack()

    def actualizar_var(self, event): 
        print(f"He sido seleccionado {self.nombre_clase_cb.get()}")
        self.nombre_clase_var.set(self.nombre_clase_cb.get())
        print(f"Mi valor es: {self.nombre_clase_var.get()}")

    def genrar_xml(self): 
        self.file_name = self.datos['nombre_clase']
        # Iniciar el XML como un string vacío
        # Por cada key en formulario, excepto 'nombre_clase', generar la parte correspondiente del XML
        for key in self.datos:
            if key != 'nombre_clase':
                # Para cada key, obtener el nombre para el <decoder> y el <parent>
                decoder_name = self.datos[key]

                # Iniciar el XML para esta key
                self.xml += f"""
<decoder name="{decoder_name}">
    <prematch>{key}</prematch>
</decoder>
<decoder name="mi-decoder-{key}">
    <parent>{decoder_name}</parent>
    <regex type="pcre2"></regex>"""

                if key in self.diccionario:
                    regex_parts = [exp.split('=')[0] for exp in self.diccionario[key]]

                self.xml += f"""
    <order>{', '.join(regex_parts)}</order>
</decoder>\n\n"""

    def subir(self):
        campos_llenos = True
        if hasattr(self, 'nombre_clase_cb'):  
            nombre_clase = self.nombre_clase_var.get()
            print(nombre_clase)
        else:  
            nombre_clase = self.nombre_clase_entry.get().strip()


        if nombre_clase:
            self.datos["nombre_clase"] = nombre_clase
        else:
            campos_llenos = False
            
       
        for llave, entry in self.campos.items():
            valor = entry.get().strip()  
            if valor:  # Si el campo no está vacío
                self.datos[llave] = valor
            else:
                campos_llenos = False
                break  # Salir del bucle si se encuentra un campo vacío
        
        # Verificar si todos los campos están llenos
        if campos_llenos:
            print(self.datos)  # O realiza la acción deseada con los datos recolectados
            self.genrar_xml()
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    def get_xml(self): 
        return [self.file_name, self.xml]

    def start(self):
        self.root.mainloop()

# Ejemplo de uso
diccionario_ejemplo = {
    "nombre del decoder": "",
    "otra llave": ""
}

# Cambia True por False para ver el comportamiento con un Entry en lugar de un Combobox
#formulario = Formulario(diccionario_ejemplo, mostrar_combobox=True)
#formulario.start()
