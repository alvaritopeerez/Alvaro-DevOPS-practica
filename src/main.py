from models.Producto import ProductoElectronico, ProductoRopa
from models.Usuario import Cliente, Administrador
from Services.Tienda_service import TiendaService


def imprimir_inventario(tienda):
    print("\n INVENTARIO ")
    for p in tienda.listar_productos():
        print(p)


def imprimir_pedidos_cliente(tienda, cliente_id):
    print("\n PEDIDOS DEL CLIENTE ")
    pedidos = tienda.listar_pedidos_usuario(cliente_id)
    if not pedidos:
        print("(Aún no se han realizado pedidos)")
    else:
        for p in pedidos:
            print(p)
            print("-------------------------------------------------------------")


def imprimir_usuarios(tienda):
    print("\n USUARIOS REGISTRADOS ")
    for usuario in tienda.listar_usuarios():
        print(usuario)


def main():
    tienda = TiendaService()

    # Usuarios
    c1 = tienda.registrar_usuario   ("cliente", "Alvaro Pérez", "alvaro@gmail.com", direccion="UIE, A Coruña")
    c2 = tienda.registrar_usuario   ("cliente", "Lara Otero", "lara@hotmail.com", direccion="Avenida USC, Santiago")
    c3 = tienda.registrar_usuario   ("cliente", "Pepinho", "pepinho@yahoo.com", direccion="Barrio Salamanca, Madrid")

    admin = tienda.registrar_usuario("administrador", "El_admin", "admin@tienda.com")

    imprimir_usuarios(tienda)

    # Productos
    p1 = tienda.añadir_producto(ProductoElectronico("PlayStation 5", 399.99, 35, 24))
    p2 = tienda.añadir_producto(ProductoElectronico("Ratón Logitech", 79.90, 45, 12))
    p3 = tienda.añadir_producto(ProductoRopa("Camiseta AMI", 94.95, 100, "S", "Blanca"))
    p4 = tienda.añadir_producto(ProductoRopa("Chaleco Scalpers", 59.90, 40, "M", "Gris"))
    p5 = tienda.añadir_producto(ProductoElectronico("Alfombrilla de ratón", 30.50, 35, 6))

    imprimir_inventario(tienda)

    # Pedidos
    pedido1 = tienda.realizar_pedido(c3.id, [(p1.id, 2), (p3.id, 3)])
    print("\n PEDIDO 1 ")
    print(pedido1)

    pedido2 = tienda.realizar_pedido(c1.id, [(p2.id, 1), (p4.id, 2), (p5.id, 1)])
    print("\n PEDIDO 2 ")
    print(pedido2)

    pedido3 = tienda.realizar_pedido(c2.id, [(p3.id, 1), (p4.id, 1), (p1.id, 1)])
    print("\n PEDIDO 3 ")
    print(pedido3)

    pedido4 = tienda.realizar_pedido(c1.id, [(p4.id, 1), (p3.id, 2), (p5.id, 1), (p2.id, 1)])
    print("\n PEDIDO 4 ")
    print(pedido4)

    # Inventario después de los pedidos
    imprimir_inventario(tienda)

    # Historial de un cliente
    imprimir_pedidos_cliente(tienda, c1.id)


if __name__ == "__main__":
    main()
