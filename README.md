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
| Contraseña | `admin`         |

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

1. **Login** con `admin` / `admin`.
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
├── views/              # Dashboard, usuarios, vehículos, conductores, viajes
├── ecotrack_utils/     # Constantes, tema, validadores y helpers
├── requirements.txt
└── .streamlit/         # Tema visual VerdeMov
```

> **Nota:** Las vistas están en `views/` (no en `pages/`) para evitar que Streamlit Cloud exponga rutas sin pasar por el login.

---

## Despliegue en Streamlit Community Cloud (gratis)

### Lo que ya está preparado en el repo

- `app.py` como punto de entrada
- `requirements.txt` con dependencias
- `.python-version` → Python 3.11
- `.streamlit/config.toml` con tema VerdeMov
- Login compatible con **Secrets** de Streamlit Cloud
- Base SQLite que se inicializa sola con datos de ejemplo

### Pasos que debés hacer vos

#### 1. Subir los últimos cambios a GitHub

```bash
git add .
git commit -m "Preparar despliegue en Streamlit Cloud"
git push origin main
```

#### 2. Crear cuenta en Streamlit Cloud

1. Entrá a [share.streamlit.io](https://share.streamlit.io)
2. Iniciá sesión con tu cuenta de **GitHub** (la misma del repo `danifcardon/ECOTRACK`)

#### 3. Crear la app

1. Clic en **New app**
2. Completá:
   - **Repository:** `danifcardon/ECOTRACK`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Clic en **Deploy**

#### 4. (Opcional) Configurar credenciales en Secrets

En la app desplegada → **Settings** → **Secrets**, pegá:

```toml
[auth]
username = "admin"
password = "admin"
display_name = "Administrador"
```

Si no configurás secrets, funcionan las mismas credenciales por defecto del MVP.

#### 5. Compartir la URL

Streamlit te dará una URL pública tipo:

`https://ecotrack-xxxxx.streamlit.app`

Esa es la que podés entregar a tu profesor.

### Importante sobre SQLite en la nube

- Los datos **pueden reiniciarse** cuando Streamlit redeploya la app.
- Al iniciar, `init_db()` vuelve a crear la base con **datos de ejemplo** si está vacía.
- Para un MVP/demo universitario esto suele ser suficiente.

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
