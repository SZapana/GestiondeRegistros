# GestiondeRegistros 
Sistema de Registro Académico - Documentación

📝 Descripción
Aplicación Windows para gestión de registros académicos de estudiantes, desarrollada en C++ con WinAPI. Permite:

- Agregar nuevos estudiantes

-  Buscar/modificar/eliminar registros

- Guardar y cargar datos desde archivos CSV

- Visualización ordenada de todos los registros

🛠️ Tecnologías utilizadas
- Lenguaje: C++

- API: Windows API (Win32)

- Estructura de datos: Lista enlazada

- Persistencia: Archivos CSV y TXT

📦 Instalación
1. Clonar el repositorio o descargar los archivos fuente

2. Compilar con un compilador compatible con WinAPI (Visual Studio, MinGW, etc.)

3. Ejecutar el archivo compilado

🖥️ Interfaz de usuario
La aplicación cuenta con una interfaz intuitiva con:

Campos de entrada:
- Nombre completo

- Correo electrónico

- Carrera

- Año de ingreso

- Campo para búsqueda/eliminación (ID)

- Campo específico para modificación (ID)

Botones:
✅ Agregar - Añade nuevo estudiante

🔍 Mostrar Todos - Lista todos los registros

🔎 Buscar - Busca por ID o nombre

✏️ Modificar - Actualiza datos de un ID específico

❌ Eliminar - Borra un registro por ID

💾 Guardar - Guarda todos los datos en archivo

📂 Cargar - Recupera datos del archivo

![Estructura de datos](https://github.com/user-attachments/assets/7f067e3d-62fa-4985-8d1f-1466956b54f4)

🚀 Funcionalidades
1. ID automático: Generación secuencial automática de IDs

2. Validación de datos: Verifica que todos los campos estén completos

3. Búsqueda flexible: Por ID exacto o coincidencia parcial de nombre

4. Persistencia: Guardado automático en archivos CSV

5. Carga inicial: Recupera datos al iniciar la aplicación
