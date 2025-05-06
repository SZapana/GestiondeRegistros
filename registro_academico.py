"""
Sistema de Registro Académico
============================
Este programa permite gestionar registros de estudiantes y docentes en una institución educativa.
Utiliza principios de POO como herencia, polimorfismo y encapsulamiento.
Los datos se guardan en archivos CSV para persistencia.
"""

import os
import csv
from abc import ABC, abstractmethod  # Para crear clases abstractas


# CLASE BASE ABSTRACTA PARA PERSONAS
class Persona(ABC):
    """
    Clase abstracta que representa a una persona en el sistema.
    No se puede instanciar directamente - sirve como modelo para las clases hijas.
    """

    def __init__(self, id, nombre, correo):
        """
        Constructor de la clase Persona.

        Args:
            id (int): Identificador único de la persona
            nombre (str): Nombre completo de la persona
            correo (str): Correo electrónico de la persona
        """
        self.id = id  # Atributo de instancia para el ID
        self.nombre = nombre  # Atributo de instancia para el nombre
        self.correo = correo  # Atributo de instancia para el correo

    @abstractmethod
    def mostrar_info(self):
        """
        Método abstracto que debe ser implementado por las clases hijas.
        Devuelve la información de la persona formateada.
        """
        pass


# CLASE PARA ESTUDIANTES (HEREDA DE PERSONA)
class Estudiante(Persona):
    """
    Clase que representa a un estudiante en el sistema.
    Hereda atributos y métodos de la clase Persona.
    """

    def __init__(self, id, nombre, correo, carrera, anio):
        """
        Constructor de la clase Estudiante.

        Args:
            id (int): ID del estudiante
            nombre (str): Nombre del estudiante
            correo (str): Correo del estudiante
            carrera (str): Carrera que estudia
            anio (int): Año de ingreso
        """
        super().__init__(id, nombre, correo)  # Llama al constructor de la clase padre
        self.carrera = carrera  # Atributo específico de Estudiante
        self.anio = anio  # Atributo específico de Estudiante

    def mostrar_info(self):
        """
        Implementación concreta del método abstracto.
        Devuelve la información del estudiante formateada.

        Returns:
            str: Información del estudiante
        """
        return (f"ID: {self.id} | Estudiante: {self.nombre} | "
                f"Correo: {self.correo} | Carrera: {self.carrera} | "
                f"Año: {self.anio}")


# CLASE PARA DOCENTES (HEREDA DE PERSONA)
class Docente(Persona):
    """
    Clase que representa a un docente en el sistema.
    Hereda atributos y métodos de la clase Persona.
    """

    def __init__(self, id, nombre, correo, departamento, titulo):
        """
        Constructor de la clase Docente.

        Args:
            id (int): ID del docente
            nombre (str): Nombre del docente
            correo (str): Correo del docente
            departamento (str): Departamento al que pertenece
            titulo (str): Título académico
        """
        super().__init__(id, nombre, correo)  # Llama al constructor de la clase padre
        self.departamento = departamento  # Atributo específico de Docente
        self.titulo = titulo  # Atributo específico de Docente

    def mostrar_info(self):
        """
        Implementación concreta del método abstracto.
        Devuelve la información del docente formateada.

        Returns:
            str: Información del docente
        """
        return (f"ID: {self.id} | Docente: {self.nombre} | "
                f"Correo: {self.correo} | Departamento: {self.departamento} | "
                f"Título: {self.titulo}")


# CLASE PRINCIPAL DEL SISTEMA
class RegistroAcademico:
    """
    Clase principal que gestiona todas las operaciones del sistema.
    Contiene métodos para agregar, buscar, modificar y eliminar registros,
    así como para guardar y cargar datos desde archivos.
    """

    def __init__(self):
        """
        Inicializa el sistema con una lista vacía de registros
        y carga los datos existentes al iniciar.
        """
        self.registros = []  # Lista para almacenar todos los registros
        self.ultimo_id = 0  # Contador para IDs autoincrementales
        self.cargar_datos()  # Carga los datos existentes al iniciar

    def generar_id(self):
        """
        Genera un nuevo ID autoincremental para los registros.

        Returns:
            int: Nuevo ID generado
        """
        self.ultimo_id += 1  # Incrementa el contador de IDs
        return self.ultimo_id  # Devuelve el nuevo ID

    def agregar_estudiante(self, nombre, correo, carrera, anio):
        """
        Agrega un nuevo estudiante al sistema.

        Args:
            nombre (str): Nombre del estudiante
            correo (str): Correo del estudiante
            carrera (str): Carrera del estudiante
            anio (str/int): Año de ingreso

        Returns:
            bool: True si se agregó correctamente, False si hubo error
        """
        try:
            # Crea una nueva instancia de Estudiante
            estudiante = Estudiante(
                self.generar_id(), nombre, correo, carrera, int(anio)
            )
            self.registros.append(estudiante)  # Agrega a la lista de registros
            print("\n✅ Estudiante agregado exitosamente!")
            return True
        except ValueError:
            print("\n❌ Error: El año debe ser un número entero")
            return False

    def agregar_docente(self, nombre, correo, departamento, titulo):
        """
        Agrega un nuevo docente al sistema.

        Args:
            nombre (str): Nombre del docente
            correo (str): Correo del docente
            departamento (str): Departamento del docente
            titulo (str): Título del docente

        Returns:
            bool: True si se agregó correctamente
        """
        # Crea una nueva instancia de Docente
        docente = Docente(
            self.generar_id(), nombre, correo, departamento, titulo
        )
        self.registros.append(docente)  # Agrega a la lista de registros
        print("\n✅ Docente agregado exitosamente!")
        return True

    def mostrar_todos(self):
        """
        Muestra todos los registros almacenados en el sistema.
        """
        if not self.registros:  # Verifica si la lista está vacía
            print("\nℹ️ No hay registros en el sistema.")
            return

        print("\n=== LISTA DE REGISTROS ===")
        for registro in self.registros:  # Recorre todos los registros
            print(registro.mostrar_info())  # Muestra la información de cada uno

    def buscar_por_id(self, id):
        """
        Busca un registro por su ID.

        Args:
            id (str): ID a buscar (se convierte a int)

        Returns:
            Persona/None: El registro encontrado o None si no existe
        """
        try:
            id_buscar = int(id)  # Intenta convertir el ID a entero
        except ValueError:
            print("\n❌ Error: El ID debe ser un número")
            return None

        # Busca el registro con el ID especificado
        for registro in self.registros:
            if registro.id == id_buscar:
                print("\n🔍 Registro encontrado:")
                print(registro.mostrar_info())
                return registro  # Devuelve el registro encontrado

        print("\nℹ️ No se encontró ningún registro con ese ID.")
        return None  # Si no encontró nada

    def buscar_por_nombre(self, nombre):
        """
        Busca registros que coincidan con un nombre (búsqueda parcial).

        Args:
            nombre (str): Nombre o parte del nombre a buscar
        """
        if not nombre.strip():  # Verifica si el nombre está vacío
            print("\n❌ Error: Debe ingresar un nombre para buscar")
            return

        # Lista de registros cuyo nombre contiene el texto buscado (case insensitive)
        encontrados = [
            r for r in self.registros
            if nombre.lower() in r.nombre.lower()
        ]

        if not encontrados:  # Si no encontró coincidencias
            print("\nℹ️ No se encontraron registros con ese nombre.")
            return

        # Muestra los registros encontrados
        print(f"\n🔍 Se encontraron {len(encontrados)} registros:")
        for registro in encontrados:
            print(registro.mostrar_info())

    def modificar_registro(self, id):
        """
        Modifica los datos de un registro existente.

        Args:
            id (str): ID del registro a modificar

        Returns:
            bool: True si se modificó correctamente, False si hubo error
        """
        registro = self.buscar_por_id(id)  # Busca el registro por ID
        if not registro:
            return False  # Si no encontró el registro

        print("\n✏️ Ingrese los nuevos datos (deje en blanco para mantener el valor actual):")

        # Campos específicos para Estudiantes
        if isinstance(registro, Estudiante):
            carrera = input(f"Carrera [{registro.carrera}]: ") or registro.carrera
            anio = input(f"Año [{registro.anio}]: ")
            try:
                registro.anio = int(anio) if anio else registro.anio
            except ValueError:
                print("❌ El año debe ser un número. Se mantendrá el valor actual.")

        # Campos específicos para Docentes
        elif isinstance(registro, Docente):
            departamento = input(f"Departamento [{registro.departamento}]: ") or registro.departamento
            titulo = input(f"Título [{registro.titulo}]: ") or registro.titulo
            registro.departamento = departamento
            registro.titulo = titulo

        # Campos comunes a todos
        nombre = input(f"Nombre [{registro.nombre}]: ") or registro.nombre
        correo = input(f"Correo [{registro.correo}]: ") or registro.correo

        # Actualiza los valores
        registro.nombre = nombre
        registro.correo = correo

        print("\n✅ Registro modificado exitosamente!")
        return True

    def eliminar_registro(self, id):
        """
        Elimina un registro del sistema después de confirmación.

        Args:
            id (str): ID del registro a eliminar

        Returns:
            bool: True si se eliminó, False si se canceló
        """
        registro = self.buscar_por_id(id)  # Busca el registro por ID
        if not registro:
            return False  # Si no encontró el registro

        # Pide confirmación antes de eliminar
        confirmacion = input("\n¿Está seguro que desea eliminar este registro? (s/n): ").lower()
        if confirmacion == 's':
            # Filtra la lista para excluir el registro con el ID especificado
            self.registros = [r for r in self.registros if r.id != registro.id]
            print("\n✅ Registro eliminado exitosamente!")
            return True
        else:
            print("\n❌ Eliminación cancelada")
            return False

    def guardar_datos(self):
        """
        Guarda todos los registros en un archivo CSV.

        Returns:
            bool: True si se guardó correctamente, False si hubo error
        """
        try:
            # Abre el archivo en modo escritura (sobrescribe si existe)
            with open('registros.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')  # Crea un escritor CSV

                # Escribe cada registro en el archivo
                for registro in self.registros:
                    if isinstance(registro, Estudiante):
                        writer.writerow([
                            'estudiante',  # Tipo de registro
                            registro.id,
                            registro.nombre,
                            registro.correo,
                            registro.carrera,
                            registro.anio
                        ])
                    elif isinstance(registro, Docente):
                        writer.writerow([
                            'docente',  # Tipo de registro
                            registro.id,
                            registro.nombre,
                            registro.correo,
                            registro.departamento,
                            registro.titulo
                        ])

            # Guarda el último ID usado en un archivo separado
            with open('ultimo_id.txt', 'w', encoding='utf-8') as file:
                file.write(str(self.ultimo_id))

            print("\n💾 Datos guardados exitosamente!")
            return True
        except Exception as e:
            print(f"\n❌ Error al guardar datos: {str(e)}")
            return False

    def cargar_datos(self):
        """
        Carga los registros desde el archivo CSV al iniciar el sistema.

        Returns:
            bool: True si se cargó correctamente, False si hubo error
        """
        try:
            if not os.path.exists('registros.csv'):
                return True  # No hay archivo para cargar

            # Abre el archivo CSV en modo lectura
            with open('registros.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')  # Crea un lector CSV

                for row in reader:
                    if not row:  # Salta filas vacías
                        continue

                    # Procesa registros de estudiantes
                    if row[0] == 'estudiante':
                        try:
                            estudiante = Estudiante(
                                int(row[1]),  # ID
                                row[2],  # Nombre
                                row[3],  # Correo
                                row[4],  # Carrera
                                int(row[5]))  # Año
                            self.registros.append(estudiante)
                        except (IndexError, ValueError):
                            continue  # Salta filas corruptas
                    # Procesa registros de docentes
                    elif row[0] == 'docente':
                        try:
                            docente = Docente(
                                int(row[1]),  # ID
                                row[2],  # Nombre
                                row[3],  # Correo
                                row[4],  # Departamento
                                row[5])  # Título
                            self.registros.append(docente)
                        except (IndexError, ValueError):
                            continue  # Salta filas corruptas

                    # Actualiza el último ID usado
                    if int(row[1]) > self.ultimo_id:
                        self.ultimo_id = int(row[1])

            # Carga el último ID guardado (si existe)
            if os.path.exists('ultimo_id.txt'):
                with open('ultimo_id.txt', 'r', encoding='utf-8') as file:
                    try:
                        self.ultimo_id = max(self.ultimo_id, int(file.read()))
                    except ValueError:
                        pass  # Si el archivo está corrupto, mantiene el valor actual

            print("\n📂 Datos cargados exitosamente!")
            return True
        except Exception as e:
            print(f"\n❌ Error al cargar datos: {str(e)}")
            return False


# FUNCIONES PARA LA INTERFAZ DE USUARIO

def mostrar_menu():
    """
    Muestra el menú principal y obtiene la selección del usuario.

    Returns:
        str: Opción seleccionada por el usuario
    """
    print("\n" + "=" * 40)
    print("=== SISTEMA DE REGISTRO ACADÉMICO ===".center(40))
    print("=" * 40)
    print("\n1. Agregar estudiante")
    print("2. Agregar docente")
    print("3. Mostrar todos los registros")
    print("4. Buscar por ID")
    print("5. Buscar por nombre")
    print("6. Modificar registro")
    print("7. Eliminar registro")
    print("8. Guardar datos")
    print("9. Salir")
    return input("\nSeleccione una opción (1-9): ").strip()


def limpiar_pantalla():
    """
    Limpia la pantalla de la consola según el sistema operativo.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# FUNCIÓN PRINCIPAL
def main():
    """
    Función principal que maneja el flujo del programa.
    """
    sistema = RegistroAcademico()  # Crea una instancia del sistema

    while True:  # Bucle principal
        limpiar_pantalla()
        opcion = mostrar_menu()  # Muestra el menú y obtiene la opción

        # Opción 1: Agregar estudiante
        if opcion == '1':
            limpiar_pantalla()
            print("\n" + "=" * 40)
            print("AGREGAR ESTUDIANTE".center(40))
            print("=" * 40)
            nombre = input("\nNombre: ").strip()
            correo = input("Correo: ").strip()
            carrera = input("Carrera: ").strip()
            anio = input("Año: ").strip()

            if not all([nombre, correo, carrera, anio]):
                print("\n❌ Error: Todos los campos son obligatorios")
            else:
                sistema.agregar_estudiante(nombre, correo, carrera, anio)

        # Opción 2: Agregar docente
        elif opcion == '2':
            limpiar_pantalla()
            print("\n" + "=" * 40)
            print("AGREGAR DOCENTE".center(40))
            print("=" * 40)
            nombre = input("\nNombre: ").strip()
            correo = input("Correo: ").strip()
            departamento = input("Departamento: ").strip()
            titulo = input("Título: ").strip()

            if not all([nombre, correo, departamento, titulo]):
                print("\n❌ Error: Todos los campos son obligatorios")
            else:
                sistema.agregar_docente(nombre, correo, departamento, titulo)

        # Opción 3: Mostrar todos los registros
        elif opcion == '3':
            limpiar_pantalla()
            sistema.mostrar_todos()

        # Opción 4: Buscar por ID
        elif opcion == '4':
            limpiar_pantalla()
            print("\n" + "=" * 40)
            print("BUSCAR POR ID".center(40))
            print("=" * 40)
            id = input("\nIngrese el ID a buscar: ").strip()
            sistema.buscar_por_id(id)

        # Opción 5: Buscar por nombre
        elif opcion == '5':
            limpiar_pantalla()
            print("\n" + "=" * 40)
            print("BUSCAR POR NOMBRE".center(40))
            print("=" * 40)
            nombre = input("\nIngrese el nombre a buscar: ").strip()
            sistema.buscar_por_nombre(nombre)

        # Opción 6: Modificar registro
        elif opcion == '6':
            limpiar_pantalla()
            print("\n" + "=" * 40)
            print("MODIFICAR REGISTRO".center(40))
            print("=" * 40)
            id = input("\nIngrese el ID del registro a modificar: ").strip()
            sistema.modificar_registro(id)

        # Opción 7: Eliminar registro
        elif opcion == '7':
            limpiar_pantalla()
            print("\n" + "=" * 40)
            print("ELIMINAR REGISTRO".center(40))
            print("=" * 40)
            id = input("\nIngrese el ID del registro a eliminar: ").strip()
            sistema.eliminar_registro(id)

        # Opción 8: Guardar datos
        elif opcion == '8':
            limpiar_pantalla()
            sistema.guardar_datos()

        # Opción 9: Salir del sistema
        elif opcion == '9':
            limpiar_pantalla()
            print("\n" + "=" * 40)
            print("SALIR DEL SISTEMA".center(40))
            print("=" * 40)
            print("\nOpciones de salida:")
            print("1. Guardar y salir")
            print("2. Salir sin guardar")
            print("3. Cancelar y volver al menú")

            confirmacion = input("\nSeleccione una opción (1-3): ").strip()

            if confirmacion == '1':
                sistema.guardar_datos()
                print("\n✅ ¡Datos guardados correctamente! Saliendo del sistema...")
                break
            elif confirmacion == '2':
                print("\nℹ️ Saliendo sin guardar cambios...")
                break
            elif confirmacion == '3':
                continue
            else:
                print("\n❌ Opción no válida. Volviendo al menú principal...")

        # Opción no válida
        else:
            print("\n❌ Opción no válida. Intente nuevamente.")

        input("\nPresione Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    main()