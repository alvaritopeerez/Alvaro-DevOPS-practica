import uuid
from typing import Any
import re

class Usuario:
    """Clase base para todos los usuarios del sistema."""

    def __init__(self, nombre: str, correo: str):
        """
        Inicializa un usuario.

        Args:
            nombre: Nombre completo del usuario.
            correo: Dirección de correo válida.
        """

        if not nombre.strip():
            raise ValueError("Error: el nombre no puede estar vacío.")
        email_pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_pattern, correo):
         raise ValueError("Error: correo inválido.")
    
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.correo = correo

    
    def is_admin(self) -> bool:
        """Indica si el usuario es administrador."""
        return False


    def __str__(self):
        return f"Usuario          (id= {self.id:<5} ,  nombre= {self.nombre:<15},  correo= {self.correo:<20})"


class Cliente(Usuario):
    def __init__(self, nombre: str, correo: str, direccion: str):
        super().__init__(nombre, correo)
        self.direccion = direccion

    def __str__(self):
        return f"Cliente          (id= {self.id:<5} ,  nombre= {self.nombre:<15},  correo= {self.correo:<20},  dirección= {self.direccion:<10})"


class Administrador(Usuario):
    def __init__(self, nombre: str, correo: str):
        super().__init__(nombre, correo)

    def is_admin(self):
        return True

    def __str__(self):
        return f"Administrador    (id= {self.id:<5} ,  nombre= {self.nombre:<15},  correo= {self.correo:<10})"
