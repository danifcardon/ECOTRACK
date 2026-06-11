# EcoTrack · VerdeMov S.A.

MVP de gestión de flota eléctrica para logística urbana sustentable. Permite administrar usuarios, vehículos, conductores y viajes desde una interfaz web construida con Streamlit.

---

## Requisitos previos

- **Python 3.11+**
- **pip** (gestor de paquetes de Python)
- Conexión a internet solo para la primera instalación de dependencias

---

## Ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/danifcardon/ECOTRACK.git
cd ECOTRACK
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Iniciar la aplicación

```bash
streamlit run app.py
```

La app se abrirá en el navegador, normalmente en `http://localhost:8501`.

### 4. Base de datos

- SQLite se crea automáticamente al primer inicio (`ecotrack.db` en la raíz del proyecto).
- Incluye datos de ejemplo: 5 usuarios, 6 vehículos, 5 conductores y 6 viajes.
- Para reiniciar los datos, eliminá `ecotrack.db` y volvé a ejecutar la app.

---

## Cuentas para probar

### Acceso al sistema (login)

| Campo      | Valor           |
|------------|-----------------|
| Usuario    | `admin`         |
| Contraseña | `ecotrack2025`  |

### Usuarios de ejemplo en la base de datos

| Nombre            | Email                          | Rol             | Estado   |
|-------------------|--------------------------------|-----------------|----------|
| María González    | maria.gonzalez@verdemov.com    | Administrador   | Activo   |
| Carlos Ruiz       | carlos.ruiz@verdemov.com       | Operador        | Activo   |
| Lucía Fernández   | lucia.fernandez@verdemov.com   | Logística       | Activo   |
| Diego Martínez    | diego.martinez@verdemov.com    | Mantenimiento   | Activo   |
| Ana Torres        | ana.torres@verdemov.com        | Operador        | Inactivo |

---

## Flujo de prueba recomendado

1. **Login** con `admin` / `ecotrack2025`.
2. **Dashboard** — revisar KPIs, gráficos y alertas (batería baja, vencimientos).
3. **Vehículos** — filtrar por estado/tipo; probar alta, edición y eliminación.
4. **Conductores** — verificar alertas de licencia por vencer.
5. **Viajes** — registrar un viaje asignando conductor y vehículo disponibles.
6. **Completar viaje** — marcar como completado con km y consumo kWh.
7. **Dashboard** — confirmar que los KPIs se actualizaron (km del vehículo, estados liberados).

### Datos útiles para alertas del dashboard

| Recurso   | Identificador | Detalle                              |
|-----------|---------------|--------------------------------------|
| Vehículo  | `AD789GH`     | Batería al 15%                       |
| Vehículo  | `AE012IJ`     | VTV por vencer en ~15 días           |
| Vehículo  | `AD789GH`     | Seguro por vencer en ~25 días        |
| Conductor | Sofía López   | Licencia por vencer en ~20 días      |

---

## Estructura del proyecto

```
ECOTRACK/
├── app.py              # Entry point, login y navegación
├── database.py         # SQLite, tablas, CRUD y datos de ejemplo
├── pages/              # Dashboard, usuarios, vehículos, conductores, viajes
├── utils/helpers.py    # Utilidades (fechas, batería, alertas)
├── requirements.txt
└── .streamlit/         # Tema visual VerdeMov
```

---

## Stack técnico

- Python + Streamlit
- SQLite (stdlib `sqlite3`)
- Pandas (tablas y reportes)
- Plotly (gráficos)

---

## Identidad visual

| Elemento   | Color     |
|------------|-----------|
| Primario   | `#2E7D32` |
| Secundario | `#66BB6A` |
| Acento     | `#A5D6A7` |
| Fondo      | `#F1F8E9` |
| Texto      | `#1B1B1B` |
