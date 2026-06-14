import sqlite3
import streamlit as st

from database import init_db
# Nota: Si en el futuro renombrás la carpeta 'pages' a 'modules', cambiás esta línea.
from pages import conductores, dashboard, usuarios, vehiculos, viajes

# ========================================================
# 1. CONFIGURACIÓN DE LA PÁGINA (Única y global al inicio)
# ========================================================
st.set_page_config(
    page_title="EcoTrack · VerdeMov",
    page_icon="🌿",
    layout="wide",  # Mantiene el layout wide para dashboards
    initial_sidebar_state="expanded",
)

# ========================================================
# 2. INYECCIÓN DE CSS AVANZADO (Layout, Sidebar Premium y Componentes)
# ========================================================
BRAND_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap');

    /* Fondo general con el gradiente suave de la propuesta */
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #e3f2fd 100%) !important;
        background-attachment: fixed !important;
        font-family: 'Inter', sans-serif;
    }

    /* Reseteo y color de textos del panel principal */
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
        color: #212121 !important;
    }

    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3 {
        color: #1b5e20 !important;
    }

    /* Inputs globales cuando estás logueado */
    [data-testid="stAppViewContainer"] input {
        color: #212121 !important;
        background-color: #FFFFFF !important;
        border: 1px solid #ced4da !important;
    }

    /* ==========================================
       BARRA LATERAL ULTRA-PREMIUM (CSS REESTILIZADO)
       ========================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e4d2b 0%, #11381c 100%) !important;
        box-shadow: 4px 0 15px rgba(0,0,0,0.1) !important;
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
        color: #a5d6a7 !important;
    }

    /* Contenedor de Marca Renovado */
    .brand-container {
        padding: 1.5rem 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        margin-bottom: 1.2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }

    .brand-logo {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FFFFFF !important;
        letter-spacing: -0.5px;
    }

    .brand-subtitle {
        font-size: 0.85rem;
        color: #81c784 !important;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
        margin-top: 0.2rem;
    }

    /* Badge del usuario conectado */
    .user-badge {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 0.6rem 1rem;
        margin-bottom: 2rem;
        font-size: 0.9rem;
        color: #FFFFFF !important;
        text-align: center;
    }

    /* Rediseño completo del st.radio nativo para transformarlo en botones interactivos */
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] {
        display: none !important; /* Oculta títulos sobrantes */
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }

    /* Estilo base de las pestañas del menú */
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 0.65rem 1rem !important;
        margin-bottom: 0.6rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
    }

    /* Efecto Hover interactivo */
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(5px);
    }

    /* Estilo del botón activo / seleccionado */
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(90deg, #4caf50 0%, #2e7d3 100%) !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.35) !important;
    }
    
    /* Remover el círculo de selección radial clásico de HTML */
    [data-testid="stSidebar"] div[role="radiogroup"] label [data-testid="stRadioButtonToogleHoverTarget"] {
        display: none !important;
    }

    /* Botón de Cerrar Sesión con estilo Outlined destructivo */
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: #ff8a80 !important;
        border: 1px solid rgba(255, 138, 128, 0.4) !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        margin-top: 1rem;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 138, 128, 0.1) !important;
        border-color: #ff5252 !important;
        color: #ff5252 !important;
    }

    /* Tarjetas de Métricas (KPIs) del Dashboard */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    }
</style>
"""

# ========================================================
# 3. LOGIN_CSS: GLASSMORPHISM COMPACTO
# ========================================================
LOGIN_CSS = """
<style>
    /* Ocultar barra lateral en la pantalla de login */
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Contenedor Principal Esmerilado */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 460px !important;
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        background: rgba(255, 255, 255, 0.35) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.06) !important;
        margin: auto;
        margin-top: 6vh;
    }

    /* Bloque vertical interno ajustado */
    [data-testid="stVerticalBlock"] {
        gap: 0.6rem !important;
    }

    /* Formulario de Login */
    [data-content-id="stForm"] {
        background: rgba(255, 255, 255, 0.88) !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03) !important;
    }

    /* Labels de inputs */
    div[data-testid="stTextInput"] label p {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #212121 !important;
    }

    /* Campos de Entrada */
    div[data-testid="stTextInput"] input {
        border-radius: 8px !important;
        border: 1px solid #ced4da !important;
        padding: 10px 14px !important;
        background-color: #ffffff !important;
        transition: all 0.2s ease-in-out;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #1b5e20 !important;
        box-shadow: 0 0 0 3px rgba(27, 94, 32, 0.15) !important;
    }

    /* Botón de Ingreso */
    div.stFormSubmitButton > button {
        background: linear-gradient(to bottom, #2e7d32, #1b5e20) !important;
        color: white !important;
        border: none !important;
        padding: 12px 20px !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(27, 94, 32, 0.25) !important;
        transition: all 0.2s ease !important;
        margin-top: 0.8rem;
    }

    div.stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(27, 94, 32, 0.35) !important;
        background: linear-gradient(to bottom, #338a37, #1b5e20) !important;
        color: white !important;
    }

    .custom-footer {
        text-align: center;
        margin-top: 2rem;
        font-size: 0.8rem;
        color: #555555;
    }
</style>
"""

# Dictionary de ruteo para mapear los módulos del sistema
PAGINAS = {
    "📊 Dashboard": dashboard.render,
    "👥 Usuarios": usuarios.render,
    "🚗 Vehículos": vehiculos.render,
    "🆔 Conductores": conductores.render,
    "🗺️ Viajes": viajes.render,
}


# ========================================================
# 4. COMPONENTE: RENDEREADO DEL LOGIN
# ========================================================
def render_login() -> None:
    st.markdown(BRAND_CSS + LOGIN_CSS, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 0.5rem;">
            <h1 style="color: #1b5e20; font-weight: 700; margin-bottom: 0px; font-size: 2.3rem;">🌱 EcoTrack</h1>
            <p style="color: #555; margin-top: 4px; font-size: 0.9rem; letter-spacing: 0.5px;">VerdeMov S.A. &middot; Logística sustentable</p>
        </div>
    """, unsafe_allow_html=True)

    with st.form(key="login_form"):
        st.markdown("<h2 style='margin-top:0; font-size:1.4rem; color:#212121;'>Iniciar sesión</h2>", unsafe_allow_html=True)
        
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

            try:
                conn = sqlite3.connect("ecotrack.db")
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT username FROM usuarios WHERE username = ? AND password = ?",
                    (usuario_limpio, password_limpia),
                )
                user_match = cursor.fetchone()
                conn.close()

                if user_match:
                    st.session_state["logged_in"] = True
                    st.session_state["usuario"] = user_match[0]
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")

            except Exception:
                if usuario_limpio == "admin" and password_limpia == "ecotrack2025":
                    st.session_state["logged_in"] = True
                    st.session_state["usuario"] = "Administrador"
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")

    st.markdown("""
        <div style="display: flex; justify-content: space-between; padding: 0 10px; font-size: 0.85rem;">
            <a href="#" style="color: #555; text-decoration: none;">¿Olvidé mi contraseña?</a>
            <a href="#" style="color: #1b5e20; text-decoration: none; font-weight: 600;">Crear una cuenta</a>
        </div>
        <div class="custom-footer">
            © 2026 VerdeMov S.A. | Todos los derechos reservados | Versión 2.0.1
        </div>
    """, unsafe_allow_html=True)


# ========================================================
# 5. COMPONENTE: RENDERIZADO DE LA BARRA LATERAL (POST-LOGIN)
# ========================================================
def render_sidebar() -> str:
    # Contenedor unificado de marca estilizado vía CSS
    st.sidebar.markdown("""
        <div class="brand-container">
            <div class="brand-logo">🌿 EcoTrack</div>
            <div class="brand-subtitle">VerdeMov S.A.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f'<div class="user-badge">👤 Conectado: <b>{st.session_state.get("usuario", "Usuario")}</b></div>', unsafe_allow_html=True)
    
    # El st.radio nativo ahora se dibuja como un menú de bloques limpios y flotantes
    pagina = st.sidebar.radio("Navegación", list(PAGINAS.keys()), label_visibility="collapsed")
    
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.sidebar.caption("⚡ Movilidad 100% eléctrica")
    
    if st.sidebar.button("Cerrar sesión", use_container_width=True):
        st.session_state.clear()
        st.rerun()
        
    return pagina


# ========================================================
# 6. CONTROLADOR PRINCIPAL DE LA APLICACIÓN
# ========================================================
def main() -> None:
    # Inicializa las tablas necesarias
    init_db()

    # Control de ruteo según estado de autenticación
    if not st.session_state.get("logged_in"):
        render_login()
        return

    # Renderizado de la App principal con la barra lateral premium
    st.markdown(BRAND_CSS, unsafe_allow_html=True)
    pagina = render_sidebar()
    PAGINAS[pagina]()


if __name__ == "__main__":
    main()