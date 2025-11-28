from pydantic import BaseModel
from typing import List, Optional

# ═══════════════════════════════════════════════════════════════
# ESQUEMAS DE USUARIO
# ═══════════════════════════════════════════════════════════════

class UsuarioCreate(BaseModel):
    """Esquema para crear un usuario"""
    nombre: str
    email: str
    tipo: str  # "cliente" o "administrador"
    direccion_postal: str

class UsuarioRead(BaseModel):
    """Esquema para devolver un usuario"""
    id: int
    nombre: str
    email: str
    es_admin: bool

# ═══════════════════════════════════════════════════════════════
# ESQUEMAS DE PRODUCTO
# ═══════════════════════════════════════════════════════════════

class ProductoCreate(BaseModel):
    """Esquema para crear un producto"""
    tipo: str  # "generico", "electronico" o "ropa"
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None  # Para electrónicos
    talla: Optional[str] = None  # Para ropa
    color: Optional[str] = None  # Para ropa

class ProductoRead(BaseModel):
    """Esquema para devolver un producto"""
    id: int
    tipo: str
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None

# ═══════════════════════════════════════════════════════════════
# ESQUEMAS DE PEDIDO
# ═══════════════════════════════════════════════════════════════

class PedidoItemCreate(BaseModel):
    """Esquema para cada producto en un pedido"""
    producto_id: int
    cantidad: int

class PedidoCreate(BaseModel):
    """Esquema para crear un pedido"""
    cliente_id: int
    items: List[PedidoItemCreate]

class PedidoItemRead(BaseModel):
    """Esquema para devolver cada línea de un pedido"""
    producto_id: int
    nombre_producto: str
    cantidad: int
    precio_unitario: float
    subtotal: float

class PedidoRead(BaseModel):
    """Esquema para devolver un pedido completo"""
    id: int
    fecha: str
    cliente_id: int
    cliente_nombre: str
    items: List[PedidoItemRead]
    total: float