from pydantic import BaseModel, EmailStr
from typing import List, Optional

# ═══════════════════════════════════════════════════════════════
# ESQUEMAS DE USUARIO
# ═══════════════════════════════════════════════════════════════

class UsuarioCreate(BaseModel):
    """Esquema para crear un usuario"""
    nombre: str
    correo: EmailStr
    tipo: str  # "cliente" o "administrador"
    direccion: Optional[str] = None

class UsuarioRead(BaseModel):
    id: str
    nombre: str
    correo: EmailStr
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
    garantia_meses: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None

class ProductoRead(BaseModel):
    id: str
    tipo: str
    nombre: str
    precio: float
    stock: int
    garantia_meses: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None

# ═══════════════════════════════════════════════════════════════
# ESQUEMAS DE PEDIDO
# ═══════════════════════════════════════════════════════════════

class PedidoItemRead(BaseModel):
    producto_id: str
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float

class PedidoItemCreate(BaseModel):
    producto_id: str
    cantidad: int

class PedidoCreate(BaseModel):
    cliente_id: str
    items: List[PedidoItemCreate]

class PedidoRead(BaseModel):
    id: str
    fecha: str
    cliente_id: str
    cliente_nombre: str
    items: List[PedidoItemRead]
    total: float