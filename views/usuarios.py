import streamlit as st

import database as db
from ecotrack_utils.helpers import ROLES, format_date, rows_to_dataframe
from ecotrack_utils.errors import ValidationError
from ecotrack_utils.validators import show_errors, validate_usuario_form


def render_form_agregar() -> None:
    with st.form("form_agregar_usuario", clear_on_submit=True):
        st.subheader("Agregar usuario")
        nombre = st.text_input("Nombre completo *")
        email = st.text_input("Email *")
        rol = st.selectbox("Rol *", ROLES)
        submitted = st.form_submit_button("Guardar", type="primary")

        if submitted:
            errores = validate_usuario_form(nombre, email, rol)
            if errores:
                show_errors(errores)
                return
            try:
                db.insert_usuario(nombre, email, rol)
                st.success(f"Usuario '{nombre.strip()}' creado correctamente.")
                st.session_state["show_add_usuario"] = False
                st.rerun()
            except ValidationError as e:
                st.error(e.message)
            except Exception:
                st.error("No se pudo crear el usuario. Intentá nuevamente.")


def render_editar(usuario: dict) -> None:
    with st.form(f"form_editar_usuario_{usuario['id']}"):
        nombre = st.text_input("Nombre", value=usuario["nombre"])
        email = st.text_input("Email", value=usuario["email"])
        rol = st.selectbox("Rol", ROLES, index=ROLES.index(usuario["rol"]) if usuario["rol"] in ROLES else 0)
        submitted = st.form_submit_button("Actualizar")

        if submitted:
            errores = validate_usuario_form(nombre, email, rol)
            if errores:
                show_errors(errores)
                return
            try:
                db.update_usuario(usuario["id"], nombre, email, rol)
                st.success("Usuario actualizado.")
                st.rerun()
            except ValidationError as e:
                st.error(e.message)
            except Exception:
                st.error("Error al actualizar el usuario.")


def render() -> None:
    st.title("Usuarios del sistema")
    st.caption("Gestión de accesos y roles · VerdeMov S.A.")

    if st.button("➕ Agregar usuario"):
        st.session_state["show_add_usuario"] = not st.session_state.get("show_add_usuario", False)

    if st.session_state.get("show_add_usuario"):
        render_form_agregar()

    usuarios = rows_to_dataframe(db.get_usuarios())
    if usuarios.empty:
        st.info("No hay usuarios registrados.")
        return

    display = usuarios[["id", "nombre", "email", "rol", "activo", "fecha_creacion"]].copy()
    display["activo"] = display["activo"].apply(lambda x: "Activo" if x == 1 else "Inactivo")
    display["fecha_creacion"] = display["fecha_creacion"].apply(format_date)
    display.columns = ["ID", "Nombre", "Email", "Rol", "Estado", "Fecha creación"]
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Detalle y edición")

    for _, row in usuarios.iterrows():
        usuario = dict(row)
        estado_label = "Activo" if usuario["activo"] == 1 else "Inactivo"
        with st.expander(f"{usuario['nombre']} — {usuario['rol']} ({estado_label})"):
            st.markdown(f"**Email:** {usuario['email']}")
            st.markdown(f"**Fecha de creación:** {format_date(usuario['fecha_creacion'])}")
            render_editar(usuario)

            col1, col2 = st.columns(2)
            with col1:
                if usuario["activo"] == 1:
                    if st.button("Desactivar", key=f"desact_{usuario['id']}"):
                        try:
                            db.desactivar_usuario(usuario["id"])
                            st.success("Usuario desactivado.")
                            st.rerun()
                        except ValidationError as e:
                            st.error(e.message)
                else:
                    if st.button("Reactivar", key=f"react_{usuario['id']}"):
                        try:
                            db.activar_usuario(usuario["id"])
                            st.success("Usuario reactivado.")
                            st.rerun()
                        except ValidationError as e:
                            st.error(e.message)
