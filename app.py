import os
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox, filedialog
import configparser
from pathlib import Path

config_file = str(Path.home() / "settings.ini")

config = configparser.ConfigParser()
if not os.path.exists(config_file): 
    config["Settings"] = {
        "language": "es-ES",
        "output_file": str(Path.home() / "output.txt") 
    }
    try:
        with open(config_file, "w") as file:
            config.write(file)
    except PermissionError as e:
        messagebox.showerror("Error", f"Permiso denegado al crear {config_file}: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {e}")

config.read(config_file)

def convert_voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            messagebox.showinfo("Info", "Hable ahora...")
            audio = recognizer.listen(source, timeout=10)
            language = config["Settings"]["language"]
            text = recognizer.recognize_google(audio, language=language)
           
            # Guarda la conversión
            output_file = config["Settings"]["output_file"]
            with open(output_file, "a") as file:
                file.write(text + "\n")
               
            messagebox.showinfo("Resultado", f"Texto reconocido:\n{text}")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "No se pudo reconocer el audio.")
        except sr.RequestError:
            messagebox.showerror("Error", "Error en el servicio de reconocimiento.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def open_settings():
    settings_window = tk.Toplevel()
    settings_window.title("Configuración")
   
    tk.Label(settings_window, text="Idioma (Ej: es-ES):").pack()
    language_entry = tk.Entry(settings_window)
    language_entry.insert(0, config["Settings"]["language"])
    language_entry.pack()
   
    tk.Label(settings_window, text="Archivo de salida:").pack()
    output_entry = tk.Entry(settings_window)
    output_entry.insert(0, config["Settings"]["output_file"])
    output_entry.pack()
   
    def save_settings():
        config["Settings"]["language"] = language_entry.get()
        config["Settings"]["output_file"] = output_entry.get()
        try:
            with open(config_file, "w") as file:
                config.write(file)
            settings_window.destroy()
            messagebox.showinfo("Configuración", "Configuración guardada.")
        except PermissionError as e:
            messagebox.showerror("Error", f"Permiso denegado al guardar {config_file}: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
   
    tk.Button(settings_window, text="Guardar", command=save_settings).pack()


def main():
    root = tk.Tk()
    root.title("Conversor de Voz a Texto")
   
    tk.Button(root, text="Convertir Voz a Texto", command=convert_voice_to_text).pack(pady=10)
    tk.Button(root, text="Configuración", command=open_settings).pack(pady=10)
    tk.Button(root, text="Salir", command=root.quit).pack(pady=10)
   
    root.mainloop()

if __name__ == "__main__":
    main()