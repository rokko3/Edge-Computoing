import cv2 as ocv
import sys
import customtkinter as ctk
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class frame(ctk.CTk):
    def __init__(self):
        self.title("Open Cam")
        self.geometry("1400x850")
        self.grid_columnconfigure(0,weight=1)
        
# Configura la dirección IP y puerto de tu celular. Ejemplos comunes:
# - IP Webcam (Android): "http://192.168.X.X:8080/video"
# - DroidCam: "http://192.168.X.X:4747/video"
# Reemplaza la IP de abajo por la que muestra tu aplicación en el celular:
url_camara_ip = "http://10.63.226.242:3346/video/" 

capturavideo = ocv.VideoCapture(url_camara_ip)
if capturavideo.isOpened():
    print(f"Camara IP Inicializada correctamente: {url_camara_ip}")
else:
    print(f"No se pudo conectar a la cámara IP: {url_camara_ip}")
    print("Intentando con la cámara local por defecto (0)...")
    capturavideo = ocv.VideoCapture(0)
    if not capturavideo.isOpened():
        sys.exit("Camara no inicializada")

while True:
    retardo, frame = capturavideo.read()
    if retardo:
        ocv.imshow('Prueba camara local', frame)
    else:
        sys.exit("Conexion de la camara erronea")
        
    if (ocv.waitKey(1) & 0xFF == 13): # Presiona Enter (código 13) para salir
        break

capturavideo.release()
ocv.destroyAllWindows()