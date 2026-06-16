COLOR_PRIMARY = "#2E7D32"
COLOR_SECONDARY = "#66BB6A"
COLOR_ACCENT = "#A5D6A7"
COLOR_BG = "#F1F8E9"
COLOR_TEXT = "#1B1B1B"
COLOR_AMBER = "#F59E0B"
BORDER_RADIUS = "12px"
BORDER_RADIUS_LG = "16px"

CHART_COLORS = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, "#1565C0", COLOR_AMBER, "#B71C1C"]

ROLES = ["Administrador", "Operador", "Logística", "Mantenimiento", "Energía"]
TIPOS_VEHICULO = ["Furgón", "Moto", "Bicicleta eléctrica", "Van"]
ESTADOS_VEHICULO = ["Disponible", "En ruta", "En mantenimiento", "Fuera de servicio"]
ESTADOS_CONDUCTOR = ["Disponible", "En ruta", "Inactivo"]
ESTADOS_VIAJE = ["Planificado", "En curso", "Completado", "Cancelado"]
TURNOS_VIAJE = ["Mañana", "Tarde", "Noche", "Sin turno"]

SEDES = ["Buenos Aires", "Rosario", "Córdoba", "Otra"]

TIPOS_MANTENIMIENTO = ["Preventivo", "Correctivo"]
ESTADOS_MANTENIMIENTO = ["Programado", "En curso", "Completado", "Cancelado"]

TIPOS_DOCUMENTO = [
    "VTV",
    "Seguro",
    "Habilitación municipal",
    "Habilitación provincial",
    "Revisión técnica",
    "Certificado de origen",
    "Permiso de circulación",
    "Licencia de conducir",
    "Otro",
]
ENTIDADES_DOCUMENTO = ["Vehículo", "Conductor"]

MODULOS_POR_ROL: dict[str, list[str]] = {
    "Administrador": ["dashboard", "vehiculos", "conductores", "viajes", "mantenimiento", "documentacion", "reportes", "usuarios"],
    "Operador":      ["dashboard", "vehiculos", "conductores", "viajes", "mantenimiento", "reportes"],
    "Logística":     ["dashboard", "vehiculos", "conductores", "viajes", "reportes"],
    "Mantenimiento": ["dashboard", "vehiculos", "mantenimiento", "documentacion", "reportes"],
    "Energía":       ["dashboard", "vehiculos", "viajes", "reportes"],
}
