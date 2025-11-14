# Usar imagen base oficial de Python
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY src/ ./src/

# Cambiar permisos para que el usuario pueda ejecutar
RUN chmod -R 755 /app

# Definir el comando de inicio
CMD ["python", "src/main.py"]