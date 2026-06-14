from datetime import date, timedelta

import streamlit as st

import database as db
from utils.helpers import ESTADOS_CONDUCTOR, alert_vencimientos, days_until, format_date, rows_to_dataframe
from utils.errors import ValidationError
from utils.validators import show_errors, validate_conductor_form

MIN_VENCIMIENTO = date.today() + timedelta(days=1)


def render_form_agregar() -> None:
    with st.form("form_agregar_conductor", clear_on_submit=True):
        st.subheader("Agregar conductor")
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo *")
            dni = st.text_input("DNI *", placeholder="30123456")
            telefono = st.text_input("Teléfono", placeholder="11-4444-5555")
        with col2:
            licencia = st.text_input("N° de licencia *")
            vencimiento = st.date_input(
                "Vencimiento licencia *",
                min_value=MIN_VENCIMIENTO,
                value=date.today() + timedelta(days=365),
            )
            estado = st.selectbox("Estado", ESTADOS_CONDUCTOR, index=0)

        submitted = st.form_submit_button("Guardar", type="primary")
        if submitted:
            errores = validate_conductor_form(nombre, dni, telefono, licencia, vencimiento, estado)
            if errores:
                show_errors(errores)
                return
            try:
                db.insert_conductor({
                    "nombre": nombre,
                    "dni": dni,
                    "telefono": telefono.strip() or None,
                    "licencia": licencia.strip(),
                    "vencimiento_licencia": vencimiento.isoformat(),
                    "estado": estado,
                })
                st.success(f"Conductor '{nombre.strip()}' agregado.")
                st.session_state["show_add_conductor"] = False
                st.rerun()
            except ValidationError as e:
                st.error(e.message)
            except Exception:
                st.error("No se pudo agregar el conductor.")


def render_editar(conductor: dict) -> None:
    venc_default = MIN_VENCIMIENTO
    if conductor.get("vencimiento_licencia"):
        try:
            venc_default = max(date.fromisoformat(conductor["vencimiento_licencia"]), MIN_VENCIMIENTO)
        except ValueError:
            pass

    with st.form(f"form_editar_conductor_{conductor['id']}"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre", value=conductor["nombre"])
            dni = st.text_input("DNI", value=conductor["dni"])
            telefono = st.text_input("Teléfono", value=conductor["telefono"] or "")
        with col2:
            licencia = st.text_input("Licencia", value=conductor["licencia"] or "")
            vencimiento = st.date_input("Vencimiento licencia", value=venc_default, min_value=MIN_VENCIMIENTO)
            estado = st.selectbox(
                "Estado",
                ESTADOS_CONDUCTOR,
                index=ESTADOS_CONDUCTOR.index(conductor["estado"]) if conductor["estado"] in ESTADOS_CONDUCTOR else 0,
            )
            activo = st.checkbox("Activo", value=conductor["activo"] == 1)

        submitted = st.form_submit_button("Actualizar")
        if submitted:
            errores = validate_conductor_form(nombre, dni, telefono, licencia, vencimiento, estado)
            if errores:
                show_errors(errores)
                return
            if not activo and estado in ("Disponible", "En ruta"):
                st.error("Un conductor inactivo no puede estar Disponible o En ruta.")
                return
            try:
                db.update_conductor(conductor["id"], {
                    "nombre": nombre,
                    "dni": dni,
                    "telefono": telefono.strip() or None,
                    "licencia": licencia.strip(),
                    "vencimiento_licencia": vencimiento.isoformat(),
                    "estado": estado,
                    "activo": 1 if activo else 0,
                })
                st.success("Conductor actualizado.")
                st.rerun()
            except ValidationError as e:
                st.error(e.message)
            except Exception:
                st.error("Error al actualizar el conductor.")


def render() -> None:
    st.title("Conductores")
    st.caption("Gestión de conductores · VerdeMov S.A.")

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        filtro_estado = st.selectbox("Filtrar por estado", ["Todos"] + ESTADOS_CONDUCTOR)
    with col2:
        filtro_activo = st.selectbox("Filtrar por condición", ["Todos", "Activos", "Inactivos"])
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Agregar conductor", use_container_width=True):
            st.session_state["show_add_conductor"] = not st.session_state.get("show_add_conductor", False)

    if st.session_state.get("show_add_conductor"):
        render_form_agregar()

    conductores = rows_to_dataframe(db.get_conductores(
        estado=filtro_estado if filtro_estado != "Todos" else None,
        activo=filtro_activo if filtro_activo != "Todos" else None,
    ))

    alert_vencimientos(conductores, "vencimiento_licencia", "Licencia de conductor")

    if conductores.empty:
        st.info("No hay conductores que coincidan con los filtros.")
        return

    display = conductores.copy()
    display["activo"] = display["activo"].apply(lambda x: "Sí" if x == 1 else "No")
    display["vencimiento_licencia"] = display["vencimiento_licencia"].apply(format_date)
    display = display[["nombre", "dni", "telefono", "licencia", "vencimiento_licencia", "estado", "activo"]]
    display.columns = ["Nombre", "DNI", "Teléfono", "Licencia", "Venc. licencia", "Estado", "Activo"]
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Detalle de conductores")

    for _, row in conductores.iterrows():
        c = dict(row)
        dias = days_until(c.get("vencimiento_licencia"))
        alerta = ""
        if dias is not None and dias <= 30:
            alerta = " ⚠️"
        with st.expander(f"{c['nombre']} — DNI {c['dni']}{alerta}"):
            if dias is not None and dias <= 30:
                if dias < 0:
                    st.warning(f"Licencia vencida desde el {format_date(c['vencimiento_licencia'])}")
                else:
                    st.warning(f"Licencia vence en {dias} días ({format_date(c['vencimiento_licencia'])})")

            st.markdown(f"**Teléfono:** {c.get('telefono') or '—'}")
            st.markdown(f"**Licencia:** {c.get('licencia') or '—'}")
            st.markdown(f"**Estado:** {c['estado']}")
            st.markdown(f"**Activo:** {'Sí' if c['activo'] == 1 else 'No'}")

            render_editar(c)

            if st.button("Eliminar", key=f"del_cond_{c['id']}"):
                try:
                    db.delete_conductor(c["id"])
                    st.success("Conductor eliminado.")
                    st.rerun()
                except ValidationError as e:
                    st.error(e.message)
