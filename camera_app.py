import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

class CameraColumn(ttk.Frame):
    def __init__(self, parent, title="Cámara"):
        super().__init__(parent, padding="10")
        self.cap = None
        self.running = False
        self.title = title
        
        # Label/Título
        self.title_label = ttk.Label(self, text=title, font=("Helvetica", 12, "bold"))
        self.title_label.pack(pady=5)
        
        # Frame de controles
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Fuente:").pack(side=tk.LEFT, padx=5)
        
        self.source_var = tk.StringVar(value="0")
        self.source_combo = ttk.Combobox(control_frame, textvariable=self.source_var, values=["0", "1", "2", "IP", "ESP"], state="readonly", width=5)
        self.source_combo.pack(side=tk.LEFT, padx=5)
        self.source_combo.bind("<<ComboboxSelected>>", self.on_source_change)
        
        self.ip_entry = ttk.Entry(control_frame, width=25)
        self.ip_entry.insert(0, "http://192.168.1.100:8080/video")
        
        self.start_btn = ttk.Button(control_frame, text="Iniciar", command=self.start_camera)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="Detener", command=self.stop_camera, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame de video
        self.video_label = ttk.Label(self, relief="groove")
        self.video_label.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        self.on_source_change()
        
    def on_source_change(self, event=None):
        if self.source_var.get() in ("IP", "ESP"):
            self.ip_entry.pack(side=tk.LEFT, padx=5, before=self.start_btn)
        else:
            self.ip_entry.pack_forget()
            
    def start_camera(self):
        source = self.source_var.get()
        if source.isdigit():
            cam_source = int(source)
        else:
            cam_source = self.ip_entry.get()
            
        self.cap = cv2.VideoCapture(cam_source)
        
        # Opciones para reducir el buffer y lag
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        if not self.cap.isOpened():
            messagebox.showerror("Error", f"No se pudo abrir la cámara en {self.title}.")
            return
            
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.source_combo.config(state=tk.DISABLED)
        self.ip_entry.config(state=tk.DISABLED)
        
        self.update_frame()
        
    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.source_combo.config(state="readonly")
        self.ip_entry.config(state=tk.NORMAL)
        self.video_label.config(image='')
        
    def update_frame(self):
        if self.running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (450, 350))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
            
            self.after(15, self.update_frame)
        else:
            if self.cap:
                self.cap.release()
                self.cap = None

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de Tres Cámaras")
        self.root.geometry("1450x550")
        
        # Container frame for the columns
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.columns = []
        for i in range(3):
            col = CameraColumn(self.main_frame, title=f"Cámara {i+1}")
            col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.columns.append(col)
            
    def stop_all(self):
        for col in self.columns:
            col.stop_camera()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop_all(), root.destroy()))
    root.mainloop()
