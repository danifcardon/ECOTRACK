from datetime import date

import streamlit as st

import database as db
from utils.helpers import ESTADOS_VIAJE, format_date, rows_to_dataframe
from utils.errors import ValidationError
from utils.validators import show_errors, validate_rango_fechas, validate_viaje_form

ESTADOS_NUEVO_VIAJE = ["Planificado", "En curso"]


def get_vehiculo_options() -> dict[str, int]:
    vehiculos = db.get_vehiculos_disponibles()
    return {f"{v['patente']} — {v['marca']} {v['modelo']}": v["id"] for v in vehiculos}


def get_conductor_options() -> dict[str, int]:
    conductores = db.get_conductores_disponibles()
    return {c["nombre"]: c["id"] for c in conductores}


def render_form_agregar() -> None:
    vehiculo_opts = get_vehiculo_options()
    conductor_opts = get_conductor_options()

    if not vehiculo_opts or not conductor_opts:
        st.warning("No hay vehículos o conductores disponibles para asignar un viaje.")
        return

    with st.form("form_agregar_viaje", clear_on_submit=True):
        st.subheader("Registrar nuevo viaje")
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha *", min_value=date.today(), value=date.today())
            origen = st.text_input("Origen *", placeholder="Buenos Aires - Palermo")
            destino = st.text_input("Destino *", placeholder="Buenos Aires - Belgrano")
        with col2:
            conductor_label = st.selectbox("Conductor *", list(conductor_opts.keys()))
            vehiculo_label = st.selectbox("Vehículo *", list(vehiculo_opts.keys()))
            estado = st.selectbox("Estado", ESTADOS_NUEVO_VIAJE, index=0)
        notas = st.text_area("Notas", max_chars=500)

        submitted = st.form_submit_button("Registrar viaje", type="primary")
        if submitted:
            errores = validate_viaje_form(
                fecha, origen, destino, estado, notas=notas, es_nuevo=True,
            )
            if errores:
                show_errors(errores)
                return
            try:
                db.insert_viaje({
                    "fecha": fecha.isoformat(),
                    "vehiculo_id": vehiculo_opts[vehiculo_label],
                    "conductor_id": conductor_opts[conductor_label],
                    "origen": origen,
                    "destino": destino,
                    "estado": estado,
                    "notas": notas.strip() or None,
                })
                st.success("Viaje registrado correctamente.")
                st.session_state["show_add_viaje"] = False
                st.rerun()
            except ValidationError as e:
                st.error(e.message)
            except Exception:
                st.error("No se pudo registrar el viaje.")


def render_completar(viaje: dict) -> None:
    if viaje["estado"] in ("Completado", "Cancelado"):
        return

    with st.form(f"form_completar_viaje_{viaje['id']}"):
        st.markdown("**Completar viaje**")
        km = st.number_input("Km recorridos *", min_value=0.1, max_value=2000.0, value=1.0, step=0.5)
        consumo = st.number_input("Consumo (kWh) *", min_value=0.1, max_value=500.0, value=1.0, step=0.1)
        submitted = st.form_submit_button("Marcar como completado", type="primary")

        if submitted:
            fecha_viaje = date.fromisoformat(viaje["fecha"]) if viaje.get("fecha") else date.today()
            errores = validate_viaje_form(
                fecha_viaje,
                viaje["origen"],
                viaje["destino"],
                "Completado",
                km_recorridos=km,
                consumo_kwh=consumo,
            )
            if errores:
                show_errors(errores)
                return
            try:
                db.update_viaje(viaje["id"], {
                    "fecha": viaje["fecha"],
                    "vehiculo_id": viaje["vehiculo_id"],
                    "conductor_id": viaje["conductor_id"],
                    "origen": viaje["origen"],
                    "destino": viaje["destino"],
                    "km_recorridos": km,
                    "estado": "Completado",
                    "consumo_kwh": consumo,
                    "notas": viaje.get("notas"),
                })
                st.success("Viaje completado. Km del vehículo actualizados.")
                st.rerun()
            except ValidationError as e:
                st.error(e.message)


def render_editar(viaje: dict) -> None:
    fecha_default = date.today()
    if viaje.get("fecha"):
        try:
            fecha_default = date.fromisoformat(viaje["fecha"])
        except ValueError:
            pass

    min_fecha = date.today() if viaje["estado"] in ("Planificado", "En curso") else date.today().replace(year=date.today().year - 1)

    with st.form(f"form_editar_viaje_{viaje['id']}"):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha", value=fecha_default, min_value=min_fecha, max_value=date.today())
            origen = st.text_input("Origen", value=viaje["origen"])
            destino = st.text_input("Destino", value=viaje["destino"])
        with col2:
            estado = st.selectbox(
                "Estado",
                ESTADOS_VIAJE,
                index=ESTADOS_VIAJE.index(viaje["estado"]) if viaje["estado"] in ESTADOS_VIAJE else 0,
            )
            km = st.number_input(
                "Km recorridos",
                value=float(viaje["km_recorridos"] or 0),
                min_value=0.0,
                max_value=2000.0,
            )
            consumo = st.number_input(
                "Consumo kWh",
                value=float(viaje["consumo_kwh"] or 0),
                min_value=0.0,
                max_value=500.0,
            )

        notas = st.text_area("Notas", value=viaje.get("notas") or "", max_chars=500)
        submitted = st.form_submit_button("Actualizar")

        if submitted:
            km_val = km if km > 0 else None
            consumo_val = consumo if consumo > 0 else None
            errores = validate_viaje_form(
                fecha, origen, destino, estado,
                km_recorridos=km_val, consumo_kwh=consumo_val, notas=notas,
            )
            if errores:
                show_errors(errores)
                return
            try:
                db.update_viaje(viaje["id"], {
                    "fecha": fecha.isoformat(),
                    "vehiculo_id": viaje["vehiculo_id"],
                    "conductor_id": viaje["conductor_id"],
                    "origen": origen,
                    "destino": destino,
                    "km_recorridos": km_val,
                    "estado": estado,
                    "consumo_kwh": consumo_val,
                    "notas": notas.strip() or None,
                })
                st.success("Viaje actualizado.")
                st.rerun()
            except ValidationError as e:
                st.error(e.message)


def render() -> None:
    st.title("Viajes")
    st.caption("Gestión de entregas y rutas · VerdeMov S.A.")

    promedio = db.get_consumo_promedio_viajes()
    if promedio is not None:
        st.metric("Consumo promedio por viaje", f"{promedio:.2f} kWh")

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        filtro_estado = st.selectbox("Filtrar por estado", ["Todos"] + ESTADOS_VIAJE)
    with col2:
        col_desde, col_hasta = st.columns(2)
        hoy = date.today()
        with col_desde:
            fecha_desde = st.date_input("Desde", value=hoy.replace(day=1), max_value=hoy)
        with col_hasta:
            fecha_hasta = st.date_input("Hasta", value=hoy, max_value=hoy)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Registrar viaje", use_container_width=True):
            st.session_state["show_add_viaje"] = not st.session_state.get("show_add_viaje", False)

    err_rango = validate_rango_fechas(fecha_desde, fecha_hasta)
    if err_rango:
        st.warning(err_rango)

    viajes = rows_to_dataframe(db.get_viajes(
        estado=filtro_estado if filtro_estado != "Todos" else None,
        fecha_desde=fecha_desde.isoformat() if fecha_desde and not err_rango else None,
        fecha_hasta=fecha_hasta.isoformat() if fecha_hasta and not err_rango else None,
    ))

    if viajes.empty:
        st.info("No hay viajes que coincidan con los filtros.")
        return

    display = viajes.copy()
    display["fecha"] = display["fecha"].apply(format_date)
    display = display[
        ["fecha", "patente", "conductor_nombre", "origen", "destino", "km_recorridos", "consumo_kwh", "estado"]
    ]
    display.columns = ["Fecha", "Patente", "Conductor", "Origen", "Destino", "Km", "kWh", "Estado"]
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Detalle de viajes")

    for _, row in viajes.iterrows():
        v = dict(row)
        with st.expander(f"{format_date(v['fecha'])} — {v['origen']} → {v['destino']} ({v['estado']})"):
            st.markdown(f"**Vehículo:** {v.get('patente', '—')} ({v.get('modelo', '')})")
            st.markdown(f"**Conductor:** {v.get('conductor_nombre', '—')}")
            st.markdown(f"**Km recorridos:** {v.get('km_recorridos') or '—'}")
            st.markdown(f"**Consumo:** {v.get('consumo_kwh') or '—'} kWh")
            if v.get("notas"):
                st.markdown(f"**Notas:** {v['notas']}")

            render_completar(v)
            render_editar(v)

            if st.button("Eliminar", key=f"del_viaje_{v['id']}"):
                try:
                    db.delete_viaje(v["id"])
                    st.success("Viaje eliminado.")
                    st.rerun()
                except ValidationError as e:
                    st.error(e.message)
