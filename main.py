"""
Archivo principal de la aplicación de Boletería
"""
import tkinter as tk
from tkinter import messagebox
import PIL.Image
import PIL.ImageTk

from config import *
from database import DatabaseManager
from email_service import EmailService
from ventanas import VentanaManager
from ui_components import crear_texto_clickeable


class AplicacionBoleteria:
    def __init__(self):
        # Inicializar servicios
        self.db = DatabaseManager()
        self.email_service = EmailService()
        
        # Crear ventana principal
        self.ventana_principal = tk.Tk()
        self.ventana_principal.iconbitmap(ICONO_PRINCIPAL)
        self.ventana_principal.geometry(GEOMETRIA_PRINCIPAL)
        self.ventana_principal.resizable(False, False)
        self.ventana_principal.title("BoleteriaOficial")
        self.ventana_principal.config(bg=COLOR_BG_PRINCIPAL)
        
        # Gestor de ventanas
        self.ventana_manager = VentanaManager(
            self.ventana_principal,
            self.db,
            self.email_service
        )
        
        # Cargar y configurar UI
        self._cargar_fondo()
        self._crear_interfaz_principal()
    
    def _cargar_fondo(self):
        """Carga la imagen de fondo"""
        try:
            fondo_pil = PIL.Image.open(RUTA_IMAGEN_FONDO)
            self.fondo_tk = PIL.ImageTk.PhotoImage(fondo_pil)
        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                f"No se encontró 'fondo_principal.jpg' en la ruta: {RUTA_IMAGEN_FONDO}"
            )
            self.fondo_tk = None
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo convertir la imagen: {e}"
            )
            self.fondo_tk = None
    
    def _crear_interfaz_principal(self):
        """Crea la interfaz de la pantalla principal"""
        # Canvas para el fondo
        self.canvas = tk.Canvas(self.ventana_principal, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Colocar imagen de fondo
        if self.fondo_tk:
            self.canvas.create_image(0, 0, image=self.fondo_tk, anchor="nw")
            self.canvas.image = self.fondo_tk
        
        # Título de bienvenida
        self.canvas.create_text(
            535, 280,
            text="¡Bienvenido!",
            fill=COLOR_FG_TEXTO,
            font=FUENTE_TITULO,
            justify="center"
        )
        
        # Botones principales
        crear_texto_clickeable(
            self.canvas,
            535, 345,
            "Registrarse",
            self.ventana_manager.mostrar_registro,
            FUENTE_BOTON
        )
        
        crear_texto_clickeable(
            self.canvas,
            535, 437,
            "Iniciar sesión",
            self.ventana_manager.mostrar_login,
            FUENTE_BOTON
        )
        
        # Botones secundarios
        crear_texto_clickeable(
            self.canvas,
            450, 543,
            "Términos",
            self.ventana_manager.mostrar_terminos,
            ("Arial", 13, "bold")
        )
        
        crear_texto_clickeable(
            self.canvas,
            630, 543,
            "Reseñas",
            self.ventana_manager.mostrar_resenas,
            ("Arial", 13, "bold")
        )
    
    def ejecutar(self):
        """Inicia el loop principal de la aplicación"""
        self.ventana_principal.mainloop()


if __name__ == "__main__":
    app = AplicacionBoleteria()
    app.ejecutar()