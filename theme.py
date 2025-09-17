import streamlit as st

# Theme constants
PRIMARY_COLOR = "#FF7A00"
PRIMARY_DARK = "#E06A00"
SUCCESS_COLOR = "#00C851"
WARNING_COLOR = "#FFBB33"
ERROR_COLOR = "#FF4444"
INFO_COLOR = "#33B5E5"

def setup_theme():
    """Setup theme and styling for the app"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'   

    # Set theme colors based on mode
    if st.session_state.theme == 'dark':
        BG_COLOR = "#0E0D0D"
        CARD_COLOR = "#1E1E1E"
        TEXT_COLOR = "#F8F9FA"
        TEXT_MUTED = "#BBBBBB"
        BORDER_COLOR = "#333333"
        SURFACE_COLOR = "#2C2C2C"
        HIGHLIGHT_COLOR = "#333366"
    else:
        BG_COLOR = "#FFFFFF"
        CARD_COLOR = "#F8F9FA"
        TEXT_COLOR = "#31333F"
        TEXT_MUTED = "#666666"
        BORDER_COLOR = "#E0E0E0"
        SURFACE_COLOR = "#F0F2F6"
        HIGHLIGHT_COLOR = "#DDE7FF"

    # Apply custom CSS
    st.markdown(f"""
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
        --highlight: {HIGHLIGHT_COLOR};
    }}

    .stApp {{
        background-color: var(--bg);
        color: var(--text);
        transition: all 0.3s ease;
    }}
    
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
    
    div[data-testid="stSidebar"] {{
        background-color: var(--bg);
        border-right: 1px solid var(--border);
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
    }}
    
    h1 {{
        color: var(--primary) !important;
        font-size: 2.2rem !important;
    }}
    
    .card {{
        background: var(--card);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid var(--border);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }}
    </style>
    """, unsafe_allow_html=True)
