from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from .Services.Tienda_service import TiendaService
from .models.Usuario import Usuario, Cliente, Administrador
from .models.Producto import Producto, ProductoElectronico, ProductoRopa
from .models.Pedido import Pedido, ItemPedido

app = FastAPI(title="Tienda Online API")

tienda_service = TiendaService()

# ---------------------- SCHEMAS ---------------------- #

class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    tipo: str  # "cliente" o "administrador"
    direccion: Optional[str] = None

class UsuarioRead(BaseModel):
    id: str
    nombre: str
    correo: EmailStr
    es_admin: bool

class ProductoCreate(BaseModel):
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

class ItemPedidoRead(BaseModel):
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
    items: List[ItemPedidoRead]
    total: float

# ---------------------- ENDPOINTS ---------------------- #

# ------ USUARIOS ------ #

@app.post("/usuarios", response_model=UsuarioRead, status_code=201)
def crear_usuario(datos: UsuarioCreate) -> UsuarioRead:
    try:
        usuario = tienda_service.registrar_usuario(
            tipo=datos.tipo,
            nombre=datos.nombre,
            correo=str(datos.correo),
            direccion=datos.direccion or "",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return UsuarioRead(
        id=usuario.id,
        nombre=usuario.nombre,
        correo=usuario.correo,
        es_admin=usuario.is_admin(),
    )

@app.get("/usuarios", response_model=list[UsuarioRead])
def listar_usuarios() -> list[UsuarioRead]:
    usuarios = tienda_service.listar_usuarios()
    return [
        UsuarioRead(
            id=u.id,
            nombre=u.nombre,
            correo=u.correo,
            es_admin=u.is_admin(),
        )
        for u in usuarios
    ]

@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: str) -> UsuarioRead:
    try:
        usuario = tienda_service.usuarios.get(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return UsuarioRead(
        id=usuario.id,
        nombre=usuario.nombre,
        correo=usuario.correo,
        es_admin=usuario.is_admin(),
    )

# ------ PRODUCTOS ------ #

@app.post("/productos", response_model=ProductoRead, status_code=201)
def crear_producto(datos: ProductoCreate) -> ProductoRead:
    try:
        if datos.tipo == "electronico":
            producto = ProductoElectronico(
                nombre=datos.nombre,
                precio=datos.precio,
                stock=datos.stock,
                garantia_meses=datos.garantia_meses or 24,
            )
        elif datos.tipo == "ropa":
            producto = ProductoRopa(
                nombre=datos.nombre,
                precio=datos.precio,
                stock=datos.stock,
                talla=datos.talla or "M",
                color=datos.color or "Negro",
            )
        else:
            producto = Producto(
                nombre=datos.nombre,
                precio=datos.precio,
                stock=datos.stock,
            )
        
        tienda_service.añadir_producto(producto)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return ProductoRead(
        id=producto.id,
        tipo=datos.tipo,
        nombre=producto.nombre,
        precio=producto.precio,
        stock=producto.stock,
        garantia_meses=getattr(producto, 'garantia_meses', None),
        talla=getattr(producto, 'talla', None),
        color=getattr(producto, 'color', None),
    )

@app.get("/productos", response_model=list[ProductoRead])
def listar_productos() -> list[ProductoRead]:
    productos = tienda_service.listar_productos()
    return [
        ProductoRead(
            id=p.id,
            tipo=p.__class__.__name__,
            nombre=p.nombre,
            precio=p.precio,
            stock=p.stock,
            garantia_meses=getattr(p, 'garantia_meses', None),
            talla=getattr(p, 'talla', None),
            color=getattr(p, 'color', None),
        )
        for p in productos
    ]

@app.get("/productos/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: str) -> ProductoRead:
    try:
        producto = tienda_service.obtener_producto(producto_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return ProductoRead(
        id=producto.id,
        tipo=producto.__class__.__name__,
        nombre=producto.nombre,
        precio=producto.precio,
        stock=producto.stock,
        garantia_meses=getattr(producto, 'garantia_meses', None),
        talla=getattr(producto, 'talla', None),
        color=getattr(producto, 'color', None),
    )

@app.delete("/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: str):
    try:
        tienda_service.quitar_producto(producto_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

# ------ PEDIDOS ------ #

@app.post("/pedidos", response_model=PedidoRead, status_code=201)
def crear_pedido(datos: PedidoCreate) -> PedidoRead:
    try:
        pedido = tienda_service.realizar_pedido(
            cliente_id=datos.cliente_id,
            items=[(item.producto_id, item.cantidad) for item in datos.items],
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    items_read = [
        ItemPedidoRead(
            producto_id=i.producto_id,
            nombre=i.nombre,
            cantidad=i.cantidad,
            precio_unitario=i.precio_unitario,
            subtotal=i.subtotal(),
        )
        for i in pedido.items
    ]

    return PedidoRead(
        id=pedido.id,
        fecha=str(pedido.fecha),
        cliente_id=pedido.cliente_id,
        cliente_nombre=pedido.cliente_nombre,
        items=items_read,
        total=pedido.total(),
    )

@app.get("/usuarios/{cliente_id}/pedidos", response_model=list[PedidoRead])
def listar_pedidos_cliente(cliente_id: str) -> list[PedidoRead]:
    try:
        if cliente_id not in tienda_service.usuarios:
            raise ValueError("Cliente no encontrado")
        pedidos = tienda_service.listar_pedidos_usuario(cliente_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return [
        PedidoRead(
            id=p.id,
            fecha=str(p.fecha),
            cliente_id=p.cliente_id,
            cliente_nombre=p.cliente_nombre,
            items=[
                ItemPedidoRead(
                    producto_id=i.producto_id,
                    nombre=i.nombre,
                    cantidad=i.cantidad,
                    precio_unitario=i.precio_unitario,
                    subtotal=i.subtotal(),
                )
                for i in p.items
            ],
            total=p.total(),
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
    uvicorn.run(app, host="0.0.0.0", port=8001)