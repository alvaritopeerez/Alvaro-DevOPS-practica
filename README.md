## Docker

### Cómo construir la imagen

Para construir la imagen Docker:

```bash
docker build -t alvaroperez-devops:latest .
```

Para ejecutar el contenedor:

```bash
docker run --rm alvarito-devops:latest
```

Ver imágenes disponibles
```bash
docker images
```

Eliminar la imagen
```bash
docker rmi alvarito-devops:latest
```

Salida esperada
Al ejecutar el contenedor, deberías ver la salida de las pruebas de TiendaService:

```text
=== Prueba TiendaService ===
Tienda creada correctamente
Producto: Laptop - $999.99
Producto: Mouse - $25.50
Total de productos en tienda: 2
...
```