from datetime import date, timedelta

import streamlit as st

import database as db
from utils.helpers import (
    ESTADOS_VEHICULO,
    TIPOS_VEHICULO,
    battery_indicator,
    format_date,
    rows_to_dataframe,
)
from utils.errors import ValidationError
from utils.validators import normalize_patente, show_errors, validate_vehiculo_form

MIN_VENCIMIENTO = date.today() + timedelta(days=1)


def _parse_fecha(valor: str | None) -> date:
    if not valor:
        return MIN_VENCIMIENTO
    try:
        return date.fromisoformat(valor)
    except ValueError:
        return MIN_VENCIMIENTO


def render_form_agregar() -> None:
    with st.form("form_agregar_vehiculo", clear_on_submit=True):
        st.subheader("Agregar vehículo")
        col1, col2 = st.columns(2)
        with col1:
            patente = st.text_input("Patente *", placeholder="AB123CD")
            marca = st.text_input("Marca *")
            modelo = st.text_input("Modelo *")
            anio = st.number_input("Año", min_value=2000, max_value=date.today().year + 1, value=date.today().year)
            tipo = st.selectbox("Tipo", TIPOS_VEHICULO)
        with col2:
            estado = st.selectbox("Estado", ESTADOS_VEHICULO)
            nivel_bateria = st.slider("Nivel de batería (%)", 0, 100, 100)
            km_totales = st.number_input("Km totales", min_value=0, max_value=9_999_999, value=0)
            vtv = st.date_input("Vencimiento VTV", min_value=MIN_VENCIMIENTO, value=MIN_VENCIMIENTO)
            seguro = st.date_input("Vencimiento seguro", min_value=MIN_VENCIMIENTO, value=MIN_VENCIMIENTO)
        notas = st.text_area("Notas", max_chars=500)

        submitted = st.form_submit_button("Guardar", type="primary")
        if submitted:
            errores = validate_vehiculo_form(
                patente, marca, modelo, int(anio), tipo, estado,
                int(nivel_bateria), int(km_totales), vtv, seguro, notas,
            )
            if errores:
                show_errors(errores)
                return
            try:
                db.insert_vehiculo({
                    "patente": normalize_patente(patente),
                    "marca": marca,
                    "modelo": modelo,
                    "anio": int(anio),
                    "tipo": tipo,
                    "estado": estado,
                    "nivel_bateria": int(nivel_bateria),
                    "km_totales": int(km_totales),
                    "vencimiento_vtv": vtv.isoformat(),
                    "vencimiento_seguro": seguro.isoformat(),
                    "notas": notas.strip() or None,
                })
                st.success(f"Vehículo {normalize_patente(patente)} agregado.")
                st.session_state["show_add_vehiculo"] = False
                st.rerun()
            except ValidationError as e:
                st.error(e.message)
            except Exception:
                st.error("No se pudo agregar el vehículo.")


def render_editar(vehiculo: dict) -> None:
    vtv_default = max(_parse_fecha(vehiculo.get("vencimiento_vtv")), MIN_VENCIMIENTO)
    seguro_default = max(_parse_fecha(vehiculo.get("vencimiento_seguro")), MIN_VENCIMIENTO)

    with st.form(f"form_editar_vehiculo_{vehiculo['id']}"):
        col1, col2 = st.columns(2)
        with col1:
            patente = st.text_input("Patente", value=vehiculo["patente"])
            marca = st.text_input("Marca", value=vehiculo["marca"])
            modelo = st.text_input("Modelo", value=vehiculo["modelo"])
            anio = st.number_input(
                "Año", value=vehiculo["anio"] or date.today().year,
                min_value=2000, max_value=date.today().year + 1,
            )
            tipo = st.selectbox(
                "Tipo", TIPOS_VEHICULO,
                index=TIPOS_VEHICULO.index(vehiculo["tipo"]) if vehiculo["tipo"] in TIPOS_VEHICULO else 0,
            )
        with col2:
            estado = st.selectbox(
                "Estado", ESTADOS_VEHICULO,
                index=ESTADOS_VEHICULO.index(vehiculo["estado"]) if vehiculo["estado"] in ESTADOS_VEHICULO else 0,
            )
            nivel_bateria = st.slider("Batería (%)", 0, 100, int(vehiculo["nivel_bateria"] or 0))
            km_totales = st.number_input(
                "Km totales", value=int(vehiculo["km_totales"] or 0),
                min_value=0, max_value=9_999_999,
            )
            vtv = st.date_input("Vencimiento VTV", value=vtv_default, min_value=MIN_VENCIMIENTO)
            seguro = st.date_input("Vencimiento seguro", value=seguro_default, min_value=MIN_VENCIMIENTO)
            notas = st.text_area("Notas", value=vehiculo["notas"] or "", max_chars=500)

        submitted = st.form_submit_button("Actualizar")
        if submitted:
            errores = validate_vehiculo_form(
                patente, marca, modelo, int(anio), tipo, estado,
                int(nivel_bateria), int(km_totales), vtv, seguro, notas,
            )
            if errores:
                show_errors(errores)
                return
            try:
                db.update_vehiculo(vehiculo["id"], {
                    "patente": normalize_patente(patente),
                    "marca": marca,
                    "modelo": modelo,
                    "anio": int(anio),
                    "tipo": tipo,
                    "estado": estado,
                    "nivel_bateria": int(nivel_bateria),
                    "km_totales": int(km_totales),
                    "vencimiento_vtv": vtv.isoformat(),
                    "vencimiento_seguro": seguro.isoformat(),
                    "notas": notas.strip() or None,
                })
                st.success("Vehículo actualizado.")
                st.rerun()
            except ValidationError as e:
                st.error(e.message)
            except Exception:
                st.error("Error al actualizar el vehículo.")


def render() -> None:
    st.title("Vehículos")
    st.caption("Flota eléctrica · VerdeMov S.A.")

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        filtro_estado = st.selectbox("Filtrar por estado", ["Todos"] + ESTADOS_VEHICULO)
    with col2:
        filtro_tipo = st.selectbox("Filtrar por tipo", ["Todos"] + TIPOS_VEHICULO)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Agregar vehículo", use_container_width=True):
            st.session_state["show_add_vehiculo"] = not st.session_state.get("show_add_vehiculo", False)

    if st.session_state.get("show_add_vehiculo"):
        render_form_agregar()

    vehiculos = rows_to_dataframe(db.get_vehiculos(
        estado=filtro_estado if filtro_estado != "Todos" else None,
        tipo=filtro_tipo if filtro_tipo != "Todos" else None,
    ))

    if vehiculos.empty:
        st.info("No hay vehículos que coincidan con los filtros.")
        return

    display = vehiculos.copy()
    display["batería"] = display["nivel_bateria"].apply(lambda x: f"{x}%")
    display = display[["patente", "marca", "modelo", "tipo", "estado", "batería", "km_totales"]]
    display.columns = ["Patente", "Marca", "Modelo", "Tipo", "Estado", "Batería", "Km totales"]
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Detalle de vehículos")

    for _, row in vehiculos.iterrows():
        v = dict(row)
        with st.expander(f"{v['patente']} — {v['marca']} {v['modelo']}"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Tipo:** {v['tipo']}")
                st.markdown(f"**Estado:** {v['estado']}")
                st.markdown(f"**Año:** {v['anio']}")
                st.markdown(
                    f"**Batería:** {battery_indicator(int(v['nivel_bateria'] or 0))}",
                    unsafe_allow_html=True,
                )
            with col_b:
                st.markdown(f"**Km totales:** {v['km_totales']:,}")
                st.markdown(f"**VTV:** {format_date(v['vencimiento_vtv'])}")
                st.markdown(f"**Seguro:** {format_date(v['vencimiento_seguro'])}")
                if v.get("notas"):
                    st.markdown(f"**Notas:** {v['notas']}")

            st.progress(int(v["nivel_bateria"] or 0) / 100)

            render_editar(v)

            if st.button("Eliminar", key=f"del_veh_{v['id']}", type="secondary"):
                try:
                    db.delete_vehiculo(v["id"])
                    st.success("Vehículo eliminado.")
                    st.rerun()
                except ValidationError as e:
                    st.error(e.message)
