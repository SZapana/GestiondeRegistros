#include <windows.h>
#include <fstream>
#include <sstream>
#include <string>

using namespace std;

// Estructura para almacenar los datos de cada estudiante
struct Estudiante {
    int id;             // ID único del estudiante
    string nombre;      // Nombre completo
    string correo;      // Correo electrónico
    string carrera;     // Carrera que estudia
    int anio;           // Año de ingreso
    Estudiante* siguiente; // Puntero al siguiente estudiante en la lista
};

// Variables globales
Estudiante* lista = nullptr;  // Puntero al inicio de la lista
int ultimoId = 0;             // Contador para asignar IDs

// Controles de la interfaz
HWND hNombre, hCorreo, hCarrera, hAnio; // Campos de entrada
HWND hLista;                            // Listbox para mostrar estudiantes
HWND hBusqueda;                         // Campo para búsqueda/ID a eliminar
HWND hIdModificar;                      // Campo para ID a modificar

// Función para generar IDs automáticamente
int GenerarId() {
    return ++ultimoId; // Incrementa y devuelve el último ID usado
}

// Función para agregar un nuevo estudiante
void AgregarEstudiante(HWND hwnd) {
    // Obtener datos de los campos de entrada
    char nombre[100], correo[100], carrera[100], anioStr[10];
    GetWindowText(hNombre, nombre, 100);
    GetWindowText(hCorreo, correo, 100);
    GetWindowText(hCarrera, carrera, 100);
    GetWindowText(hAnio, anioStr, 10);

    // Validar que todos los campos estén completos
    if (strlen(nombre) == 0 || strlen(correo) == 0 || strlen(carrera) == 0 || strlen(anioStr) == 0) {
        MessageBox(hwnd, "Todos los campos son obligatorios", "Error", MB_OK);
        return;
    }

    // Convertir año a número y validar
    int anio = atoi(anioStr);
    if (anio <= 0) {
        MessageBox(hwnd, "El año debe ser un número positivo", "Error", MB_OK);
        return;
    }

    // Crear nuevo estudiante
    Estudiante* nuevo = new Estudiante;
    nuevo->id = GenerarId();
    nuevo->nombre = nombre;
    nuevo->correo = correo;
    nuevo->carrera = carrera;
    nuevo->anio = anio;
    nuevo->siguiente = nullptr;

    // Agregar a la lista enlazada
    if (lista == nullptr) {
        lista = nuevo; // Si la lista está vacía, este es el primer elemento
    } else {
        // Buscar el último elemento y agregar el nuevo
        Estudiante* temp = lista;
        while (temp->siguiente != nullptr) {
            temp = temp->siguiente;
        }
        temp->siguiente = nuevo;
    }

    // Mostrar en la lista de la interfaz
    string item = to_string(nuevo->id) + " - " + nombre + " - " + correo;
    SendMessage(hLista, LB_ADDSTRING, 0, (LPARAM)item.c_str());

    // Limpiar campos después de agregar
    SetWindowText(hNombre, "");
    SetWindowText(hCorreo, "");
    SetWindowText(hCarrera, "");
    SetWindowText(hAnio, "");
}

// Función para mostrar todos los estudiantes
void MostrarEstudiantes() {
    // Limpiar la lista actual
    SendMessage(hLista, LB_RESETCONTENT, 0, 0);

    // Recorrer la lista enlazada y agregar cada estudiante
    Estudiante* temp = lista;
    while (temp != nullptr) {
        string item = to_string(temp->id) + " - " + temp->nombre + " - " + temp->correo;
        SendMessage(hLista, LB_ADDSTRING, 0, (LPARAM)item.c_str());
        temp = temp->siguiente;
    }
}

// Función para buscar estudiantes por ID o nombre
void BuscarEstudiante(HWND hwnd) {
    char busqueda[100];
    GetWindowText(hBusqueda, busqueda, 100);
    string strBusqueda = busqueda;

    // Validar que se ingresó un término de búsqueda
    if (strBusqueda.empty()) {
        MessageBox(hwnd, "Ingrese un ID o nombre para buscar", "Error", MB_OK);
        return;
    }

    // Limpiar la lista antes de mostrar resultados
    SendMessage(hLista, LB_RESETCONTENT, 0, 0);

    // Buscar coincidencias
    Estudiante* temp = lista;
    bool encontrado = false;

    while (temp != nullptr) {
        // Comparar con ID (convertido a string) o nombre
        if (to_string(temp->id) == strBusqueda ||
            temp->nombre.find(strBusqueda) != string::npos) {
            string item = to_string(temp->id) + " - " + temp->nombre + " - " + temp->correo;
            SendMessage(hLista, LB_ADDSTRING, 0, (LPARAM)item.c_str());
            encontrado = true;
        }
        temp = temp->siguiente;
    }

    // Mostrar mensaje si no se encontraron resultados
    if (!encontrado) {
        MessageBox(hwnd, "No se encontraron coincidencias", "Búsqueda", MB_OK);
    }
}

// Función para modificar un estudiante existente
void ModificarEstudiante(HWND hwnd) {
    char idStr[10], nombre[100], correo[100], carrera[100], anioStr[10];
    GetWindowText(hIdModificar, idStr, 10);
    GetWindowText(hNombre, nombre, 100);
    GetWindowText(hCorreo, correo, 100);
    GetWindowText(hCarrera, carrera, 100);
    GetWindowText(hAnio, anioStr, 10);

    // Validar ID
    if (strlen(idStr) == 0) {
        MessageBox(hwnd, "Ingrese un ID válido", "Error", MB_OK);
        return;
    }

    int id = atoi(idStr);
    if (id <= 0) {
        MessageBox(hwnd, "El ID debe ser un número positivo", "Error", MB_OK);
        return;
    }

    // Validar año
    int anio = atoi(anioStr);
    if (anio <= 0) {
        MessageBox(hwnd, "El año debe ser un número positivo", "Error", MB_OK);
        return;
    }

    // Buscar el estudiante a modificar
    Estudiante* temp = lista;
    bool encontrado = false;

    while (temp != nullptr) {
        if (temp->id == id) {
            // Actualizar datos
            temp->nombre = nombre;
            temp->correo = correo;
            temp->carrera = carrera;
            temp->anio = anio;
            encontrado = true;
            break;
        }
        temp = temp->siguiente;
    }

    // Mostrar resultado de la operación
    if (encontrado) {
        MessageBox(hwnd, "Estudiante modificado correctamente", "Éxito", MB_OK);
        MostrarEstudiantes(); // Actualizar la vista
    } else {
        MessageBox(hwnd, "ID no encontrado", "Error", MB_OK);
    }
}

// Función para eliminar un estudiante
void EliminarEstudiante(HWND hwnd) {
    char idStr[10];
    GetWindowText(hBusqueda, idStr, 10);

    // Validar ID
    if (strlen(idStr) == 0) {
        MessageBox(hwnd, "Ingrese un ID válido", "Error", MB_OK);
        return;
    }

    int id = atoi(idStr);
    if (id <= 0) {
        MessageBox(hwnd, "El ID debe ser un número positivo", "Error", MB_OK);
        return;
    }

    // Buscar el estudiante a eliminar
    Estudiante* temp = lista;
    Estudiante* anterior = nullptr;
    bool encontrado = false;

    while (temp != nullptr) {
        if (temp->id == id) {
            // Reorganizar los punteros para "saltar" el nodo a eliminar
            if (anterior == nullptr) {
                lista = temp->siguiente; // Era el primer elemento
            } else {
                anterior->siguiente = temp->siguiente;
            }
            delete temp; // Liberar memoria
            encontrado = true;
            break;
        }
        anterior = temp;
        temp = temp->siguiente;
    }

    // Mostrar resultado de la operación
    if (encontrado) {
        MessageBox(hwnd, "Estudiante eliminado correctamente", "Éxito", MB_OK);
        MostrarEstudiantes(); // Actualizar la vista
    } else {
        MessageBox(hwnd, "ID no encontrado", "Error", MB_OK);
    }
}

// Función para guardar los datos en archivo CSV
void GuardarArchivo() {
    ofstream file("registros.csv");
    if (!file.is_open()) {
        MessageBox(NULL, "Error al crear el archivo de registros", "Error", MB_OK);
        return;
    }

    // Recorrer la lista y escribir cada registro
    Estudiante* temp = lista;
    while (temp != nullptr) {
        file << temp->id << ";" << temp->nombre << ";" << temp->correo << ";"
             << temp->carrera << ";" << temp->anio << "\n";
        temp = temp->siguiente;
    }
    file.close();

    // Guardar también el último ID usado
    ofstream idFile("ultimo_id.txt");
    if (idFile.is_open()) {
        idFile << ultimoId;
        idFile.close();
    }

    MessageBox(NULL, "Datos guardados correctamente", "Éxito", MB_OK);
}

// Función para cargar datos desde archivo
void CargarArchivo(HWND hwnd) {
    // Limpiar la lista actual
    while (lista != nullptr) {
        Estudiante* temp = lista;
        lista = lista->siguiente;
        delete temp;
    }

    // Cargar el último ID usado
    ifstream idFile("ultimo_id.txt");
    if (idFile.is_open()) {
        string idStr;
        getline(idFile, idStr);
        if (!idStr.empty()) {
            try {
                ultimoId = stoi(idStr);
            } catch (...) {
                ultimoId = 0; // Valor por defecto si hay error
            }
        }
        idFile.close();
    }

    // Cargar los registros de estudiantes
    ifstream file("registros.csv");
    if (!file.is_open()) {
        MessageBox(hwnd, "No se encontró archivo de registros. Se creará uno nuevo al guardar.", "Información", MB_OK);
        return;
    }

    string linea;
    while (getline(file, linea)) {
        if (linea.empty()) continue; // Saltar líneas vacías

        stringstream ss(linea);
        string idStr, nombre, correo, carrera, anioStr;

        // Leer los campos separados por ;
        if (!getline(ss, idStr, ';') ||
            !getline(ss, nombre, ';') ||
            !getline(ss, correo, ';') ||
            !getline(ss, carrera, ';') ||
            !getline(ss, anioStr, ';')) {
            continue; // Saltar líneas mal formateadas
        }

        try {
            // Convertir y validar datos
            int id = stoi(idStr);
            int anio = stoi(anioStr);

            // Crear nuevo estudiante
            Estudiante* nuevo = new Estudiante;
            nuevo->id = id;
            nuevo->nombre = nombre;
            nuevo->correo = correo;
            nuevo->carrera = carrera;
            nuevo->anio = anio;
            nuevo->siguiente = nullptr;

            // Agregar a la lista
            if (lista == nullptr) {
                lista = nuevo;
            } else {
                Estudiante* temp = lista;
                while (temp->siguiente != nullptr) {
                    temp = temp->siguiente;
                }
                temp->siguiente = nuevo;
            }
        } catch (...) {
            continue; // Saltar registros con datos inválidos
        }
    }
    file.close();

    // Mostrar los estudiantes cargados
    MostrarEstudiantes();
    MessageBox(hwnd, "Datos cargados correctamente", "Éxito", MB_OK);
}

// Función para manejar los mensajes de la ventana
LRESULT CALLBACK WindowProcedure(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp) {
    switch (msg) {
    case WM_COMMAND:
        // Manejar eventos de los botones
        switch (wp) {
        case 1: AgregarEstudiante(hwnd); break;     // Botón Agregar
        case 2: MostrarEstudiantes(); break;        // Botón Mostrar Todos
        case 3: BuscarEstudiante(hwnd); break;      // Botón Buscar
        case 4: ModificarEstudiante(hwnd); break;   // Botón Modificar
        case 5: EliminarEstudiante(hwnd); break;    // Botón Eliminar
        case 6: GuardarArchivo(); break;            // Botón Guardar
        case 7: CargarArchivo(hwnd); break;        // Botón Cargar
        }
        break;
    case WM_DESTROY:
        PostQuitMessage(0); // Salir de la aplicación
        break;
    default:
        return DefWindowProc(hwnd, msg, wp, lp);
    }
    return 0;
}

// Función para crear los controles de la interfaz
void CrearControles(HWND hwnd) {
    // Crear etiquetas y campos de entrada
    CreateWindow("STATIC", "Nombre:", WS_VISIBLE | WS_CHILD, 20, 20, 80, 20, hwnd, NULL, NULL, NULL);
    hNombre = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 20, 200, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("STATIC", "Correo:", WS_VISIBLE | WS_CHILD, 20, 50, 80, 20, hwnd, NULL, NULL, NULL);
    hCorreo = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 50, 200, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("STATIC", "Carrera:", WS_VISIBLE | WS_CHILD, 20, 80, 80, 20, hwnd, NULL, NULL, NULL);
    hCarrera = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 80, 200, 20, hwnd, NULL, NULL, NULL);

    CreateWindow("STATIC", "Año:", WS_VISIBLE | WS_CHILD, 20, 110, 80, 20, hwnd, NULL, NULL, NULL);
    hAnio = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 110, 100, 20, hwnd, NULL, NULL, NULL);

    // Campo para búsqueda/eliminación (usa el mismo campo para simplificar)
    CreateWindow("STATIC", "Buscar/Eliminar (ID):", WS_VISIBLE | WS_CHILD, 20, 140, 150, 20, hwnd, NULL, NULL, NULL);
    hBusqueda = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 170, 140, 100, 20, hwnd, NULL, NULL, NULL);

    // Campo para ID a modificar
    CreateWindow("STATIC", "Modificar (ID):", WS_VISIBLE | WS_CHILD, 20, 170, 150, 20, hwnd, NULL, NULL, NULL);
    hIdModificar = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 170, 170, 100, 20, hwnd, NULL, NULL, NULL);

    // Crear botones con sus IDs correspondientes
    CreateWindow("BUTTON", "Agregar", WS_VISIBLE | WS_CHILD, 300, 20, 100, 30, hwnd, (HMENU)1, NULL, NULL);
    CreateWindow("BUTTON", "Mostrar Todos", WS_VISIBLE | WS_CHILD, 300, 60, 100, 30, hwnd, (HMENU)2, NULL, NULL);
    CreateWindow("BUTTON", "Buscar", WS_VISIBLE | WS_CHILD, 300, 100, 100, 30, hwnd, (HMENU)3, NULL, NULL);
    CreateWindow("BUTTON", "Modificar", WS_VISIBLE | WS_CHILD, 300, 140, 100, 30, hwnd, (HMENU)4, NULL, NULL);
    CreateWindow("BUTTON", "Eliminar", WS_VISIBLE | WS_CHILD, 300, 180, 100, 30, hwnd, (HMENU)5, NULL, NULL);
    CreateWindow("BUTTON", "Guardar", WS_VISIBLE | WS_CHILD, 300, 220, 100, 30, hwnd, (HMENU)6, NULL, NULL);
    CreateWindow("BUTTON", "Cargar", WS_VISIBLE | WS_CHILD, 300, 260, 100, 30, hwnd, (HMENU)7, NULL, NULL);

    // Crear lista para mostrar los estudiantes
    hLista = CreateWindow("LISTBOX", NULL,
                         WS_VISIBLE | WS_CHILD | WS_BORDER | LBS_NOTIFY | WS_VSCROLL,
                         20, 210, 380, 200, hwnd, NULL, NULL, NULL);
}

// Función principal
int WINAPI WinMain(HINSTANCE hInst, HINSTANCE hPrev, LPSTR args, int nCmdShow) {
    // Registrar la clase de la ventana
    WNDCLASS wc = { 0 };
    wc.hbrBackground = (HBRUSH)COLOR_WINDOW;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hInstance = hInst;
    wc.lpszClassName = "RegistroWin";
    wc.lpfnWndProc = WindowProcedure;

    if (!RegisterClass(&wc)) return -1;

    // Crear la ventana principal
    HWND hwnd = CreateWindow("RegistroWin", "Sistema de Registro Académico",
                            WS_OVERLAPPEDWINDOW | WS_VISIBLE,
                            100, 100, 450, 450, NULL, NULL, NULL, NULL);

    // Crear los controles de la interfaz
    CrearControles(hwnd);

    // Cargar datos al iniciar la aplicación
    CargarArchivo(hwnd);

    // Bucle principal de mensajes
    MSG msg = { 0 };
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    // Liberar memoria antes de salir
    while (lista != nullptr) {
        Estudiante* temp = lista;
        lista = lista->siguiente;
        delete temp;
    }

    return 0;
}
