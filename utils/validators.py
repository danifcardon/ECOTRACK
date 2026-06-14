import re
from datetime import date, datetime

from utils.constants import (
    ESTADOS_CONDUCTOR,
    ESTADOS_VEHICULO,
    ESTADOS_VIAJE,
    ROLES,
    TIPOS_VEHICULO,
)
from utils.errors import ValidationError

MAX_TEXTO = 200
MAX_NOTAS = 500
MAX_KM_VIAJE = 2000
MAX_KM_TOTALES = 9_999_999
MAX_CONSUMO_KWH = 500

PATENTE_REGEX = re.compile(r"^[A-Z]{2}\d{3}[A-Z]{2}$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
NOMBRE_REGEX = re.compile(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s'.-]{2,100}$")
DNI_REGEX = re.compile(r"^\d{7,8}$")
TELEFONO_REGEX = re.compile(r"^[\d\s\-+()]{6,20}$")


def _hoy() -> date:
    return date.today()


def validate_required_text(valor: str | None, campo: str, min_len: int = 1, max_len: int = MAX_TEXTO) -> str | None:
    if valor is None or not str(valor).strip():
        return f"{campo} es obligatorio."
    texto = str(valor).strip()
    if len(texto) < min_len:
        return f"{campo} debe tener al menos {min_len} caracteres."
    if len(texto) > max_len:
        return f"{campo} no puede superar {max_len} caracteres."
    return None


def validate_nombre(nombre: str) -> str | None:
    err = validate_required_text(nombre, "El nombre", min_len=2, max_len=100)
    if err:
        return err
    if not NOMBRE_REGEX.match(nombre.strip()):
        return "El nombre solo puede contener letras, espacios y caracteres válidos."
    return None


def validate_email(email: str) -> str | None:
    err = validate_required_text(email, "El email", min_len=5, max_len=120)
    if err:
        return err
    if not EMAIL_REGEX.match(email.strip().lower()):
        return "El formato del email no es válido."
    return None


def validate_rol(rol: str) -> str | None:
    if rol not in ROLES:
        return "El rol seleccionado no es válido."
    return None


def validate_patente(patente: str) -> str | None:
    err = validate_required_text(patente, "La patente", min_len=6, max_len=10)
    if err:
        return err
    normalizada = patente.strip().upper().replace(" ", "")
    if not PATENTE_REGEX.match(normalizada):
        return "La patente debe tener formato argentino: AB123CD (2 letras, 3 números, 2 letras)."
    return None


def normalize_patente(patente: str) -> str:
    return patente.strip().upper().replace(" ", "")


def validate_marca_modelo(valor: str, campo: str) -> str | None:
    err = validate_required_text(valor, campo, min_len=2, max_len=80)
    if err:
        return err
    if valor.strip().isdigit():
        return f"{campo} no puede ser solo números."
    return None


def validate_anio(anio: int) -> str | None:
    actual = _hoy().year
    if anio < 2000 or anio > actual + 1:
        return f"El año debe estar entre 2000 y {actual + 1}."
    return None


def validate_tipo_vehiculo(tipo: str) -> str | None:
    if tipo not in TIPOS_VEHICULO:
        return "El tipo de vehículo no es válido."
    return None


def validate_estado_vehiculo(estado: str) -> str | None:
    if estado not in ESTADOS_VEHICULO:
        return "El estado del vehículo no es válido."
    return None


def validate_nivel_bateria(nivel: int) -> str | None:
    if not isinstance(nivel, int) or nivel < 0 or nivel > 100:
        return "El nivel de batería debe estar entre 0 y 100."
    return None


def validate_km_totales(km: int) -> str | None:
    if km < 0 or km > MAX_KM_TOTALES:
        return f"Los km totales deben estar entre 0 y {MAX_KM_TOTALES:,}."
    return None


def validate_fecha_vencimiento(fecha: date, campo: str) -> str | None:
    if fecha <= _hoy():
        return f"{campo} debe ser posterior a hoy ({_hoy().strftime('%d/%m/%Y')})."
    return None


def validate_notas(notas: str | None) -> str | None:
    if notas and len(notas.strip()) > MAX_NOTAS:
        return f"Las notas no pueden superar {MAX_NOTAS} caracteres."
    return None


def validate_dni(dni: str) -> str | None:
    err = validate_required_text(dni, "El DNI", min_len=7, max_len=8)
    if err:
        return err
    limpio = dni.strip().replace(".", "").replace(" ", "")
    if not DNI_REGEX.match(limpio):
        return "El DNI debe tener 7 u 8 dígitos numéricos."
    return None


def normalize_dni(dni: str) -> str:
    return dni.strip().replace(".", "").replace(" ", "")


def validate_telefono(telefono: str | None) -> str | None:
    if not telefono or not telefono.strip():
        return None
    if not TELEFONO_REGEX.match(telefono.strip()):
        return "El teléfono tiene un formato inválido."
    return None


def validate_licencia(licencia: str | None) -> str | None:
    if not licencia or not licencia.strip():
        return None
    if len(licencia.strip()) < 5 or len(licencia.strip()) > 20:
        return "El número de licencia debe tener entre 5 y 20 caracteres."
    return None


def validate_estado_conductor(estado: str) -> str | None:
    if estado not in ESTADOS_CONDUCTOR:
        return "El estado del conductor no es válido."
    return None


def validate_fecha_viaje(fecha: date, estado: str, es_nuevo: bool = False) -> str | None:
    hoy = _hoy()
    if estado in ("Planificado", "En curso"):
        if fecha < hoy:
            return "La fecha del viaje no puede ser anterior a hoy para viajes planificados o en curso."
    if estado == "Completado":
        if fecha > hoy:
            return "Un viaje completado no puede tener fecha futura."
        if (hoy - fecha).days > 365:
            return "La fecha del viaje completado no puede ser mayor a un año de antigüedad."
    if es_nuevo and fecha < hoy:
        return "No se pueden registrar viajes con fecha anterior a hoy."
    return None


def validate_origen_destino(origen: str, destino: str) -> str | None:
    err_o = validate_required_text(origen, "El origen", min_len=3, max_len=MAX_TEXTO)
    if err_o:
        return err_o
    err_d = validate_required_text(destino, "El destino", min_len=3, max_len=MAX_TEXTO)
    if err_d:
        return err_d
    if origen.strip().lower() == destino.strip().lower():
        return "El origen y el destino deben ser diferentes."
    return None


def validate_km_viaje(km: float | None, estado: str, requerido: bool = False) -> str | None:
    if estado == "Completado" or requerido:
        if km is None or km <= 0:
            return "Los km recorridos deben ser mayores a 0."
        if km > MAX_KM_VIAJE:
            return f"Los km recorridos no pueden superar {MAX_KM_VIAJE}."
    elif km is not None and km < 0:
        return "Los km recorridos no pueden ser negativos."
    return None


def validate_consumo(consumo: float | None, estado: str) -> str | None:
    if estado == "Completado":
        if consumo is None or consumo <= 0:
            return "El consumo en kWh es obligatorio y debe ser mayor a 0 para viajes completados."
        if consumo > MAX_CONSUMO_KWH:
            return f"El consumo no puede superar {MAX_CONSUMO_KWH} kWh."
    elif consumo is not None and consumo < 0:
        return "El consumo no puede ser negativo."
    return None


def validate_estado_viaje(estado: str) -> str | None:
    if estado not in ESTADOS_VIAJE:
        return "El estado del viaje no es válido."
    return None


def validate_rango_fechas(desde: date, hasta: date) -> str | None:
    if desde > hasta:
        return "La fecha 'Desde' no puede ser posterior a la fecha 'Hasta'."
    if hasta > _hoy():
        return "La fecha 'Hasta' no puede ser futura."
    return None


def collect_errors(*errores: str | None) -> list[str]:
    return [e for e in errores if e]


def validate_usuario_form(nombre: str, email: str, rol: str) -> list[str]:
    return collect_errors(
        validate_nombre(nombre),
        validate_email(email),
        validate_rol(rol),
    )


def validate_vehiculo_form(
    patente: str,
    marca: str,
    modelo: str,
    anio: int,
    tipo: str,
    estado: str,
    nivel_bateria: int,
    km_totales: int,
    vencimiento_vtv: date,
    vencimiento_seguro: date,
    notas: str | None,
) -> list[str]:
    return collect_errors(
        validate_patente(patente),
        validate_marca_modelo(marca, "La marca"),
        validate_marca_modelo(modelo, "El modelo"),
        validate_anio(int(anio)),
        validate_tipo_vehiculo(tipo),
        validate_estado_vehiculo(estado),
        validate_nivel_bateria(int(nivel_bateria)),
        validate_km_totales(int(km_totales)),
        validate_fecha_vencimiento(vencimiento_vtv, "El vencimiento de VTV"),
        validate_fecha_vencimiento(vencimiento_seguro, "El vencimiento del seguro"),
        validate_notas(notas),
    )


def validate_conductor_form(
    nombre: str,
    dni: str,
    telefono: str | None,
    licencia: str | None,
    vencimiento_licencia: date,
    estado: str,
) -> list[str]:
    errores = collect_errors(
        validate_nombre(nombre),
        validate_dni(dni),
        validate_telefono(telefono),
        validate_licencia(licencia),
        validate_fecha_vencimiento(vencimiento_licencia, "El vencimiento de la licencia"),
        validate_estado_conductor(estado),
    )
    if not licencia or not licencia.strip():
        errores.append("El número de licencia es obligatorio.")
    return errores


def validate_viaje_form(
    fecha: date,
    origen: str,
    destino: str,
    estado: str,
    km_recorridos: float | None = None,
    consumo_kwh: float | None = None,
    notas: str | None = None,
    es_nuevo: bool = False,
) -> list[str]:
    return collect_errors(
        validate_fecha_viaje(fecha, estado, es_nuevo=es_nuevo),
        validate_origen_destino(origen, destino),
        validate_estado_viaje(estado),
        validate_km_viaje(km_recorridos, estado),
        validate_consumo(consumo_kwh, estado),
        validate_notas(notas),
    )


def show_errors(errores: list[str]) -> None:
    import streamlit as st

    for error in errores:
        st.error(error)
