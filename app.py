import streamlit as st

from database import init_db
from ecotrack_utils.constants import COLOR_TEXT
from ecotrack_utils.theme import build_brand_css, build_login_css
from views import conductores, dashboard, usuarios, vehiculos, viajes

# ========================================================
# 1. CONFIGURACIÓN DE LA PÁGINA (Única y global al inicio)
# ========================================================
st.set_page_config(
    page_title="EcoTrack · VerdeMov",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========================================================
# 2. INYECCIÓN DE CSS (paleta EcoTrack centralizada en ecotrack_utils/theme.py)
# ========================================================
BRAND_CSS = build_brand_css()
LOGIN_CSS = build_login_css()

# Módulos de navegación (clave interna → función render)
PAGINAS = {
    "dashboard": dashboard.render,
    "usuarios": usuarios.render,
    "vehiculos": vehiculos.render,
    "conductores": conductores.render,
    "viajes": viajes.render,
}

MENU_ITEMS = [
    ("dashboard", "Dashboard"),
    ("usuarios", "Usuarios"),
    ("vehiculos", "Vehículos"),
    ("conductores", "Conductores"),
    ("viajes", "Viajes"),
]


def _credenciales_validas(usuario: str, password: str) -> tuple[bool, str]:
    try:
        user_ok = st.secrets["auth"]["username"]
        pass_ok = st.secrets["auth"]["password"]
        display = st.secrets["auth"].get("display_name", "Administrador")
    except (KeyError, FileNotFoundError, AttributeError):
        user_ok = "admin"
        pass_ok = "admin"
        display = "Administrador"

    if usuario == user_ok and password == pass_ok:
        return True, display
    return False, ""


# ========================================================
# 4. COMPONENTE: RENDEREADO DEL LOGIN
# ========================================================
def render_login() -> None:
    st.markdown(BRAND_CSS + LOGIN_CSS, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem; padding: 0 0.5rem;">
            <h1 style="color: {COLOR_TEXT}; font-weight: 700; margin-bottom: 0; font-size: 2.3rem;">🌱 EcoTrack</h1>
            <p style="color: {COLOR_TEXT}; opacity: 0.7; margin-top: 0.5rem; font-size: 0.9rem; letter-spacing: 0.5px;">
                VerdeMov S.A. &middot; Logística sustentable
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.form(key="login_form"):
        st.markdown(
            f"<h2 style='margin-top:0; font-size:1.4rem; font-weight:700; color:{COLOR_TEXT};'>Iniciar sesión</h2>",
            unsafe_allow_html=True,
        )

        usuario = st.text_input("Usuario", placeholder="Introduce tu usuario")
        password = st.text_input("Contraseña", type="password", placeholder="••••••••")

        submitted = st.form_submit_button("Ingresar al Sistema", use_container_width=True)

        if submitted:
            usuario_limpio = (usuario or "").strip()
            password_limpia = (password or "").strip()

            if not usuario_limpio or not password_limpia:
                st.error("Usuario y contraseña son obligatorios.")
                return
            if len(usuario_limpio) > 50 or len(password_limpia) > 100:
                st.error("Usuario o contraseña demasiado largos.")
                return

            valido, nombre_display = _credenciales_validas(usuario_limpio, password_limpia)
            if valido:
                st.session_state["logged_in"] = True
                st.session_state["usuario"] = nombre_display
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

    st.markdown("""
        <div style="display: flex; justify-content: space-between; padding: 0 12px; font-size: 0.85rem; margin-top: 0.5rem;">
            <a href="#" class="login-link-muted">¿Olvidé mi contraseña?</a>
            <a href="#" class="login-link-primary">Crear una cuenta</a>
        </div>
        <div class="custom-footer">
            © 2026 VerdeMov S.A. | Todos los derechos reservados | Versión 2.0.1
        </div>
    """, unsafe_allow_html=True)


# ========================================================
# 5. COMPONENTE: RENDERIZADO DE LA BARRA LATERAL (POST-LOGIN)
# ========================================================
def render_sidebar() -> str:
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "dashboard"

    st.sidebar.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon" aria-hidden="true">
                <span class="material-symbols-outlined">eco</span>
            </div>
            <div class="sidebar-brand-text">
                <span class="sidebar-brand-name">EcoTrack</span>
                <span class="sidebar-brand-subtitle">Panel administrador</span>
            </div>
        </div>
        <div class="sidebar-divider"></div>
    """, unsafe_allow_html=True)

    for page_id, label in MENU_ITEMS:
        is_active = st.session_state.nav_page == page_id
        if st.sidebar.button(
            label,
            key=f"nav_{page_id}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.nav_page = page_id
            st.rerun()

    st.sidebar.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)

    if st.sidebar.button("Cerrar sesión", key="btn_logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    return st.session_state.nav_page


# ========================================================
# 6. CONTROLADOR PRINCIPAL DE LA APLICACIÓN
# ========================================================
def main() -> None:
    init_db()

    if not st.session_state.get("logged_in"):
        render_login()
        return

    st.markdown(BRAND_CSS, unsafe_allow_html=True)
    pagina = render_sidebar()
    PAGINAS[pagina]()


if __name__ == "__main__":
    main()
