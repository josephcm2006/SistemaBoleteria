"""
Gestión de todas las ventanas de la aplicación
"""
import tkinter as tk
from tkinter import Toplevel, Frame, Button, Label, messagebox, StringVar
from ui_components import *
from config import *


class VentanaManager:
    def __init__(self, ventana_principal, db_manager, email_service):
        self.ventana_principal = ventana_principal
        self.db = db_manager
        self.email_service = email_service
        
        # Variables de entrada
        self.correo_registro = StringVar(value="")
        self.contra_registro = StringVar(value="")
        self.correo_login = StringVar(value="")
        self.contra_login = StringVar(value="")
        self.codigo_var = StringVar(value="")
        
        # Referencias a ventanas
        self.ventana_registro = None
        self.ventana_registro2 = None
        self.ventana_login = None
        self.ventana_principal_app = None
        self.ventana_terminos = None
        self.ventana_resenas = None
        
        # Widgets temporales
        self.entrada_correo_registro = None
        self.boton_enviar_email = None
        self.bloque_codigo = None
        self.entrada_codigo = None
    
    def reiniciar_variables(self):
        """Reinicia todas las variables de entrada"""
        self.correo_registro.set("")
        self.contra_registro.set("")
        self.correo_login.set("")
        self.contra_login.set("")
        self.codigo_var.set("")
    
    def volver_a_principal(self):
        """Vuelve a la ventana principal cerrando todas las demás"""
        ventanas = [
            self.ventana_registro,
            self.ventana_registro2,
            self.ventana_login,
            self.ventana_principal_app
        ]
        
        for ventana in ventanas:
            if ventana is not None:
                ventana.withdraw()
        
        self.ventana_principal.deiconify()
        self.reiniciar_variables()
    
    def confirmar_volver(self):
        """Confirma antes de volver"""
        self.volver_a_principal()
    
    def mostrar_registro(self):
        """Muestra la ventana de registro paso 1"""
        if self.ventana_principal is not None:
            self.ventana_principal.withdraw()
        if self.ventana_registro2 is not None:
            self.ventana_registro2.withdraw()
        
        if self.ventana_registro is None:
            self._crear_ventana_registro()
        
        self.ventana_registro.deiconify()
    
    def _crear_ventana_registro(self):
        """Crea la ventana de registro paso 1"""
        self.ventana_registro = Toplevel()
        configurar_ventana_base(self.ventana_registro, "Registro")
        
        # Título
        crear_label_titulo(
            self.ventana_registro,
            "Ingrese su Correo:",
            font=("Arial", 18, "bold")
        ).place(relx=0.3, rely=0.2)
        
        # Campo de correo
        frame_correo, self.entrada_correo_registro = crear_frame_entrada(
            self.ventana_registro,
            self.correo_registro
        )
        frame_correo.place(relx=0.24, rely=0.30)
        
        # Botón enviar email
        self.boton_enviar_email = crear_boton_estandar(
            self.ventana_registro,
            "Enviar email",
            self._enviar_email
        )
        self.boton_enviar_email.place(relx=0.415, rely=0.4)
        
        # Botón volver
        crear_boton_estandar(
            self.ventana_registro,
            "Volver",
            self.confirmar_volver
        ).place(relx=0.45, rely=0.50)
        
        # Bloque de código (oculto inicialmente)
        self._crear_bloque_codigo()
    
    def _crear_bloque_codigo(self):
        """Crea el bloque para ingresar el código de verificación"""
        self.bloque_codigo = Frame(self.ventana_registro, bg=COLOR_BG_PRINCIPAL)
        
        Label(
            self.bloque_codigo,
            text="Ingrese su código:",
            bg=COLOR_BG_PRINCIPAL,
            fg=COLOR_FG_TEXTO,
            font=("Arial", 7, "bold")
        ).pack(side="left", padx=5)
        
        self.entrada_codigo = tk.Entry(
            self.bloque_codigo,
            textvariable=self.codigo_var,
            fg=COLOR_FG_TEXTO,
            bg=COLOR_BG_SECUNDARIO,
            justify="center",
            font=("Arial", 7, "bold")
        )
        self.entrada_codigo.pack(side="left", padx=5)
        
        Button(
            self.bloque_codigo,
            text="Verificar",
            command=self._verificar_codigo,
            fg=COLOR_FG_TEXTO,
            bg=COLOR_BG_SECUNDARIO,
            bd=5,
            relief="raised"
        ).pack(side="left", padx=5)
    
    def _enviar_email(self):
        """Maneja el envío del email de verificación"""
        email = self.entrada_correo_registro.get()
        
        if not email or "@" not in email:
            messagebox.showerror("ERROR", "Debe ingresar un email válido")
            self.correo_registro.set("")
            return
        
        self.email_service.generar_codigo()
        self.boton_enviar_email.config(state="disabled")
        
        def on_success():
            self.ventana_registro.after(0, self._actualizar_gui_email, True)
        
        def on_error():
            self.ventana_registro.after(0, self._actualizar_gui_email, False)
        
        self.email_service.enviar_codigo_verificacion(email, on_success, on_error)
    
    def _actualizar_gui_email(self, success):
        """Actualiza la GUI después del envío del email"""
        self.boton_enviar_email.config(state="normal")
        
        if success:
            self.bloque_codigo.place(relx=0.2, rely=0.7, width=300, height=150)
            messagebox.showinfo("Éxito", "Código enviado correctamente")
        else:
            messagebox.showerror("ERROR", "Error enviando el correo")
    
    def _verificar_codigo(self):
        """Verifica el código ingresado"""
        if self.email_service.verificar_codigo(self.entrada_codigo.get()):
            messagebox.showinfo("Éxito", "Código verificado correctamente")
            self.mostrar_registro2()
        else:
            messagebox.showerror("ERROR", "Código incorrecto")
            self.codigo_var.set("")
    
    def mostrar_registro2(self):
        """Muestra la ventana de registro paso 2"""
        if self.bloque_codigo:
            self.bloque_codigo.place_forget()
        
        if self.ventana_registro is not None:
            self.ventana_registro.withdraw()
        
        if self.ventana_registro2 is None:
            self._crear_ventana_registro2()
        
        self.ventana_registro2.deiconify()
    
    def _crear_ventana_registro2(self):
        """Crea la ventana de registro paso 2"""
        self.ventana_registro2 = Toplevel()
        configurar_ventana_base(self.ventana_registro2, "Completar Registro")
        
        # Título
        Label(
            self.ventana_registro2,
            text="Complete su registro",
            font=("Arial", 14, "bold"),
            bg=COLOR_BG_PRINCIPAL,
            fg=COLOR_FG_TEXTO
        ).pack(pady=20)
        
        # Label contraseña
        crear_label_titulo(
            self.ventana_registro2,
            "Ingrese una contraseña:"
        ).place(relx=0.3, rely=0.3)
        
        # Campo contraseña
        frame_contra, entrada_contra = crear_frame_entrada(
            self.ventana_registro2,
            self.contra_registro,
            show="*"
        )
        frame_contra.place(relx=0.24, rely=0.4)
        
        # Botón terminar registro
        crear_boton_estandar(
            self.ventana_registro2,
            "Terminar registro",
            self._guardar_registro
        ).place(relx=0.4, rely=0.6)
        
        # Botón volver
        crear_boton_estandar(
            self.ventana_registro2,
            "Volver",
            self.confirmar_volver
        ).place(relx=0.45, rely=0.7)
    
    def _guardar_registro(self):
        """Guarda el registro del usuario"""
        correo = self.entrada_correo_registro.get()
        contra = self.contra_registro.get()
        
        exito, mensaje = self.db.registrar_usuario(correo, contra)
        
        if exito:
            self.mostrar_login()
        else:
            messagebox.showerror("Error", mensaje)
    
    def mostrar_login(self):
        """Muestra la ventana de inicio de sesión"""
        ventanas_a_ocultar = [
            self.ventana_registro2,
            self.ventana_principal,
            self.ventana_registro
        ]
        
        for ventana in ventanas_a_ocultar:
            if ventana is not None:
                ventana.withdraw()
        
        if self.ventana_login is None:
            self._crear_ventana_login()
        
        self.ventana_login.deiconify()
    
    def _crear_ventana_login(self):
        """Crea la ventana de inicio de sesión"""
        self.ventana_login = Toplevel()
        configurar_ventana_base(self.ventana_login, "Inicio de sesión")
        
        # Título
        Label(
            self.ventana_login,
            text="Iniciar Sesión",
            fg=COLOR_FG_TEXTO,
            bg=COLOR_BG_PRINCIPAL,
            font=FUENTE_SUBTITULO
        ).pack(pady=30)
        
        # Campo correo
        crear_label_titulo(self.ventana_login, "Correo:").place(relx=0.45, rely=0.25)
        frame_correo, entrada_correo = crear_frame_entrada(
            self.ventana_login,
            self.correo_login
        )
        frame_correo.place(relx=0.24, rely=0.3)
        
        # Campo contraseña
        crear_label_titulo(self.ventana_login, "Contraseña:").place(relx=0.43, rely=0.37)
        frame_contra, entrada_contra = crear_frame_entrada(
            self.ventana_login,
            self.contra_login,
            show="*"
        )
        frame_contra.place(relx=0.24, rely=0.44)
        
        # Botones
        frame_botones = Frame(
            self.ventana_login,
            bg=COLOR_BG_PRINCIPAL,
            width=200,
            height=23
        )
        frame_botones.place(relx=0.44, rely=0.6)
        frame_botones.pack_propagate(False)
        
        Button(
            frame_botones,
            text="Iniciar sesion",
            command=self._hacer_login,
            bd=5,
            relief="raised",
            bg=COLOR_BG_SECUNDARIO,
            fg=COLOR_FG_TEXTO
        ).pack(side="left", padx=5)
        
        Button(
            frame_botones,
            text="Volver",
            command=self.confirmar_volver,
            bd=5,
            relief="raised",
            bg=COLOR_BG_SECUNDARIO,
            fg=COLOR_FG_TEXTO
        ).pack(side="right", padx=5)
    
    def _hacer_login(self):
        """Realiza el inicio de sesión"""
        correo = self.correo_login.get()
        contra = self.contra_login.get()
        
        exito, mensaje = self.db.verificar_credenciales(correo, contra)
        
        if exito:
            if self.ventana_login is not None:
                self.ventana_login.withdraw()
            
            if self.ventana_principal_app is None:
                self._crear_ventana_principal_app()
            
            self.ventana_principal_app.deiconify()
            messagebox.showinfo("Accedido", "Su inicio de sesión fue exitoso")
        else:
            messagebox.showerror("ERROR", mensaje)
            self.correo_login.set("")
            self.contra_login.set("")
    
    def _crear_ventana_principal_app(self):
        """Crea la ventana principal de la aplicación"""
        self.ventana_principal_app = Toplevel()
        configurar_ventana_base(self.ventana_principal_app, "Boleteria")
        
        Label(
            self.ventana_principal_app,
            text="BIENVENIDOS",
            fg=COLOR_FG_TEXTO,
            bg=COLOR_BG_SECUNDARIO,
            font=FUENTE_SUBTITULO
        ).pack(pady=20)
        
        crear_boton_estandar(
            self.ventana_principal_app,
            "Cerrar sesión",
            self.confirmar_volver
        ).pack(pady=30)
    
    def mostrar_terminos(self):
        """Muestra la ventana de términos"""
        if self.ventana_terminos is None:
            self.ventana_terminos = Toplevel()
            self.ventana_terminos.geometry(GEOMETRIA_TERMINOS)
            
            crear_boton_estandar(
                self.ventana_terminos,
                "Volver",
                self._volver_de_terminos
            ).pack()
        
        self.ventana_principal.withdraw()
        self.ventana_terminos.deiconify()
    
    def _volver_de_terminos(self):
        """Vuelve de la ventana de términos"""
        self.ventana_principal.deiconify()
        self.ventana_terminos.withdraw()
    
    def mostrar_resenas(self):
        """Muestra la ventana de reseñas"""
        if self.ventana_resenas is None:
            self.ventana_resenas = Toplevel()
            self.ventana_resenas.geometry(GEOMETRIA_SECUNDARIA)
            
            crear_boton_estandar(
                self.ventana_resenas,
                "Regresar",
                self._volver_de_resenas
            ).pack()
        
        self.ventana_principal.withdraw()
        self.ventana_resenas.deiconify()
    
    def _volver_de_resenas(self):
        """Vuelve de la ventana de reseñas"""
        self.ventana_principal.deiconify()
        self.ventana_resenas.withdraw()