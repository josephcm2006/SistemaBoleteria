"""
Servicio de envío de correos electrónicos
"""
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
from config import MI_EMAIL, MI_CONTRASEÑA


class EmailService:
    def __init__(self):
        self.codigo_verificacion = None
        self.email_destinatario = None
    
    def generar_codigo(self):
        """Genera un código de verificación de 6 dígitos"""
        self.codigo_verificacion = str(random.randint(100000, 999999))
        return self.codigo_verificacion
    
    def enviar_codigo_verificacion(self, email_destino, callback_success, callback_error):
        """
        Envía el código de verificación al email especificado
        callback_success: función a ejecutar si el envío es exitoso
        callback_error: función a ejecutar si hay error
        """
        self.email_destinatario = email_destino
        
        def _enviar():
            try:
                mensaje = MIMEMultipart()
                mensaje["From"] = MI_EMAIL
                mensaje["To"] = email_destino
                mensaje["Subject"] = "Código de verificación"

                escrito = f"""
Código de verificación

Este es su código: {self.codigo_verificacion}
                
Por favor, no comparta este código con nadie.
                """
                mensaje.attach(MIMEText(escrito, "plain"))

                servidor = smtplib.SMTP("smtp.gmail.com", 587)
                servidor.starttls()
                servidor.login(MI_EMAIL, MI_CONTRASEÑA)
                servidor.send_message(mensaje)
                servidor.quit()
                
                if callback_success:
                    callback_success()
                    
            except Exception as e:
                print(f"Error enviando email: {e}")
                if callback_error:
                    callback_error()
        
        # Ejecutar en un hilo separado para no bloquear la UI
        threading.Thread(target=_enviar, daemon=True).start()
    
    def verificar_codigo(self, codigo_ingresado):
        """Verifica si el código ingresado es correcto"""
        return codigo_ingresado == self.codigo_verificacion
    
    def reset(self):
        """Reinicia el servicio de email"""
        self.codigo_verificacion = None
        self.email_destinatario = None