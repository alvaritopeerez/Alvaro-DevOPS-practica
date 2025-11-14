import uuid
from typing import Optional

class Producto:
    """Clase base para todos los productos de la tienda."""

    def __init__(self, nombre: str, precio: float, stock: int) -> None:
        
        """
        Inicializa un producto.
        
        Args:
            nombre: Nombre del producto
            precio: Precio unitario (debe ser >= 0)
            stock: Cantidad disponible (debe ser >= 0)
        """

        if not nombre.strip():
            raise ValueError("Error: el nombre no puede estar vacío.")
        if precio < 0:
            raise ValueError("Error: el precio es negativo.")
        if stock < 0:
            raise ValueError("Error: el stock es negativo.")
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
    
    def hay_stock(self, cantidad: int) -> bool:
        """Verifica si hay suficiente stock para la cantidad solicitada."""
        return cantidad > 0 and self.stock >= cantidad

    def actualizar_stock(self, cantidad: int) -> None:
        nuevo_stock = self.stock + cantidad
        if nuevo_stock < 0:
            raise ValueError("No hay suficiente stock.")
        self.stock = nuevo_stock

    def __str__(self) -> str:
        return f"Producto  (id= {self.id:<5} ,  nombre= {self.nombre:<21}, precio= €{self.precio:<9}, stock= {self.stock:<7})"


class ProductoElectronico(Producto):
    def __init__(self, nombre: str, precio: float, stock: int, garantia_meses: int = 24):
        super().__init__(nombre, precio, stock)
        if garantia_meses <= 0:
            raise ValueError("La garantía no es válida.")
        self.garantia_meses = garantia_meses

    def __str__(self):
        return f"Producto Electrónico  (id= {self.id:<5} ,  nombre= {self.nombre:<21}, precio= €{self.precio:<9}, stock= {self.stock:<7}, garantia= {self.garantia_meses:<3}meses)"


class ProductoRopa(Producto):
    def __init__(self, nombre: str, precio: float, stock: int, talla: str, color: str):
        super().__init__(nombre, precio, stock)
        if not talla or not color:
            raise ValueError("Es obligatorio definir la talla y el color.")
        self.talla = talla
        self.color = color

    def __str__(self):
        return f"Producto de Ropa      (id= {self.id:<5} ,  nombre= {self.nombre:<21}, precio= €{self.precio:<9}, stock= {self.stock:<7}, talla= {self.talla:<11}, color= {self.color})"
