from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Importar schemas
from schemas import (
    UsuarioCreate, UsuarioRead,
    ProductoCreate, ProductoRead,
    PedidoCreate, PedidoRead
)

# Importar la lógica de negocio
from Services.Tienda_service import TiendaService

# Inicializar FastAPI
app = FastAPI(
    title="Tienda Online API",
    description="API REST para gestionar una tienda online",
    version="1.0.0"
)

# Permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia del servicio
tienda = TiendaService()

# ═══════════════════════════════════════════════════════════════
# ENDPOINTS DE USUARIOS
# ═══════════════════════════════════════════════════════════════

@app.post("/usuarios", response_model=UsuarioRead, status_code=201)
def crear_usuario(usuario: UsuarioCreate):
    """Crear un nuevo usuario"""
    try:
        nuevo_usuario = tienda.crear_usuario(
            nombre=usuario.nombre,
            email=usuario.email,
            tipo=usuario.tipo,
            direccion_postal=usuario.direccion_postal
        )
        return {
            "id": nuevo_usuario.id,
            "nombre": nuevo_usuario.nombre,
            "email": nuevo_usuario.email,
            "es_admin": nuevo_usuario.es_admin
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: int):
    """Obtener un usuario específico"""
    try:
        usuario = tienda.obtener_usuario(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "es_admin": usuario.es_admin
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios():
    """Listar todos los usuarios"""
    try:
        usuarios = tienda.listar_usuarios()
        return [
            {
                "id": u.id,
                "nombre": u.nombre,
                "email": u.email,
                "es_admin": u.es_admin
            }
            for u in usuarios
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ═══════════════════════════════════════════════════════════════
# ENDPOINTS DE PRODUCTOS
# ═══════════════════════════════════════════════════════════════

@app.post("/productos", response_model=ProductoRead, status_code=201)
def crear_producto(producto: ProductoCreate):
    """Crear un nuevo producto"""
    try:
        nuevo_producto = tienda.crear_producto(
            tipo=producto.tipo,
            nombre=producto.nombre,
            precio=producto.precio,
            stock=producto.stock,
            meses_garantia=producto.meses_garantia,
            talla=producto.talla,
            color=producto.color
        )
        return {
            "id": nuevo_producto.id,
            "tipo": nuevo_producto.tipo,
            "nombre": nuevo_producto.nombre,
            "precio": nuevo_producto.precio,
            "stock": nuevo_producto.stock,
            "meses_garantia": getattr(nuevo_producto, 'meses_garantia', None),
            "talla": getattr(nuevo_producto, 'talla', None),
            "color": getattr(nuevo_producto, 'color', None)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/productos", response_model=List[ProductoRead])
def listar_productos():
    """Listar todos los productos"""
    try:
        productos = tienda.listar_productos()
        return [
            {
                "id": p.id,
                "tipo": p.tipo,
                "nombre": p.nombre,
                "precio": p.precio,
                "stock": p.stock,
                "meses_garantia": getattr(p, 'meses_garantia', None),
                "talla": getattr(p, 'talla', None),
                "color": getattr(p, 'color', None)
            }
            for p in productos
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/productos/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: int):
    """Obtener un producto específico"""
    try:
        producto = tienda.obtener_producto(producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {
            "id": producto.id,
            "tipo": producto.tipo,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "stock": producto.stock,
            "meses_garantia": getattr(producto, 'meses_garantia', None),
            "talla": getattr(producto, 'talla', None),
            "color": getattr(producto, 'color', None)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int):
    """Eliminar un producto"""
    try:
        tienda.eliminar_producto(producto_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ═══════════════════════════════════════════════════════════════
# ENDPOINTS DE PEDIDOS
# ═══════════════════════════════════════════════════════════════

@app.post("/pedidos", response_model=PedidoRead, status_code=201)
def crear_pedido(pedido: PedidoCreate):
    """Crear un nuevo pedido"""
    try:
        nuevo_pedido = tienda.crear_pedido(
            cliente_id=pedido.cliente_id,
            items=[(item.producto_id, item.cantidad) for item in pedido.items]
        )
        return {
            "id": nuevo_pedido.id,
            "fecha": str(nuevo_pedido.fecha),
            "cliente_id": nuevo_pedido.cliente.id,
            "cliente_nombre": nuevo_pedido.cliente.nombre,
            "items": [],
            "total": nuevo_pedido.calcular_total()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/usuarios/{cliente_id}/pedidos", response_model=List[PedidoRead])
def listar_pedidos_cliente(cliente_id: int):
    """Listar todos los pedidos de un cliente"""
    try:
        pedidos = tienda.obtener_pedidos_cliente(cliente_id)
        return [
            {
                "id": p.id,
                "fecha": str(p.fecha),
                "cliente_id": p.cliente.id,
                "cliente_nombre": p.cliente.nombre,
                "items": [],
                "total": p.calcular_total()
            }
            for p in pedidos
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ═══════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════

@app.get("/")
def root():
    """Health check endpoint"""
    return {"mensaje": "Tienda Online API funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)