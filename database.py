"""
Gestión de base de datos de usuarios
"""

class DatabaseManager:
    def __init__(self):
        self.correos = []
        self.contraseñas = []
    
    def registrar_usuario(self, correo, contraseña):
        """Registra un nuevo usuario"""
        if not contraseña:
            return False, "La contraseña no puede estar vacía"
        
        if correo in self.correos:
            return False, "El correo ya está registrado"
        
        self.correos.append(correo)
        self.contraseñas.append(contraseña)
        print(f"Usuario registrado - Correos: {self.correos}")
        return True, "Usuario registrado exitosamente"
    
    def verificar_credenciales(self, correo, contraseña):
        """Verifica las credenciales de inicio de sesión"""
        try:
            if correo in self.correos:
                indice = self.correos.index(correo)
                if self.contraseñas[indice] == contraseña:
                    return True, "Credenciales correctas"
            return False, "Credenciales incorrectas"
        except ValueError:
            return False, "Usuario no encontrado"
    
    def obtener_total_usuarios(self):
        """Retorna el total de usuarios registrados"""
        return len(self.correos)