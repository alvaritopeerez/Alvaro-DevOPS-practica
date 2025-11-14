from typing import List, Tuple, Dict
from models.Producto import Producto
from models.Usuario import Usuario, Cliente, Administrador
from models.Pedido import Pedido, ItemPedido

class TiendaService:
    """Servicio que gestiona usuarios, productos y pedidos de la tienda."""

    def __init__(self) -> None:
        self.usuarios: Dict[str, Usuario] = {} # Almacena usuarios por su ID
        self.productos: Dict[str, Producto] = {} # Almacena productos por su ID
        self.pedidos: Dict[str, Pedido] = {} # Almacena pedidos por su ID
        self.correo_index: Dict[str, str] = {} # Índice para buscar usuarios por correo


    def registrar_usuario(self, tipo: str, nombre: str, correo: str, **kwargs) -> Usuario:
        """Registra un nuevo usuario y lo indexa por correo."""

        if tipo == "cliente":
            usuario = Cliente(nombre, correo, kwargs.get("direccion", ""))
        elif tipo == "administrador":
            usuario = Administrador(nombre, correo)
        else:
            raise ValueError("Tipo inválido. Debe ser 'cliente' o 'administrador'.")
        if correo in self.correo_index:
            raise ValueError("Este correo ya está en uso.")
        self.usuarios[usuario.id] = usuario
        self.correo_index[correo] = usuario.id
        return usuario

    def añadir_producto(self, producto: Producto) -> Producto:
        """Añade un nuevo producto al catálogo."""
        
        if producto.id in self.productos:
            raise ValueError("Este producto ya existe.")
        self.productos[producto.id] = producto
        return producto

    def quitar_producto(self, producto_id: str):
        if producto_id not in self.productos:
            raise KeyError("Error: no se ha encontrado el producto.")
        del self.productos[producto_id]

    def listar_productos(self) -> List[Producto]:
        """Devuelve la lista de todos los productos."""
        return list(self.productos.values())

    def obtener_producto(self, producto_id: str) -> Producto:
        if producto_id not in self.productos:  # No existe el producto
            raise KeyError("No se ha encontrado el producto.")
        return self.productos[producto_id] # Retorna la instancia del producto
    
    def _validar_y_actualizar_stock(self, producto_id: str, cantidad: int) -> None:
        """
        Verifica disponibilidad y descuenta stock.

        Raises:
            ValueError: Si no hay stock suficiente.
        """
        producto = self.obtener_producto(producto_id)
        if not producto.hay_stock(cantidad):
            raise ValueError(f"No hay stock suficiente de '{producto.nombre}'.")
        producto.actualizar_stock(-cantidad)

   
    def realizar_pedido(self, cliente_id: str, items: list[tuple[str,int]]) -> Pedido:
        """Crea un pedido para un cliente, actualiza stock y retorna la instancia Pedido."""
        if cliente_id not in self.usuarios:
            raise ValueError("El cliente no existe.")
        cliente = self.usuarios[cliente_id]
        if not isinstance(cliente, Cliente):
            raise ValueError("Solo los clientes pueden realizar pedidos.")
        if not items:
            raise ValueError("Error: el pedido está vacío y debe tener productos.")

        
        lineas: List[ItemPedido] = []
        for pid, cantidad in items:
            if cantidad <= 0:
                raise ValueError("Error: cantidad debe ser positiva.")
            producto = self.obtener_producto(pid)
            if not producto.hay_stock(cantidad):
                raise ValueError(f"No hay stock suficiente de {producto.nombre}")   # Validar stock
            lineas.append(ItemPedido(pid, producto.nombre, producto.precio, cantidad))    # Crear línea de pedido

       
        for pid, cantidad in items:
            self._validar_y_actualizar_stock(pid, cantidad)

     
        pedido = Pedido(cliente_id, lineas, cliente.nombre)
        self.pedidos[pedido.id] = pedido
        return pedido

    def listar_pedidos_usuario(self, cliente_id: str) -> List[Pedido]:
        """Devuelve los pedidos de un cliente ordenados por fecha."""

        return sorted(
            [p for p in self.pedidos.values() if p.cliente_id == cliente_id], key=lambda p: p.fecha)  # Ordenar por fecha

    def listar_usuarios(self) -> List[Usuario]:
        """Devuelve lista de todos los usuarios registrados."""
        return list(self.usuarios.values())