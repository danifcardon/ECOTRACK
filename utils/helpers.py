from datetime import date, datetime

import pandas as pd
import streamlit as st

from database import get_connection as _get_connection


def get_connection():
    return _get_connection()


def format_date(date_str: str | None) -> str:
    if not date_str:
        return "—"
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return date_str


def days_until(date_str: str | None) -> int | None:
    if not date_str:
        return None
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (target - datetime.now().date()).days
    except ValueError:
        return None


def battery_color(nivel: int) -> str:
    if nivel < 20:
        return "#E53935"
    if nivel < 50:
        return "#FDD835"
    return "#2E7D32"


def battery_indicator(nivel: int) -> str:
    color = battery_color(nivel)
    return f'<span style="color:{color}; font-weight:bold;">{nivel}%</span>'


def alert_vencimientos(df: pd.DataFrame, col_fecha: str, label: str, dias: int = 30) -> None:
    if df.empty or col_fecha not in df.columns:
        return
    for _, row in df.iterrows():
        fecha = row.get(col_fecha)
        if not fecha:
            continue
        dias_restantes = days_until(str(fecha))
        if dias_restantes is None:
            continue
        identificador = row.get("patente") or row.get("nombre") or row.get("dni") or "Registro"
        if dias_restantes < 0:
            st.warning(f"{label} vencido: {identificador} ({format_date(str(fecha))})")
        elif dias_restantes <= dias:
            st.warning(
                f"{label} por vencer en {dias_restantes} días: {identificador} ({format_date(str(fecha))})"
            )


def rows_to_dataframe(rows: list) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame([dict(row) for row in rows])


def clean_row(row) -> dict:
    data = row.to_dict() if hasattr(row, "to_dict") else dict(row)
    return {k: (None if pd.isna(v) else v) for k, v in data.items()}


def clamp_fecha(fecha: date, min_fecha: date, max_fecha: date) -> date:
    if fecha < min_fecha:
        return min_fecha
    if fecha > max_fecha:
        return max_fecha
    return fecha


from utils.constants import (
    ESTADOS_CONDUCTOR,
    ESTADOS_VEHICULO,
    ESTADOS_VIAJE,
    ROLES,
    TIPOS_VEHICULO,
)
