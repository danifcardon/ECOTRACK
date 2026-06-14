import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

from utils.errors import ValidationError
from utils.validators import normalize_dni, normalize_patente

DB_PATH = Path(__file__).parent / "ecotrack.db"


def get_db_path() -> Path:
    return DB_PATH


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            rol TEXT NOT NULL,
            activo INTEGER DEFAULT 1,
            fecha_creacion TEXT
        );

        CREATE TABLE IF NOT EXISTS vehiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patente TEXT UNIQUE NOT NULL,
            modelo TEXT NOT NULL,
            marca TEXT NOT NULL,
            anio INTEGER,
            tipo TEXT,
            estado TEXT,
            nivel_bateria INTEGER,
            km_totales INTEGER DEFAULT 0,
            vencimiento_vtv TEXT,
            vencimiento_seguro TEXT,
            notas TEXT
        );

        CREATE TABLE IF NOT EXISTS conductores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            dni TEXT UNIQUE NOT NULL,
            telefono TEXT,
            licencia TEXT,
            vencimiento_licencia TEXT,
            estado TEXT,
            activo INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS viajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            vehiculo_id INTEGER REFERENCES vehiculos(id),
            conductor_id INTEGER REFERENCES conductores(id),
            origen TEXT NOT NULL,
            destino TEXT NOT NULL,
            km_recorridos REAL,
            estado TEXT,
            consumo_kwh REAL,
            notas TEXT
        );
    """)

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        _insert_sample_data(cursor)

    conn.commit()
    conn.close()


def _insert_sample_data(cursor: sqlite3.Cursor) -> None:
    hoy = datetime.now()
    fecha_creacion = hoy.strftime("%Y-%m-%d")
    vtv_proximo = (hoy + timedelta(days=15)).strftime("%Y-%m-%d")
    seguro_proximo = (hoy + timedelta(days=25)).strftime("%Y-%m-%d")
    licencia_proximo = (hoy + timedelta(days=20)).strftime("%Y-%m-%d")
    licencia_ok = (hoy + timedelta(days=180)).strftime("%Y-%m-%d")
    vtv_ok = (hoy + timedelta(days=200)).strftime("%Y-%m-%d")
    seguro_ok = (hoy + timedelta(days=300)).strftime("%Y-%m-%d")
    mes_actual = hoy.strftime("%Y-%m")

    usuarios = [
        ("María González", "maria.gonzalez@verdemov.com", "Administrador", 1, fecha_creacion),
        ("Carlos Ruiz", "carlos.ruiz@verdemov.com", "Operador", 1, fecha_creacion),
        ("Lucía Fernández", "lucia.fernandez@verdemov.com", "Logística", 1, fecha_creacion),
        ("Diego Martínez", "diego.martinez@verdemov.com", "Mantenimiento", 1, fecha_creacion),
        ("Ana Torres", "ana.torres@verdemov.com", "Operador", 0, fecha_creacion),
    ]
    cursor.executemany(
        "INSERT INTO usuarios (nombre, email, rol, activo, fecha_creacion) VALUES (?, ?, ?, ?, ?)",
        usuarios,
    )

    vehiculos = [
        ("AB123CD", "eSprinter", "Mercedes-Benz", 2023, "Furgón", "Disponible", 85, 12450, vtv_ok, seguro_ok, "Unidad principal zona norte"),
        ("AC456EF", "Kangoo E-Tech", "Renault", 2022, "Van", "En ruta", 62, 28700, vtv_ok, seguro_ok, "Repartos Córdoba centro"),
        ("AD789GH", "Super Soco CPx", "Super Soco", 2024, "Moto", "Disponible", 15, 3200, vtv_ok, seguro_proximo, "Batería baja - recargar"),
        ("AE012IJ", "eDeliver 3", "Maxus", 2023, "Furgón", "En mantenimiento", 45, 15600, vtv_proximo, seguro_ok, "Service programado"),
        ("AF345KL", "Cargo Bike Pro", "Urban Arrow", 2024, "Bicicleta eléctrica", "Disponible", 92, 890, vtv_ok, seguro_ok, "Microcentro Buenos Aires"),
        ("AG678MN", "eVito", "Mercedes-Benz", 2021, "Van", "Fuera de servicio", 0, 45200, vtv_ok, seguro_ok, "Esperando repuesto"),
    ]
    cursor.executemany(
        """INSERT INTO vehiculos
           (patente, modelo, marca, anio, tipo, estado, nivel_bateria, km_totales,
            vencimiento_vtv, vencimiento_seguro, notas)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        vehiculos,
    )

    conductores = [
        ("Juan Pérez", "30123456", "11-4444-5555", "B12345678", licencia_ok, "Disponible", 1),
        ("Sofía López", "28987654", "11-5555-6666", "B87654321", licencia_proximo, "En ruta", 1),
        ("Martín Giménez", "33456789", "351-444-3333", "B11223344", licencia_ok, "Disponible", 1),
        ("Valentina Acosta", "35678901", "341-222-1111", "B99887766", licencia_ok, "Inactivo", 0),
        ("Facundo Herrera", "27890123", "11-7777-8888", "B55443322", licencia_ok, "Disponible", 1),
    ]
    cursor.executemany(
        """INSERT INTO conductores
           (nombre, dni, telefono, licencia, vencimiento_licencia, estado, activo)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        conductores,
    )

    viajes = [
        (f"{mes_actual}-05", 2, 2, "Buenos Aires - Palermo", "Buenos Aires - Belgrano", 18.5, "Completado", 4.2, "Entrega express"),
        (f"{mes_actual}-08", 1, 1, "Buenos Aires - Microcentro", "Buenos Aires - Puerto Madero", 12.0, "Completado", 3.1, None),
        (f"{mes_actual}-10", 5, 3, "Córdoba - Nueva Córdoba", "Córdoba - Villa Carlos Paz", 35.0, "Completado", 2.8, "Ruta interurbana corta"),
        (f"{mes_actual}-12", 2, 2, "Rosario - Centro", "Rosario - Fisherton", 22.0, "En curso", None, "En progreso"),
        (f"{mes_actual}-15", 1, 5, "Buenos Aires - Recoleta", "Buenos Aires - Caballito", 8.5, "Planificado", None, "Programado mañana"),
        (f"{mes_actual}-03", 4, 1, "Buenos Aires - San Telmo", "Buenos Aires - La Boca", 6.0, "Cancelado", None, "Cliente canceló"),
    ]
    cursor.executemany(
        """INSERT INTO viajes
           (fecha, vehiculo_id, conductor_id, origen, destino, km_recorridos, estado, consumo_kwh, notas)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        viajes,
    )


def fetch_all(query: str, params: tuple = ()) -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def fetch_one(query: str, params: tuple = ()) -> sqlite3.Row | None:
    conn = get_connection()
    row = conn.execute(query, params).fetchone()
    conn.close()
    return row


def execute(query: str, params: tuple = ()) -> int:
    conn = get_connection()
    cursor = conn.execute(query, params)
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def email_exists(email: str, exclude_id: int | None = None) -> bool:
    if exclude_id:
        row = fetch_one("SELECT id FROM usuarios WHERE email = ? AND id != ?", (email, exclude_id))
    else:
        row = fetch_one("SELECT id FROM usuarios WHERE email = ?", (email,))
    return row is not None


def patente_exists(patente: str, exclude_id: int | None = None) -> bool:
    patente = normalize_patente(patente)
    if exclude_id:
        row = fetch_one("SELECT id FROM vehiculos WHERE patente = ? AND id != ?", (patente, exclude_id))
    else:
        row = fetch_one("SELECT id FROM vehiculos WHERE patente = ?", (patente,))
    return row is not None


def dni_exists(dni: str, exclude_id: int | None = None) -> bool:
    dni = normalize_dni(dni)
    if exclude_id:
        row = fetch_one("SELECT id FROM conductores WHERE dni = ? AND id != ?", (dni, exclude_id))
    else:
        row = fetch_one("SELECT id FROM conductores WHERE dni = ?", (dni,))
    return row is not None


def count_viajes_activos_vehiculo(vehiculo_id: int, exclude_viaje_id: int | None = None) -> int:
    query = "SELECT COUNT(*) AS c FROM viajes WHERE vehiculo_id = ? AND estado IN ('Planificado', 'En curso')"
    params: list = [vehiculo_id]
    if exclude_viaje_id:
        query += " AND id != ?"
        params.append(exclude_viaje_id)
    return fetch_one(query, tuple(params))["c"]


def count_viajes_activos_conductor(conductor_id: int, exclude_viaje_id: int | None = None) -> int:
    query = "SELECT COUNT(*) AS c FROM viajes WHERE conductor_id = ? AND estado IN ('Planificado', 'En curso')"
    params: list = [conductor_id]
    if exclude_viaje_id:
        query += " AND id != ?"
        params.append(exclude_viaje_id)
    return fetch_one(query, tuple(params))["c"]


def count_viajes_vehiculo(vehiculo_id: int) -> int:
    return fetch_one("SELECT COUNT(*) AS c FROM viajes WHERE vehiculo_id = ?", (vehiculo_id,))["c"]


def count_viajes_conductor(conductor_id: int) -> int:
    return fetch_one("SELECT COUNT(*) AS c FROM viajes WHERE conductor_id = ?", (conductor_id,))["c"]


def _assert_vehiculo_disponible(vehiculo_id: int) -> None:
    vehiculo = get_vehiculo(vehiculo_id)
    if not vehiculo:
        raise ValidationError("El vehículo seleccionado no existe.")
    if vehiculo["estado"] != "Disponible":
        raise ValidationError(f"El vehículo {vehiculo['patente']} no está disponible (estado: {vehiculo['estado']}).")


def _assert_conductor_disponible(conductor_id: int) -> None:
    conductor = get_conductor(conductor_id)
    if not conductor:
        raise ValidationError("El conductor seleccionado no existe.")
    if conductor["activo"] != 1:
        raise ValidationError(f"El conductor {conductor['nombre']} está inactivo.")
    if conductor["estado"] != "Disponible":
        raise ValidationError(f"El conductor {conductor['nombre']} no está disponible (estado: {conductor['estado']}).")
    if conductor["vencimiento_licencia"]:
        venc = date.fromisoformat(conductor["vencimiento_licencia"])
        if venc <= date.today():
            raise ValidationError(f"La licencia del conductor {conductor['nombre']} está vencida.")


def get_usuarios() -> list[sqlite3.Row]:
    return fetch_all("SELECT * FROM usuarios ORDER BY nombre")


def get_usuario(usuario_id: int) -> sqlite3.Row | None:
    return fetch_one("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))


def insert_usuario(nombre: str, email: str, rol: str) -> int:
    email = email.strip().lower()
    if email_exists(email):
        raise ValidationError("Ya existe un usuario con ese email.")
    fecha = datetime.now().strftime("%Y-%m-%d")
    return execute(
        "INSERT INTO usuarios (nombre, email, rol, activo, fecha_creacion) VALUES (?, ?, ?, 1, ?)",
        (nombre.strip(), email, rol, fecha),
    )


def update_usuario(usuario_id: int, nombre: str, email: str, rol: str) -> None:
    if not get_usuario(usuario_id):
        raise ValidationError("El usuario no existe.")
    email = email.strip().lower()
    if email_exists(email, exclude_id=usuario_id):
        raise ValidationError("Ya existe otro usuario con ese email.")
    execute(
        "UPDATE usuarios SET nombre = ?, email = ?, rol = ? WHERE id = ?",
        (nombre.strip(), email, rol, usuario_id),
    )


def desactivar_usuario(usuario_id: int) -> None:
    execute("UPDATE usuarios SET activo = 0 WHERE id = ?", (usuario_id,))


def activar_usuario(usuario_id: int) -> None:
    execute("UPDATE usuarios SET activo = 1 WHERE id = ?", (usuario_id,))


def get_vehiculos(estado: str | None = None, tipo: str | None = None) -> list[sqlite3.Row]:
    query = "SELECT * FROM vehiculos WHERE 1=1"
    params: list = []
    if estado and estado != "Todos":
        query += " AND estado = ?"
        params.append(estado)
    if tipo and tipo != "Todos":
        query += " AND tipo = ?"
        params.append(tipo)
    query += " ORDER BY patente"
    return fetch_all(query, tuple(params))


def get_vehiculo(vehiculo_id: int) -> sqlite3.Row | None:
    return fetch_one("SELECT * FROM vehiculos WHERE id = ?", (vehiculo_id,))


def get_vehiculos_disponibles() -> list[sqlite3.Row]:
    return fetch_all("SELECT * FROM vehiculos WHERE estado = 'Disponible' ORDER BY patente")


def insert_vehiculo(data: dict) -> int:
    patente = normalize_patente(data["patente"])
    if patente_exists(patente):
        raise ValidationError(f"Ya existe un vehículo con la patente {patente}.")
    return execute(
        """INSERT INTO vehiculos
           (patente, modelo, marca, anio, tipo, estado, nivel_bateria, km_totales,
            vencimiento_vtv, vencimiento_seguro, notas)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            patente, data["modelo"].strip(), data["marca"].strip(), data["anio"], data["tipo"],
            data["estado"], data["nivel_bateria"], data["km_totales"],
            data["vencimiento_vtv"], data["vencimiento_seguro"], data.get("notas"),
        ),
    )


def update_vehiculo(vehiculo_id: int, data: dict) -> None:
    if not get_vehiculo(vehiculo_id):
        raise ValidationError("El vehículo no existe.")
    patente = normalize_patente(data["patente"])
    if patente_exists(patente, exclude_id=vehiculo_id):
        raise ValidationError(f"Ya existe otro vehículo con la patente {patente}.")
    if data["estado"] == "Disponible" and count_viajes_activos_vehiculo(vehiculo_id) > 0:
        raise ValidationError("No se puede marcar como Disponible: el vehículo tiene viajes activos.")
    execute(
        """UPDATE vehiculos SET patente=?, modelo=?, marca=?, anio=?, tipo=?, estado=?,
           nivel_bateria=?, km_totales=?, vencimiento_vtv=?, vencimiento_seguro=?, notas=?
           WHERE id=?""",
        (
            patente, data["modelo"].strip(), data["marca"].strip(), data["anio"], data["tipo"],
            data["estado"], data["nivel_bateria"], data["km_totales"],
            data["vencimiento_vtv"], data["vencimiento_seguro"], data.get("notas"), vehiculo_id,
        ),
    )


def delete_vehiculo(vehiculo_id: int) -> None:
    if not get_vehiculo(vehiculo_id):
        raise ValidationError("El vehículo no existe.")
    if count_viajes_activos_vehiculo(vehiculo_id) > 0:
        raise ValidationError("No se puede eliminar: el vehículo tiene viajes planificados o en curso.")
    if count_viajes_vehiculo(vehiculo_id) > 0:
        raise ValidationError("No se puede eliminar: el vehículo tiene viajes asociados en el historial.")
    execute("DELETE FROM vehiculos WHERE id = ?", (vehiculo_id,))


def update_vehiculo_km_estado(vehiculo_id: int, km_extra: float, estado: str) -> None:
    execute(
        "UPDATE vehiculos SET km_totales = km_totales + ?, estado = ? WHERE id = ?",
        (int(km_extra), estado, vehiculo_id),
    )


def get_conductores(estado: str | None = None, activo: str | None = None) -> list[sqlite3.Row]:
    query = "SELECT * FROM conductores WHERE 1=1"
    params: list = []
    if estado and estado != "Todos":
        query += " AND estado = ?"
        params.append(estado)
    if activo == "Activos":
        query += " AND activo = 1"
    elif activo == "Inactivos":
        query += " AND activo = 0"
    query += " ORDER BY nombre"
    return fetch_all(query, tuple(params))


def get_conductor(conductor_id: int) -> sqlite3.Row | None:
    return fetch_one("SELECT * FROM conductores WHERE id = ?", (conductor_id,))


def get_conductores_disponibles() -> list[sqlite3.Row]:
    return fetch_all(
        "SELECT * FROM conductores WHERE estado = 'Disponible' AND activo = 1 ORDER BY nombre"
    )


def insert_conductor(data: dict) -> int:
    dni = normalize_dni(data["dni"])
    if dni_exists(dni):
        raise ValidationError(f"Ya existe un conductor con el DNI {dni}.")
    return execute(
        """INSERT INTO conductores
           (nombre, dni, telefono, licencia, vencimiento_licencia, estado, activo)
           VALUES (?, ?, ?, ?, ?, ?, 1)""",
        (
            data["nombre"].strip(), dni, data.get("telefono"), data.get("licencia"),
            data["vencimiento_licencia"], data["estado"],
        ),
    )


def update_conductor(conductor_id: int, data: dict) -> None:
    if not get_conductor(conductor_id):
        raise ValidationError("El conductor no existe.")
    dni = normalize_dni(data["dni"])
    if dni_exists(dni, exclude_id=conductor_id):
        raise ValidationError(f"Ya existe otro conductor con el DNI {dni}.")
    if data["estado"] == "Disponible" and count_viajes_activos_conductor(conductor_id) > 0:
        raise ValidationError("No se puede marcar como Disponible: el conductor tiene viajes activos.")
    if data["estado"] in ("Disponible", "En ruta") and data["activo"] != 1:
        raise ValidationError("Un conductor inactivo no puede estar Disponible o En ruta.")
    execute(
        """UPDATE conductores SET nombre=?, dni=?, telefono=?, licencia=?,
           vencimiento_licencia=?, estado=?, activo=? WHERE id=?""",
        (
            data["nombre"].strip(), dni, data.get("telefono"), data.get("licencia"),
            data["vencimiento_licencia"], data["estado"], data["activo"], conductor_id,
        ),
    )


def delete_conductor(conductor_id: int) -> None:
    if not get_conductor(conductor_id):
        raise ValidationError("El conductor no existe.")
    if count_viajes_activos_conductor(conductor_id) > 0:
        raise ValidationError("No se puede eliminar: el conductor tiene viajes planificados o en curso.")
    if count_viajes_conductor(conductor_id) > 0:
        raise ValidationError("No se puede eliminar: el conductor tiene viajes asociados en el historial.")
    execute("DELETE FROM conductores WHERE id = ?", (conductor_id,))


def get_viajes(estado: str | None = None, fecha_desde: str | None = None, fecha_hasta: str | None = None) -> list[sqlite3.Row]:
    query = """
        SELECT v.*, ve.patente, ve.modelo, c.nombre AS conductor_nombre
        FROM viajes v
        LEFT JOIN vehiculos ve ON v.vehiculo_id = ve.id
        LEFT JOIN conductores c ON v.conductor_id = c.id
        WHERE 1=1
    """
    params: list = []
    if estado and estado != "Todos":
        query += " AND v.estado = ?"
        params.append(estado)
    if fecha_desde:
        query += " AND v.fecha >= ?"
        params.append(fecha_desde)
    if fecha_hasta:
        query += " AND v.fecha <= ?"
        params.append(fecha_hasta)
    query += " ORDER BY v.fecha DESC, v.id DESC"
    return fetch_all(query, tuple(params))


def get_viaje(viaje_id: int) -> sqlite3.Row | None:
    return fetch_one(
        """SELECT v.*, ve.patente, ve.modelo, c.nombre AS conductor_nombre
           FROM viajes v
           LEFT JOIN vehiculos ve ON v.vehiculo_id = ve.id
           LEFT JOIN conductores c ON v.conductor_id = c.id
           WHERE v.id = ?""",
        (viaje_id,),
    )


def insert_viaje(data: dict) -> int:
    estado = data["estado"]
    if estado not in ("Planificado", "En curso", "Completado", "Cancelado"):
        raise ValidationError("Estado de viaje inválido.")

    vehiculo = get_vehiculo(data["vehiculo_id"])
    conductor = get_conductor(data["conductor_id"])
    if not vehiculo or not conductor:
        raise ValidationError("Vehículo o conductor no encontrado.")

    if estado in ("Planificado", "En curso"):
        _assert_vehiculo_disponible(data["vehiculo_id"])
        _assert_conductor_disponible(data["conductor_id"])
    elif estado == "Completado":
        if not data.get("km_recorridos") or data["km_recorridos"] <= 0:
            raise ValidationError("Un viaje completado requiere km recorridos mayores a 0.")

    viaje_id = execute(
        """INSERT INTO viajes
           (fecha, vehiculo_id, conductor_id, origen, destino, km_recorridos, estado, consumo_kwh, notas)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            data["fecha"], data["vehiculo_id"], data["conductor_id"],
            data["origen"].strip(), data["destino"].strip(), data.get("km_recorridos"),
            estado, data.get("consumo_kwh"), data.get("notas"),
        ),
    )
    if estado in ("Planificado", "En curso"):
        execute("UPDATE vehiculos SET estado = 'En ruta' WHERE id = ?", (data["vehiculo_id"],))
        execute("UPDATE conductores SET estado = 'En ruta' WHERE id = ?", (data["conductor_id"],))
    return viaje_id


def update_viaje(viaje_id: int, data: dict) -> None:
    viaje_anterior = fetch_one("SELECT * FROM viajes WHERE id = ?", (viaje_id,))
    if not viaje_anterior:
        raise ValidationError("El viaje no existe.")

    estado = data["estado"]
    estado_prev = viaje_anterior["estado"]

    if estado == "Completado":
        if not data.get("km_recorridos") or data["km_recorridos"] <= 0:
            raise ValidationError("Para completar el viaje, los km recorridos deben ser mayores a 0.")
        if not data.get("consumo_kwh") or data["consumo_kwh"] <= 0:
            raise ValidationError("Para completar el viaje, el consumo en kWh es obligatorio.")

    if estado in ("Planificado", "En curso") and estado_prev in ("Completado", "Cancelado"):
        _assert_vehiculo_disponible(data["vehiculo_id"])
        _assert_conductor_disponible(data["conductor_id"])

    execute(
        """UPDATE viajes SET fecha=?, vehiculo_id=?, conductor_id=?, origen=?, destino=?,
           km_recorridos=?, estado=?, consumo_kwh=?, notas=? WHERE id=?""",
        (
            data["fecha"], data["vehiculo_id"], data["conductor_id"],
            data["origen"].strip(), data["destino"].strip(), data.get("km_recorridos"),
            estado, data.get("consumo_kwh"), data.get("notas"), viaje_id,
        ),
    )

    if estado == "Completado" and estado_prev != "Completado":
        km = data.get("km_recorridos") or 0
        update_vehiculo_km_estado(data["vehiculo_id"], km, "Disponible")
        execute("UPDATE conductores SET estado = 'Disponible' WHERE id = ?", (data["conductor_id"],))
    elif estado == "Cancelado" and estado_prev in ("Planificado", "En curso"):
        execute("UPDATE vehiculos SET estado = 'Disponible' WHERE id = ?", (data["vehiculo_id"],))
        execute("UPDATE conductores SET estado = 'Disponible' WHERE id = ?", (data["conductor_id"],))
    elif estado in ("Planificado", "En curso") and estado_prev in ("Completado", "Cancelado"):
        execute("UPDATE vehiculos SET estado = 'En ruta' WHERE id = ?", (data["vehiculo_id"],))
        execute("UPDATE conductores SET estado = 'En ruta' WHERE id = ?", (data["conductor_id"],))


def delete_viaje(viaje_id: int) -> None:
    viaje = fetch_one("SELECT * FROM viajes WHERE id = ?", (viaje_id,))
    if not viaje:
        raise ValidationError("El viaje no existe.")
    execute("DELETE FROM viajes WHERE id = ?", (viaje_id,))
    if viaje["estado"] in ("Planificado", "En curso"):
        if count_viajes_activos_vehiculo(viaje["vehiculo_id"]) == 0:
            execute("UPDATE vehiculos SET estado = 'Disponible' WHERE id = ?", (viaje["vehiculo_id"],))
        if count_viajes_activos_conductor(viaje["conductor_id"]) == 0:
            execute("UPDATE conductores SET estado = 'Disponible' WHERE id = ?", (viaje["conductor_id"],))


def get_dashboard_kpis() -> dict:
    hoy = datetime.now()
    mes_inicio = hoy.replace(day=1).strftime("%Y-%m-%d")
    mes_fin = hoy.strftime("%Y-%m-%d")

    total_vehiculos = fetch_one("SELECT COUNT(*) AS c FROM vehiculos")["c"]
    en_ruta = fetch_one("SELECT COUNT(*) AS c FROM vehiculos WHERE estado = 'En ruta'")["c"]
    conductores_disp = fetch_one(
        "SELECT COUNT(*) AS c FROM conductores WHERE estado = 'Disponible' AND activo = 1"
    )["c"]
    viajes_mes = fetch_one(
        "SELECT COUNT(*) AS c FROM viajes WHERE fecha >= ? AND fecha <= ?",
        (mes_inicio, mes_fin),
    )["c"]

    return {
        "total_vehiculos": total_vehiculos,
        "vehiculos_en_ruta": en_ruta,
        "conductores_disponibles": conductores_disp,
        "viajes_mes": viajes_mes,
    }


def get_viajes_por_estado() -> list[sqlite3.Row]:
    return fetch_all("SELECT estado, COUNT(*) AS cantidad FROM viajes GROUP BY estado")


def get_vehiculos_por_estado() -> list[sqlite3.Row]:
    return fetch_all("SELECT estado, COUNT(*) AS cantidad FROM vehiculos GROUP BY estado")


def get_ultimos_viajes(limite: int = 5) -> list[sqlite3.Row]:
    return fetch_all(
        """SELECT v.*, ve.patente, c.nombre AS conductor_nombre
           FROM viajes v
           LEFT JOIN vehiculos ve ON v.vehiculo_id = ve.id
           LEFT JOIN conductores c ON v.conductor_id = c.id
           ORDER BY v.fecha DESC, v.id DESC LIMIT ?""",
        (limite,),
    )


def get_consumo_promedio_viajes() -> float | None:
    row = fetch_one(
        "SELECT AVG(consumo_kwh) AS promedio FROM viajes WHERE consumo_kwh IS NOT NULL"
    )
    return row["promedio"] if row and row["promedio"] is not None else None
