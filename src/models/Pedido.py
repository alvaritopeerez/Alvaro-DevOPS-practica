import uuid
from datetime import datetime
from typing import List, Optional

class ItemPedido:
    def __init__(self, producto_id: str, nombre: str, precio_unitario: float, cantidad: int):
        if cantidad <= 0:
            raise ValueError("Error: cantidad inválida")
        if precio_unitario < 0:
            raise ValueError("Error: precio inválido")
        self.producto_id = producto_id
        self.nombre = nombre
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
    
    def subtotal(self) -> float:
        return self.precio_unitario * self.cantidad


class Pedido:
    def __init__(self, cliente_id: str, items: List[ItemPedido], cliente_nombre: Optional[str] = None):
        if not items:
            raise ValueError("Error: el pedido ha de tener productos")
        self.id = str(uuid.uuid4())
        self.cliente_id = cliente_id
        self.cliente_nombre = cliente_nombre or f"Cliente( {cliente_id})"
        self.items = items
        self.fecha = datetime.now()

    def total(self) -> float:
        return round(sum(i.subtotal() for i in self.items), 2)

    def __str__(self) -> str:
        lineas = "\n".join([f"  - {i.nombre}  x{i.cantidad}    @ {i.precio_unitario}€ =    {i.subtotal()}€" for i in self.items])
        return f"id= {self.id},  fecha= {self.fecha},  cliente= {self.cliente_nombre})\n{lineas} \nTotal: {self.total()}€"