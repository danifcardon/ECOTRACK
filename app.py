import streamlit as st

from database import init_db
from pages import conductores, dashboard, usuarios, vehiculos, viajes

st.set_page_config(
    page_title="EcoTrack · VerdeMov",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

BRAND_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp {
        background-color: #F1F8E9;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] h5,
    [data-testid="stAppViewContainer"] h6,
    [data-testid="stAppViewContainer"] .stMarkdown,
    [data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] {
        color: #1B1B1B !important;
    }

    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3 {
        color: #2E7D32 !important;
    }

    [data-testid="stAppViewContainer"] input {
        color: #1B1B1B !important;
        background-color: #FFFFFF !important;
        border: 1px solid #A5D6A7 !important;
    }

    [data-testid="stAppViewContainer"] button[data-testid="baseButton-primary"],
    [data-testid="stAppViewContainer"] .stFormSubmitButton button {
        background-color: #2E7D32 !important;
        border-color: #2E7D32 !important;
        color: #FFFFFF !important;
    }

    [data-testid="stAppViewContainer"] button[data-testid="baseButton-primary"]:hover,
    [data-testid="stAppViewContainer"] .stFormSubmitButton button:hover {
        background-color: #1B5E20 !important;
        border-color: #1B5E20 !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2E7D32 0%, #1B5E20 100%);
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #A5D6A7 !important;
    }

    .brand-logo {
        font-size: 1.6rem;
        font-weight: 700;
        color: #FFFFFF !important;
        padding: 0.5rem 0 1rem 0;
        border-bottom: 2px solid #66BB6A;
        margin-bottom: 1rem;
    }

    .brand-subtitle {
        font-size: 0.85rem;
        color: #A5D6A7 !important;
        margin-top: -0.5rem;
        margin-bottom: 1.5rem;
    }

    .user-badge {
        background-color: rgba(255,255,255,0.15);
        border-radius: 8px;
        padding: 0.75rem;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
        color: #FFFFFF !important;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #A5D6A7;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(46, 125, 50, 0.08);
    }

    div[data-testid="stMetric"] label {
        color: #2E7D32 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #1B1B1B !important;
    }

    .login-wrapper {
        max-width: 440px;
        margin: 3rem auto 0 auto;
        padding: 2.5rem;
        background: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #A5D6A7;
        box-shadow: 0 4px 24px rgba(46, 125, 50, 0.12);
    }

    .login-title {
        text-align: center;
        color: #2E7D32 !important;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .login-subtitle {
        text-align: center;
        color: #2E7D32 !important;
        opacity: 0.75;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    .login-heading {
        color: #1B1B1B !important;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .stExpander {
        background-color: #FFFFFF;
        border: 1px solid #A5D6A7;
        border-radius: 8px;
    }
</style>
"""

LOGIN_CSS = """
<style>
    section[data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="stAppViewBlockContainer"] {
        max-width: 520px;
        padding-top: 2rem;
    }
</style>
"""

PAGINAS = {
    "Dashboard": dashboard.render,
    "Usuarios": usuarios.render,
    "Vehículos": vehiculos.render,
    "Conductores": conductores.render,
    "Viajes": viajes.render,
}


def render_login() -> None:
    st.markdown(BRAND_CSS + LOGIN_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="login-wrapper">
            <div class="login-title">🌿 EcoTrack</div>
            <div class="login-subtitle">VerdeMov S.A. · Logística eléctrica sustentable</div>
            <div class="login-heading">Iniciar sesión</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Ingresar", type="primary", use_container_width=True)

        if submitted:
            if usuario == "admin" and password == "ecotrack2025":
                st.session_state["logged_in"] = True
                st.session_state["usuario"] = "Administrador"
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")


def render_sidebar() -> str:
    st.sidebar.markdown('<div class="brand-logo">🌿 EcoTrack</div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        '<div class="brand-subtitle">VerdeMov S.A.</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        f'<div class="user-badge">👤 {st.session_state.get("usuario", "Usuario")}</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")
    pagina = st.sidebar.radio("Navegación", list(PAGINAS.keys()), label_visibility="collapsed")
    st.sidebar.markdown("---")
    st.sidebar.caption("Movilidad 100% eléctrica")
    if st.sidebar.button("Cerrar sesión", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    return pagina


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
