from ecotrack_utils.constants import (
    BORDER_RADIUS,
    BORDER_RADIUS_LG,
    COLOR_ACCENT,
    COLOR_BG,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_TEXT,
)


def build_brand_css() -> str:
    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap');

    .stApp {{
        background: {COLOR_BG} !important;
        font-family: 'Inter', sans-serif;
    }}

    /* ── Sidebar pegado al borde izquierdo ── */
    section[data-testid="stSidebar"] {{
        background: {COLOR_PRIMARY} !important;
        border-right: none !important;
        box-shadow: 2px 0 24px rgba(27, 27, 27, 0.12) !important;
        top: 0 !important;
        left: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        min-width: 17.5rem !important;
        max-width: 17.5rem !important;
        width: 17.5rem !important;
        height: 100vh !important;
        z-index: 999990 !important;
    }}

    section[data-testid="stSidebar"] > div {{
        padding: 0 !important;
        margin: 0 !important;
        background: {COLOR_PRIMARY} !important;
        height: 100% !important;
    }}

    [data-testid="stSidebarContent"] {{
        padding: 0 !important;
        margin: 0 !important;
        background: {COLOR_PRIMARY} !important;
        height: 100% !important;
    }}

    [data-testid="stSidebarUserContent"] {{
        padding: 0 !important;
        margin: 0 !important;
        background: {COLOR_PRIMARY} !important;
        min-height: 100vh !important;
        display: flex !important;
        flex-direction: column !important;
    }}

    [data-testid="stSidebarUserContent"] > [data-testid="stVerticalBlock"] {{
        gap: 0 !important;
        padding: 0 0.75rem 1.25rem 0.75rem !important;
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        margin: 0 !important;
    }}

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown {{
        color: #FFFFFF !important;
    }}

    /* Brand header */
    .sidebar-brand {{
        display: flex;
        align-items: center;
        gap: 0.85rem;
        padding: 1.5rem 1rem 1.25rem 1rem;
        margin: 0 -0.75rem 0 -0.75rem;
        background: rgba(0, 0, 0, 0.12);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }}

    .sidebar-brand-icon {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 2.75rem;
        height: 2.75rem;
        background: rgba(255, 255, 255, 0.12);
        border-radius: 10px;
        flex-shrink: 0;
    }}

    .sidebar-brand-text {{
        display: flex;
        flex-direction: column;
        gap: 0.15rem;
        min-width: 0;
    }}

    .sidebar-brand-name {{
        font-size: 1.2rem;
        font-weight: 700;
        color: #FFFFFF !important;
        letter-spacing: -0.3px;
        line-height: 1.2;
    }}

    .sidebar-brand-org {{
        font-size: 0.7rem;
        font-weight: 600;
        color: {COLOR_ACCENT} !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        line-height: 1.2;
    }}

    /* User session */
    .sidebar-user {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem 0.25rem 1.25rem 0.25rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 0.5rem;
    }}

    .sidebar-user-avatar {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 2.25rem;
        height: 2.25rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        flex-shrink: 0;
    }}

    .sidebar-user-info {{
        display: flex;
        flex-direction: column;
        gap: 0.1rem;
        min-width: 0;
    }}

    .sidebar-user-label {{
        font-size: 0.68rem;
        font-weight: 500;
        color: {COLOR_ACCENT} !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}

    .sidebar-user-name {{
        font-size: 0.9rem;
        font-weight: 600;
        color: #FFFFFF !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .nav-section-title {{
        font-size: 0.68rem !important;
        font-weight: 600 !important;
        color: rgba(255, 255, 255, 0.5) !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        padding: 0.75rem 0.5rem 0.5rem 0.5rem;
        margin: 0 !important;
    }}

    /* Nav buttons (hijos 3–7 del bloque vertical = módulos) */
    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:nth-child(n+3):nth-child(-n+7) .stButton {{
        margin: 0.1rem 0 !important;
    }}

    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:nth-child(n+3):nth-child(-n+7) .stButton > button {{
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: 100% !important;
        padding: 0.7rem 0.85rem 0.7rem 2.65rem !important;
        border: none !important;
        border-radius: 8px !important;
        background: transparent !important;
        color: rgba(255, 255, 255, 0.82) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: none !important;
        transition: background 0.18s ease, color 0.18s ease, box-shadow 0.18s ease !important;
        position: relative !important;
        min-height: 2.65rem !important;
        margin: 0 !important;
    }}

    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:nth-child(n+3):nth-child(-n+7) .stButton > button::before {{
        font-family: 'Material Symbols Outlined' !important;
        font-size: 1.2rem !important;
        font-weight: normal !important;
        position: absolute !important;
        left: 0.75rem !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        line-height: 1 !important;
        opacity: 0.88;
    }}

    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:nth-child(3) .stButton > button::before {{
        content: 'space_dashboard' !important;
    }}

    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:nth-child(4) .stButton > button::before {{
        content: 'group' !important;
    }}

    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:nth-child(5) .stButton > button::before {{
        content: 'directions_car' !important;
    }}

    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:nth-child(6) .stButton > button::before {{
        content: 'badge' !important;
    }}

    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:nth-child(7) .stButton > button::before {{
        content: 'route' !important;
    }}

    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:nth-child(n+3):nth-child(-n+7) .stButton > button:hover {{
        background: rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
        transform: none !important;
        border: none !important;
    }}

    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:nth-child(n+3):nth-child(-n+7) .stButton > button[data-testid="baseButton-primary"] {{
        background: rgba(255, 255, 255, 0.14) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: inset 3px 0 0 {COLOR_ACCENT} !important;
        border: none !important;
    }}

    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:nth-child(n+3):nth-child(-n+7) .stButton > button[data-testid="baseButton-primary"]::before {{
        opacity: 1;
    }}

    /* Logout (último botón del sidebar) */
    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:last-child .stButton > button {{
        background: transparent !important;
        color: rgba(255, 255, 255, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.22) !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        margin-top: 0.25rem !important;
        transition: all 0.18s ease !important;
        box-shadow: none !important;
    }}

    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > div:last-child .stButton > button:hover {{
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: {COLOR_ACCENT} !important;
        color: #FFFFFF !important;
    }}

    .sidebar-spacer {{
        flex: 1;
        min-height: 1.5rem;
    }}

    .sidebar-footer {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 0.5rem 0.25rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.45) !important;
        letter-spacing: 0.02em;
    }}

    .sidebar-footer-dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: {COLOR_SECONDARY};
        flex-shrink: 0;
    }}

    /* Eliminar franja superior y huecos del layout Streamlit */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        z-index: 999999 !important;
    }}

    [data-testid="stSidebarHeader"] {{
        padding: 0 !important;
        background: {COLOR_PRIMARY} !important;
    }}

    [data-testid="stSidebarCollapsedControl"] {{
        color: #FFFFFF !important;
    }}

    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {{
        border: none !important;
        padding: 0 !important;
    }}

    .stApp > div:first-child {{
        margin: 0 !important;
        padding: 0 !important;
    }}

    [data-testid="stAppViewContainer"] {{
        padding: 1.5rem 2rem 2.5rem 2rem !important;
    }}

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
    [data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] {{
        color: {COLOR_TEXT} !important;
    }}

    [data-testid="stAppViewContainer"] h1 {{
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.25rem !important;
    }}

    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3 {{
        font-weight: 700 !important;
    }}

    [data-testid="stAppViewContainer"] [data-testid="stVerticalBlock"] {{
        gap: 1rem !important;
    }}

    [data-testid="stAppViewContainer"] input,
    [data-testid="stAppViewContainer"] textarea,
    [data-testid="stAppViewContainer"] select {{
        color: {COLOR_TEXT} !important;
        background-color: #FFFFFF !important;
        border: 1px solid {COLOR_ACCENT} !important;
        border-radius: {BORDER_RADIUS} !important;
        padding: 0.65rem 1rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }}

    [data-testid="stAppViewContainer"] input:focus,
    [data-testid="stAppViewContainer"] textarea:focus {{
        border-color: {COLOR_PRIMARY} !important;
        box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.18) !important;
        outline: none !important;
    }}

    [data-testid="stAppViewContainer"] .stButton > button {{
        background: {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: {BORDER_RADIUS} !important;
        padding: 0.65rem 1.35rem !important;
        font-weight: 600 !important;
        transition: background 0.2s ease, transform 0.15s ease !important;
    }}

    [data-testid="stAppViewContainer"] .stButton > button:hover {{
        background: {COLOR_SECONDARY} !important;
        color: #FFFFFF !important;
        transform: translateY(-1px);
    }}

    [data-testid="stAppViewContainer"] .stButton > button[kind="secondary"],
    [data-testid="stAppViewContainer"] .stButton > button[data-testid="baseButton-secondary"] {{
        background: #FFFFFF !important;
        color: {COLOR_PRIMARY} !important;
        border: 1px solid {COLOR_SECONDARY} !important;
    }}

    [data-testid="stAppViewContainer"] .stButton > button[kind="secondary"]:hover,
    [data-testid="stAppViewContainer"] .stButton > button[data-testid="baseButton-secondary"]:hover {{
        background: {COLOR_ACCENT} !important;
        border-color: {COLOR_SECONDARY} !important;
        color: {COLOR_TEXT} !important;
    }}

    [data-testid="stAppViewContainer"] div.stFormSubmitButton > button,
    [data-testid="stAppViewContainer"] button[data-testid="baseButton-primary"] {{
        background: {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: {BORDER_RADIUS} !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: background 0.2s ease !important;
    }}

    [data-testid="stAppViewContainer"] div.stFormSubmitButton > button:hover,
    [data-testid="stAppViewContainer"] button[data-testid="baseButton-primary"]:hover {{
        background: {COLOR_SECONDARY} !important;
        color: #FFFFFF !important;
    }}

    [data-testid="stAppViewContainer"] [data-content-id="stForm"] {{
        background: #FFFFFF !important;
        border: 1px solid {COLOR_ACCENT} !important;
        border-radius: {BORDER_RADIUS_LG} !important;
        padding: 1.75rem 2rem !important;
        margin-bottom: 1rem !important;
    }}

    [data-testid="stAppViewContainer"] [data-testid="stExpander"] {{
        background: #FFFFFF !important;
        border: 1px solid {COLOR_ACCENT} !important;
        border-radius: {BORDER_RADIUS} !important;
        margin-bottom: 0.75rem !important;
    }}

    [data-testid="stAppViewContainer"] [data-testid="stExpander"] summary {{
        padding: 1rem 1.25rem !important;
        font-weight: 600 !important;
    }}

    div[data-testid="stMetric"] {{
        background-color: #FFFFFF !important;
        border: 1px solid {COLOR_ACCENT} !important;
        border-radius: {BORDER_RADIUS} !important;
        padding: 1.35rem 1.5rem !important;
        box-shadow: 0 2px 8px rgba(27, 27, 27, 0.04) !important;
    }}

    div[data-testid="stMetric"] label {{
        color: {COLOR_TEXT} !important;
        font-weight: 500 !important;
    }}

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {COLOR_PRIMARY} !important;
        font-weight: 700 !important;
    }}

    [data-testid="stAppViewContainer"] [data-testid="stDataFrame"] {{
        border: 1px solid {COLOR_ACCENT} !important;
        border-radius: {BORDER_RADIUS} !important;
        overflow: hidden !important;
    }}

    [data-testid="stAppViewContainer"] .stProgress > div > div {{
        background-color: {COLOR_PRIMARY} !important;
    }}

    [data-testid="stAppViewContainer"] .stProgress {{
        padding: 0.5rem 0 !important;
    }}

    hr {{
        border-color: {COLOR_ACCENT} !important;
        margin: 1.75rem 0 !important;
    }}
</style>
"""


def build_login_css() -> str:
    return f"""
<style>
    section[data-testid="stSidebar"] {{
        display: none !important;
    }}

    [data-testid="stAppViewBlockContainer"] {{
        max-width: 480px !important;
        padding: 2.75rem 2.25rem 2.25rem 2.25rem !important;
        background: #FFFFFF !important;
        border-radius: {BORDER_RADIUS_LG} !important;
        border: 1px solid {COLOR_ACCENT} !important;
        box-shadow: 0 8px 32px rgba(27, 27, 27, 0.06) !important;
        margin: auto;
        margin-top: 5vh;
    }}

    [data-testid="stVerticalBlock"] {{
        gap: 0.85rem !important;
    }}

    [data-content-id="stForm"] {{
        background: {COLOR_BG} !important;
        border: 1px solid {COLOR_ACCENT} !important;
        border-radius: {BORDER_RADIUS} !important;
        padding: 2rem 2.25rem !important;
        box-shadow: none !important;
    }}

    div[data-testid="stTextInput"] label p {{
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: {COLOR_TEXT} !important;
    }}

    div[data-testid="stTextInput"] input {{
        border-radius: {BORDER_RADIUS} !important;
        border: 1px solid {COLOR_ACCENT} !important;
        padding: 12px 16px !important;
        background-color: #FFFFFF !important;
        color: {COLOR_TEXT} !important;
        transition: all 0.2s ease-in-out;
    }}

    div[data-testid="stTextInput"] input:focus {{
        border-color: {COLOR_PRIMARY} !important;
        box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.18) !important;
    }}

    div.stFormSubmitButton > button {{
        background: {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 14px 24px !important;
        border-radius: {BORDER_RADIUS} !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: background 0.2s ease !important;
        margin-top: 1rem;
    }}

    div.stFormSubmitButton > button:hover {{
        background: {COLOR_SECONDARY} !important;
        color: #FFFFFF !important;
    }}

    .custom-footer {{
        text-align: center;
        margin-top: 2rem;
        font-size: 0.8rem;
        color: {COLOR_TEXT};
        opacity: 0.7;
    }}

    .login-link-muted {{
        color: {COLOR_TEXT};
        opacity: 0.65;
        text-decoration: none;
    }}

    .login-link-primary {{
        color: {COLOR_PRIMARY};
        text-decoration: none;
        font-weight: 600;
    }}
</style>
"""
