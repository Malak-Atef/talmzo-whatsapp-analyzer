# utils/config.py
import streamlit as st

# ألوان متسقة لتحسين الهوية البصرية
PRIMARY_COLOR = "#FF7A00"
PRIMARY_DARK = "#E06A00"
SUCCESS_COLOR = "#00C851"
WARNING_COLOR = "#FFBB33"
ERROR_COLOR = "#FF4444"
INFO_COLOR = "#33B5E5"

def setup_theme():
    """إعداد ثيم التطبيق"""
    # التحقق من وجود إعدادات الثيم في الجلسة
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'  # الثيم الافتراضي
    
    if st.session_state.theme == 'dark':
        BG_COLOR = "#FFFFFF"
        CARD_COLOR = "#F8F9FA"
        TEXT_COLOR = "#31333F"
        TEXT_MUTED = "#666666"
        BORDER_COLOR = "#E0E0E0"
        SURFACE_COLOR = "#F0F2F6"
    else:
        BG_COLOR = "#0E0D0D"
        CARD_COLOR = "#F8F9FA"
        TEXT_COLOR = "#31333F"
        TEXT_MUTED = "#666666"
        BORDER_COLOR = "#E0E0E0"
        SURFACE_COLOR = "#F0F2F6"
    
    CUSTOM_CSS = f"""
    <style>
    :root {{
        --primary: {PRIMARY_COLOR};
        --primary-dark: {PRIMARY_DARK};
        --success: {SUCCESS_COLOR};
        --warning: {WARNING_COLOR};
        --error: {ERROR_COLOR};
        --info: {INFO_COLOR};
        --bg: {BG_COLOR};
        --card: {CARD_COLOR};
        --text: {TEXT_COLOR};
        --text-muted: {TEXT_MUTED};
        --border: {BORDER_COLOR};
        --surface: {SURFACE_COLOR};
    }}
    
    .stApp {{
        background-color: var(--bg);
        color: var(--text);
        transition: all 0.3s ease;
    }}
    
    /* تحسينات للأزرار */
    .stButton>button, .stDownloadButton>button {{
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: #000;
        border: 0;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(255, 122, 0, 0.3);
        transition: all 0.2s ease;
    }}
    
    .stButton>button:hover, .stDownloadButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(255, 122, 0, 0.4);
        filter: brightness(1.1);
    }}
    
    .stButton>button:active, .stDownloadButton>button:active {{
        transform: translateY(0);
    }}
    
    /* تحسينات الشريط الجانبي */
    div[data-testid="stSidebar"] {{
        background-color: var(--surface);
        border-right: 1px solid var(--border);
    }}
    
    /* تحسينات العناوين */
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
    }}
    
    h1 {{
        color: var(--primary) !important;
        font-size: 2.2rem !important;
    }}
    
    h2 {{
        font-size: 1.8rem !important;
        border-bottom: 2px solid var(--primary);
        padding-bottom: 0.5rem;
    }}
    
    /* تحسينات البطاقات */
    .card {{
        background: var(--card);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid var(--border);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }}
    
    .card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }}
    
    /* تحسينات البادجات */
    .badge {{
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-muted);
    }}
    
    .badge-primary {{
        background: rgba(255, 122, 0, 0.15);
        color: var(--primary);
        border-color: rgba(255, 122, 0, 0.3);
    }}
    
    .badge-success {{
        background: rgba(0, 200, 81, 0.15);
        color: var(--success);
        border-color: rgba(0, 200, 81, 0.3);
    }}
    
    .badge-warning {{
        background: rgba(255, 187, 51, 0.15);
        color: var(--warning);
        border-color: rgba(255, 187, 51, 0.3);
    }}
    
    .badge-error {{
        background: rgba(255, 68, 68, 0.15);
        color: var(--error);
        border-color: rgba(255, 68, 68, 0.3);
    }}
    
    /* تحسينات النصوص */
    .small {{
        font-size: 0.9rem;
        color: var(--text-muted);
        line-height: 1.5;
    }}
    
    .app-title {{
        font-size: 1.6rem;
        font-weight: 900;
        letter-spacing: 0.5px;
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    /* تحسينات الإشعارات */
    .notification-badge {{
        position: absolute;
        top: -5px;
        right: -5px;
        background-color: var(--error);
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        font-size: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(255, 68, 68, 0.4);
    }}
    
    /* تحسينات الجداول */
    .dataframe {{
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }}
    
    /* تحسينات الـ metrics */
    [data-testid="stMetricValue"] {{
        color: var(--primary);
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: var(--text-muted);
        font-size: 1rem !important;
        font-weight: 600 !important;
    }}
    
    /* تحسينات الـ tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: var(--surface);
        border-radius: 12px 12px 0 0;
        padding: 12px 20px;
        font-weight: 600;
        border: 1px solid var(--border);
        border-bottom: none;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: var(--primary);
        color: #000;
    }}
    
    /* تحسينات الـ progress bar */
    .stProgress > div > div {{
        background: linear-gradient(90deg, var(--primary), var(--primary-dark));
    }}
    
    /* تحسينات للهواتف */
    @media (max-width: 768px) {{
        .stButton > button {{
            padding: 0.7rem 1.2rem;
            font-size: 0.95rem;
        }}
        
        .app-title {{
            font-size: 1.4rem;
        }}
        
        .card {{
            padding: 16px;
        }}
        
        h1 {{
            font-size: 1.8rem !important;
        }}
        
        h2 {{
            font-size: 1.5rem !important;
        }}
    }}
    </style>
    """
    
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)