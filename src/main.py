from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from .Services.tienda_service import TiendaService
from .models.usuario import Usuario
from .models.producto import Producto, ProductoElectronico, ProductoRopa
from .models.pedido import Pedido

app = FastAPI(title="Tienda Online API (versión mínima)")

tienda_service = TiendaService()

# ---------------------- SCHEMAS ---------------------- #

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    tipo: str
    direccion_postal: Optional[str] = None

class UsuarioRead(BaseModel):
    id: UUID
    nombre: str
    email: EmailStr
    es_admin: bool

class ProductoCreate(BaseModel):
    tipo: str  # "generico", "electronico" o "ropa"
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None

class ProductoRead(BaseModel):
    id: UUID
    tipo: str
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None

class PedidoItemCreate(BaseModel):
    producto_id: UUID
    cantidad: int

class PedidoCreate(BaseModel):
    cliente_id: UUID
    items: List[PedidoItemCreate]

class PedidoItemRead(BaseModel):
    producto_id: UUID
    nombre_producto: str
    cantidad: int
    precio_unitario: float
    subtotal: float

class PedidoRead(BaseModel):
    id: UUID
    fecha: str
    cliente_id: UUID
    cliente_nombre: str
    items: List[PedidoItemRead]
    total: float

# ---------------------- ENDPOINTS ---------------------- #

# ------ USUARIOS ------ #

@app.post("/usuarios", response_model=UsuarioRead)
def crear_usuario(datos: UsuarioCreate) -> UsuarioRead:
    try:
        usuario = tienda_service.registrar_usuario(
            nombre=datos.nombre,
            email=str(datos.email),
            tipo=datos.tipo,
            direccion_postal=datos.direccion_postal,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return UsuarioRead(
        id=usuario.id,
        nombre=usuario.nombre,
        email=usuario.email,
        es_admin=usuario.is_admin(),
    )

@app.get("/usuarios", response_model=list[UsuarioRead])
def listar_usuarios() -> list[UsuarioRead]:
    usuarios = tienda_service.usuarios.values()
    return [
        UsuarioRead(
            id=u.id,
            nombre=u.nombre,
            email=u.email,
            es_admin=u.is_admin(),
        )
        for u in usuarios
    ]

@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: UUID) -> UsuarioRead:
    try:
        usuario = tienda_service.obtener_usuario(usuario_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return UsuarioRead(
        id=usuario.id,
        nombre=usuario.nombre,
        email=usuario.email,
        es_admin=usuario.is_admin(),
    )

# ------ PRODUCTOS ------ #

@app.post("/productos", response_model=ProductoRead, status_code=201)
def crear_producto(datos: ProductoCreate) -> ProductoRead:
    try:
        producto = tienda_service.agregar_producto(
            tipo=datos.tipo,
            nombre=datos.nombre,
            precio=datos.precio,
            stock=datos.stock,
            meses_garantia=datos.meses_garantia,
            talla=datos.talla,
            color=datos.color,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return ProductoRead(
        id=producto.id,
        tipo=datos.tipo,
        nombre=producto.nombre,
        precio=producto.precio,
        stock=producto.stock,
        meses_garantia=getattr(producto, 'meses_garantia', None),
        talla=getattr(producto, 'talla', None),
        color=getattr(producto, 'color', None),
    )

@app.get("/productos", response_model=list[ProductoRead])
def listar_productos() -> list[ProductoRead]:
    productos = tienda_service.productos.values()
    return [
        ProductoRead(
            id=p.id,
            tipo=p.tipo,
            nombre=p.nombre,
            precio=p.precio,
            stock=p.stock,
            meses_garantia=getattr(p, 'meses_garantia', None),
            talla=getattr(p, 'talla', None),
            color=getattr(p, 'color', None),
        )
        for p in productos
    ]

@app.get("/productos/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: UUID) -> ProductoRead:
    try:
        producto = tienda_service.obtener_producto(producto_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return ProductoRead(
        id=producto.id,
        tipo=producto.tipo,
        nombre=producto.nombre,
        precio=producto.precio,
        stock=producto.stock,
        meses_garantia=getattr(producto, 'meses_garantia', None),
        talla=getattr(producto, 'talla', None),
        color=getattr(producto, 'color', None),
    )

@app.delete("/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: UUID):
    try:
        tienda_service.eliminar_producto(producto_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

# ------ PEDIDOS ------ #

@app.post("/pedidos", response_model=PedidoRead, status_code=201)
def crear_pedido(datos: PedidoCreate) -> PedidoRead:
    try:
        pedido = tienda_service.crear_pedido(
            cliente_id=datos.cliente_id,
            items=[(item.producto_id, item.cantidad) for item in datos.items],
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return PedidoRead(
        id=pedido.id,
        fecha=str(pedido.fecha),
        cliente_id=pedido.cliente.id,
        cliente_nombre=pedido.cliente.nombre,
        items=[],
        total=pedido.calcular_total(),
    )

@app.get("/usuarios/{cliente_id}/pedidos", response_model=list[PedidoRead])
def listar_pedidos_cliente(cliente_id: UUID) -> list[PedidoRead]:
    try:
        pedidos = tienda_service.obtener_pedidos_cliente(cliente_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return [
        PedidoRead(
            id=p.id,
            fecha=str(p.fecha),
            cliente_id=p.cliente.id,
            cliente_nombre=p.cliente.nombre,
            items=[],
            total=p.calcular_total(),
        )
        for p in pedidos
    ]

# ------ HEALTH CHECK ------ #

@app.get("/")
def root():
    """Health check endpoint"""
    return {"mensaje": "Tienda Online API funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)