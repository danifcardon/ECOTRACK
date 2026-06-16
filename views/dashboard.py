import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import database as db
from ecotrack_utils.constants import CHART_COLORS, COLOR_BG
from ecotrack_utils.helpers import alert_vencimientos, format_date, rows_to_dataframe


def render_alertas() -> None:
    vehiculos = rows_to_dataframe(db.get_vehiculos())
    conductores = rows_to_dataframe(db.get_conductores())

    st.subheader("Alertas operativas")

    if not vehiculos.empty:
        bateria_baja = vehiculos[vehiculos["nivel_bateria"] < 20]
        for _, v in bateria_baja.iterrows():
            st.warning(
                f"Batería baja ({v['nivel_bateria']}%): {v['patente']} — {v['marca']} {v['modelo']}"
            )

        alert_vencimientos(vehiculos, "vencimiento_vtv", "VTV")
        alert_vencimientos(vehiculos, "vencimiento_seguro", "Seguro")

    if not conductores.empty:
        alert_vencimientos(conductores, "vencimiento_licencia", "Licencia de conducir")

    if vehiculos.empty or (
        vehiculos[vehiculos["nivel_bateria"] < 20].empty
        and all(
            len(vehiculos[vehiculos[col].notna()]) == 0
            for col in ["vencimiento_vtv", "vencimiento_seguro"]
        )
    ):
        st.info("No hay alertas críticas en este momento.")


def render() -> None:
    st.title("Dashboard")
    st.caption("Panel de control · VerdeMov S.A.")

    kpis = db.get_dashboard_kpis()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total vehículos", kpis["total_vehiculos"])
    col2.metric("Vehículos en ruta", kpis["vehiculos_en_ruta"])
    col3.metric("Conductores disponibles", kpis["conductores_disponibles"])
    col4.metric("Viajes del mes", kpis["viajes_mes"])

    st.markdown("---")

    col_graf1, col_graf2 = st.columns(2)

    viajes_estado = rows_to_dataframe(db.get_viajes_por_estado())
    with col_graf1:
        st.subheader("Viajes por estado")
        if viajes_estado.empty:
            st.info("Sin datos de viajes.")
        else:
            fig = px.bar(
                viajes_estado,
                x="estado",
                y="cantidad",
                color="estado",
                color_discrete_sequence=CHART_COLORS,
                labels={"estado": "Estado", "cantidad": "Cantidad"},
            )
            fig.update_layout(showlegend=False, plot_bgcolor=COLOR_BG, paper_bgcolor=COLOR_BG)
            st.plotly_chart(fig, use_container_width=True)

    vehiculos_estado = rows_to_dataframe(db.get_vehiculos_por_estado())
    with col_graf2:
        st.subheader("Vehículos por estado")
        if vehiculos_estado.empty:
            st.info("Sin datos de vehículos.")
        else:
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=vehiculos_estado["estado"],
                        values=vehiculos_estado["cantidad"],
                        marker_colors=CHART_COLORS[: len(vehiculos_estado)],
                        hole=0.4,
                    )
                ]
            )
            fig.update_layout(plot_bgcolor=COLOR_BG, paper_bgcolor=COLOR_BG)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Últimos viajes registrados")

    ultimos = rows_to_dataframe(db.get_ultimos_viajes(5))
    if ultimos.empty:
        st.info("No hay viajes registrados.")
    else:
        display = ultimos[["fecha", "patente", "conductor_nombre", "origen", "destino", "estado", "km_recorridos"]].copy()
        display["fecha"] = display["fecha"].apply(format_date)
        display.columns = ["Fecha", "Patente", "Conductor", "Origen", "Destino", "Estado", "Km"]
        st.dataframe(display, use_container_width=True, hide_index=True)

    st.markdown("---")
    render_alertas()
