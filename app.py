 # -*- coding: utf-8 -*-    
import os
from pathlib import Path

def set_if_none(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

import io
import re
import sys
import math
import json
import time
import base64
import typing as t
from datetime import datetime, date, timedelta
from io import BytesIO

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------
# Page setup
# -----------------------------

APP_DATA_DIR = Path("data")
APP_DATA_DIR.mkdir(exist_ok=True)

# مفاتيح session ثابتة
SS = st.session_state

# إعدادات الصفحة
st.set_page_config(
    page_title="TALMZO - محلل واتساب",
    page_icon="/assets/logo/logo.ico",
    layout="wide",
    initial_sidebar_state="expanded",
    
)

# إخفاء أسماء الصفحات من القائمة الجانبية
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# إعدادات الثيمات
# -----------------------------
# ألوان متسقة لتحسين الهوية البصرية (متاحة على مستوى التطبيق)
PRIMARY_COLOR = "#FF7A00"
PRIMARY_DARK = "#E06A00"

def setup_theme():
    # التحقق من وجود إعدادات الثيم في الجلسة
    if 'theme' not in SS:
        SS.theme = 'dark'  # الثيم الافتراضي

    if SS.theme == 'dark':
        BG_COLOR = "#0E0D0D"
        CARD_COLOR = "#121212"
        TEXT_COLOR = "#E6E6E6"
        TEXT_MUTED = "#B5B5B5"
        BORDER_COLOR = "#2D2D2D"
        SURFACE_COLOR = "#161616"
    else:
        BG_COLOR = "#FFFFFF"
        CARD_COLOR = "#F8F9FA"
        TEXT_COLOR = "#31333F"
        TEXT_MUTED = "#666666"
        BORDER_COLOR = "#E0E0E0"
        SURFACE_COLOR = "#F0F2F6"

    # stripe color for alternating rows (adjust per theme)
    row_stripe = "rgba(255,255,255,0.02)" if SS.theme == 'dark' else "var(--surface)"

    CUSTOM_CSS = f"""
    <style>
    :root {{
        --primary: {PRIMARY_COLOR};
        --primary-dark: {PRIMARY_DARK};
        --success: #00CC96;
        --warning: #FFBB33;
        --error: #FF4444;
        --info: #00A3E0;
        --bg: {BG_COLOR};
        --card: {CARD_COLOR};
        --text: {TEXT_COLOR};
        --text-muted: {TEXT_MUTED};
        --border: {BORDER_COLOR};
        --surface: {SURFACE_COLOR};
        --row-stripe: {row_stripe};
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

    .stButton>button:hover, .stDownloadButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(255, 122, 0, 0.4);
        filter: brightness(1.1);
    }}

    div[data-testid="stSidebar"] {{
        background-color: var(--surface);
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

    .badge {{
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-muted);
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

    /* DataFrame styling follows theme variables */
 
        /* === stronger DataFrame & sidebar rules to follow theme === */
        div[data-testid="stSidebar"] {{
            background-color: var(--surface) !important;
            color: var(--text) !important;
            border-right: 1px solid var(--border) !important;
        }}

        div[data-testid="stDataFrame"] table,
        div[data-testid="stTable"] table {{
            background-color: var(--card) !important;
            color: var(--text) !important;
            border-collapse: collapse !important;
            width: 100% !important;
        }}

    .dataframe thead tr {{
        background-color: var(--surface);
        color: var(--text);
        font-weight: 700;
    }}

    .dataframe tbody tr {{
        background-color: transparent;
        color: var(--text);
    }}

    .dataframe tbody tr:nth-child(even) {{
        background-color: var(--row-stripe);
    }}

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

    .stProgress > div > div {{
        background: linear-gradient(90deg, var(--primary), var(--primary-dark));
    }}

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


# تهيئة الثيم
setup_theme()
st.write(SS.theme)

# -----------------------------
# Header مع تحسينات
# -----------------------------
def show_header():
    # 🖼️ اللوجو بعرض الشاشة
    try:
        logo_path = Path(__file__).parent / "assets/logo/logo.png"
        if logo_path.exists():
            import base64
            img_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()
            st.markdown(
                f"""
                <div style="width:100%; text-align:center; margin-bottom:1rem;">
                    <img src="data:image/png;base64,{img_base64}" 
                         style="width:100%; max-height:250px; object-fit:contain; border-radius:12px;" />
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {PRIMARY_COLOR}, {PRIMARY_DARK}); 
                        width: 100%; height: 180px; border-radius: 16px; margin-bottom:1rem;
                        display: flex; align-items: center; justify-content: center;
                        font-size: 48px; font-weight: bold; color: #000; opacity:0.75;'>
                TZ
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown(f"<div style='font-size: 3rem; color: {PRIMARY_COLOR};'>TZ</div>", unsafe_allow_html=True)

    # 📝 العنوان + زر الثيم
    c_title, c_theme = st.columns([6, 1])
    
    with c_title:
        st.markdown(
          
           f"""
            <div class="logo-wrap" style="display:flex; justify-content:center; align-items:center; margin-top:0.5rem;">
                <span>برنامج تلمذو للقراءات اليومية</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        

    with c_theme:
        theme_icon = "☀️" if st.session_state.theme == 'dark' else "🌙"
        if st.button(theme_icon, key="theme_toggle", help="تغيير الوضع"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()

    # خط فاصل أنيق
    st.markdown(
        "<div style='height:2px;background:linear-gradient(90deg,transparent,var(--primary),transparent);margin:1rem 0;'></div>",
        unsafe_allow_html=True
    )

# عرض الهيدر
show_header()

# -----------------------------
# Helper functions
# -----------------------------
SYSTEM_PREFIXES = (
    "Messages and calls are end-to-end encrypted.",
    "Messages to this chat and calls are now secured with end-to-end encryption.",
    "You joined using this group's invite link",
    "changed the subject",
    "changed this group's icon",
    "created group",
    "added",
    "removed",
    "left",
    "انضم",
    "أضاف",
    "قام بتغيير",
    "غيّر صورة المجموعة",
    "أنشأ المجموعة",
    "قام بإضافة",
    "قام بإزالة",
    "غادر",
)

MEDIA_OMITTED_TOKENS = (
    "<Media omitted>",
    "image omitted", "video omitted",
    "‏صوت غير مرفق", "ملف غير مرفق",
    "تم حذف هذه الرسالة", "This message was deleted",
    "<This message was edited>", "This message was edited",
    "تم تعديل هذه الرسالة"
)

# WhatsApp export date formats vary by locale/platform. We'll try multiple.
DATE_PATTERNS = [
    # [10/04/2025, 14:30:15] Name: message  (iOS/Android newer format with seconds)
    r"^\[(?P<dt>\d{1,2}/\d{1,2}/\d{2,4}),\s+(?P<time>\d{1,2}:\d{2}(?::\d{2})?)\]\s(?P<sender>[^:\n]+?):\s(?P<msg>.*)$",
    # 10/04/2025, 14:30 - Name: message  (Android classic with hyphen)
    r"^(?P<dt>\d{1,2}/\d{1,2}/\d{2,4}),\s+(?P<time>\d{1,2}:\d{2})\s+-\s+(?P<sender>[^:\n]+?):\s(?P<msg>.*)$",
    # 10/04/2025, 14:30:15 - Name: message (Android with seconds)
    r"^(?P<dt>\d{1,2}/\d{1,2}/\d{2,4}),\s+(?P<time>\d{1,2}:\d{2}:\d{2})\s+-\s+(?P<sender>[^:\n]+?):\s(?P<msg>.*)$",
    # 3/2/25, 1:23 PM - Name: message  (Android/iOS with AM/PM)
    r"^(?P<dt>\d{1,2}/\d{1,2}/\d{2,4}),\s+(?P<time>\d{1,2}:\d{2}(?:\s?[AP]M)?)\s+-\s+(?P<sender>[^:\n]+?):\s(?P<msg>.*)$",
]

DATE_FORMATS_TRY = [
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%d/%m/%y %H:%M:%S",
    "%d/%m/%y %H:%M",
    "%d/%m/%Y %I:%M %p",
    "%d/%m/%y %I:%M %p",
    "%m/%d/%Y %H:%M:%S",
    "%m/%d/%Y %H:%M",
    "%m/%d/%y %H:%M:%S",
    "%m/%d/%y %H:%M",
    "%m/%d/%Y %I:%M %p",
    "%m/%d/%y %I:%M %p",
]

@st.cache_data(show_spinner=False)
def parse_chat_txt(txt: str) -> pd.DataFrame:
    """Parse WhatsApp exported chat text into a DataFrame: [timestamp, sender, message].
    It supports multi-line messages by joining lines until the next message pattern is found.
    """
    lines = txt.splitlines()
    rows: list[dict] = []
    buffer = None  # hold current message dict

    regexes = [re.compile(p) for p in DATE_PATTERNS]

    def commit_buffer():
        nonlocal buffer, rows
        if buffer is not None:
            rows.append(buffer)
            buffer = None

    for line in lines:
        matched = None
        for rx in regexes:
            m = rx.match(line)
            if m:
                matched = m
                break
        if matched:
            # new message begins
            commit_buffer()
            dt_str = m.group("dt").strip()
            tm_str = m.group("time").strip()
            sender = m.group("sender").strip()
            msg = m.group("msg").strip()
            # try parse datetime
            dt_parsed = None
            for fmt in DATE_FORMATS_TRY:
                try:
                    dt_parsed = datetime.strptime(f"{dt_str} {tm_str}", fmt)
                    break
                except ValueError:
                    continue
            if dt_parsed is None:
                # Skip if unparseable
                continue

            buffer = {
                "timestamp": dt_parsed,
                "sender": sender,
                "message": msg,
            }
        else:
            # continuation of previous message (multiline)
            if buffer is not None:
                buffer["message"] += "\n" + line
            else:
                # orphan line - ignore
                pass
    # flush last
    commit_buffer()

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    # cleanup: drop system messages / media omitted lines
    def is_system(msg: str) -> bool:
        text = (msg or "").strip()
        if not text:
            return True
        if any(text.startswith(p) for p in SYSTEM_PREFIXES):
            return True
        if text in MEDIA_OMITTED_TOKENS:
            return True
        return False

    df = df[~df["message"].map(is_system)].copy()
    df["date"] = df["timestamp"].dt.date
    return df

def build_mapping_ui(unique_senders: list[str]) -> pd.DataFrame:
    """Interactive mapping editor: Sender Key -> Real Name."""
    st.subheader("🧭 تعريف الأسماء (Mapping)")
    st.caption("اربط أسماء أو أرقام واتس آب بالأسماء الحقيقية. لو رفعت ملف CSV فيه عمودين: sender_key, real_name هنستخدمه تلقائيًا.")
    
    # إنشاء نموذج بيانات للعرض والتحرير
    sample_data = []
    for sender in unique_senders:
        # البحث عن الاسم الحقيقي إذا كان موجودًا في الملف المحمل
        real_name = sender  # القيمة الافتراضية
        if mapping_df is not None and not mapping_df.empty:
            matched = mapping_df[mapping_df["sender_key"] == sender]
            if not matched.empty:
                real_name = matched.iloc[0]["real_name"]
        sample_data.append({"sender_key": sender, "real_name": real_name})
    
    sample = pd.DataFrame(sample_data)
    edited = st.data_editor(sample, use_container_width=True, num_rows="fixed", key="mapping_editor")
    return edited

import re

def normalize_phone(raw: str) -> str:
    if not isinstance(raw, str):
        return raw
    # نشيل أي مسافات أو شرطات أو رموز
    num = re.sub(r"\D", "", raw)
    # لو بيبدأ بـ 20 (مفتاح مصر) نشيله ونخلي الباقي
    if num.startswith("20"):
        num = num[2:]
    return num

def apply_mapping(df: pd.DataFrame, mapping_df: pd.DataFrame) -> pd.DataFrame:
    if mapping_df is None or mapping_df.empty:
        df = df.copy()
        df["name"] = df["sender"]
        return df

    df = df.copy()
    # لو مفيش sender_norm لسه، نعمله هنا
    if "sender_norm" not in df.columns:
        df["sender_norm"] = df["sender"].apply(normalize_phone)

    # إنشاء قاموس للتعيين
    mapping_dict = {}
    for _, row in mapping_df.iterrows():
        mapping_dict[str(row["sender_key"])] = row["real_name"]
    
    # تطبيق التعيين
    df["name"] = df["sender_norm"].map(mapping_dict).fillna(df["sender"])
    return df

@st.cache_data(show_spinner=False)
def compute_participation(df: pd.DataFrame, start: date, end: date, min_days: int) -> pd.DataFrame:
    """Compute distinct active days per name within [start, end]."""
    mask = (df["date"] >= start) & (df["date"] <= end)
    sub = df.loc[mask].copy()
    if sub.empty:
        return pd.DataFrame(columns=["name", "active_days", "status"])
    agg = (
        sub.groupby(["name"])["date"]
        .nunique()
        .reset_index(name="active_days")
        .sort_values(["active_days", "name"], ascending=[False, True])
    )
    agg["status"] = agg["active_days"].apply(lambda d: "✅ مشارك كافي" if d >= min_days else "❌ مشاركة أقل من المطلوب")
    return agg

@st.cache_data(show_spinner=False)
def to_excel_bytes(part_df: pd.DataFrame, details_df: pd.DataFrame | None) -> bytes:
    """Create Excel file in-memory with summary and details sheets."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        part_df.to_excel(writer, index=False, sheet_name="Summary")
        if details_df is not None and not details_df.empty:
            # Limit message length for Excel readability
            det = details_df.copy()
            det["timestamp"] = det["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
            det.to_excel(writer, index=False, sheet_name="Details")
    return output.getvalue()

@st.cache_data(show_spinner=False)
def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")

@st.cache_data(show_spinner=False)
def make_pdf_bytes(part_df: pd.DataFrame, title: str) -> bytes:
    """Generate a PDF using reportlab with optional Arabic shaping.
    Falls back to CSV bytes if reportlab or fonts fail.
    """
    try:
        # imports local to function so app can still run if reportlab missing
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.enums import TA_RIGHT, TA_CENTER
        import os

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=24, leftMargin=24,
                                topMargin=24, bottomMargin=24)
        styles = getSampleStyleSheet()

        # ---------------------------
        # Register Arabic-capable TTF if available
        # ---------------------------
        font_name = None
        # try common path; اضبطي المسار لو وضعتي الخط في مكان تاني
        font_path = os.path.join("assets", "fonts", "NotoNaskhArabic-Regular.ttf")
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont("NotoArabic", font_path))
                font_name = "NotoArabic"
            except Exception:
                font_name = None

        # ---------------------------
        # Try to enable proper Arabic shaping (optional)
        # ---------------------------
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display

            def fix_ar(text: str) -> str:
                if not isinstance(text, str) or text.strip() == "":
                    return text
                try:
                    reshaped = arabic_reshaper.reshape(text)
                    return get_display(reshaped)
                except Exception:
                    return text
        except Exception:
            # arabic_reshaper / python-bidi not installed -> return text as-is
            def fix_ar(text: str) -> str:
                return text

        # ---------------------------
        # Title
        # ---------------------------
        title_text = fix_ar(title)
        title_style = ParagraphStyle(
            name="Title",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontName=font_name or styles["Title"].fontName,
        )
        story = [Paragraph(title_text, title_style), Spacer(1, 12)]

        # ---------------------------
        # Build table data (reshape Arabic if possible)
        # ---------------------------
        # prepare header
        headers = [fix_ar(str(c)) for c in list(part_df.columns)]
        data = [headers]

        for _, row in part_df.iterrows():
            row_vals = [fix_ar("" if pd.isna(v) else str(v)) for v in row.tolist()]
            data.append(row_vals)

        # Create table; align right if we have Arabic-capable font
        h_align = "RIGHT" if font_name else "LEFT"
        table = Table(data, repeatRows=1, hAlign=h_align)

        # Styling
        tbl_style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2b2b2b")),  # header bg
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("FONTNAME", (0, 0), (-1, -1), font_name or styles["Normal"].fontName),
            ("ALIGN", (0, 0), (-1, -1), "RIGHT" if font_name else "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
        table.setStyle(tbl_style)

        story.append(table)

        doc.build(story)
        return buffer.getvalue()

    except Exception as e:
        # If anything goes wrong (module missing, font error, building error), fallback to CSV bytes
        try:
            # Log exception to console for debugging (optional)
            print("make_pdf_bytes error:", e)
        except Exception:
            pass
        return df_to_csv_bytes(part_df)


# -----------------------------
# Sidebar – Inputs
# -----------------------------
with st.sidebar:
    st.header("الإعدادات")
    
    # رفع ملف الشات مع الاحتفاظ به في الجلسة
    up = st.file_uploader("ارفع ملف المحادثة (.txt)", type=["txt"], key="chat_file")
    if up is not None:
        SS["chat_bytes"] = up.read()
        SS["chat_name"] = up.name
        st.success(f"تم رفع ملف المحادثة: {up.name}")

        colA, colB = st.columns(2)
        with colA:
            start_date = st.date_input("من تاريخ", value=SS.get("start_date", date(date.today().year, 1, 1)))
            SS["start_date"] = start_date
        with colB:
            end_date = st.date_input("إلى تاريخ", value=SS.get("end_date", date.today()))
            SS["end_date"] = end_date

        min_days = st.number_input("الحد الأدنى لأيام المشاركة", min_value=1, max_value=365, value=int(SS.get("min_days",5)), step=1)
        SS["min_days"] = int(min_days)

        st.markdown("---")
        st.caption("ملف الأسماء يجب ان يحتوي علي — عمودان: sender_key, real_name")
        mapping_file = st.file_uploader("ملف الأسماء CSV", type=["csv"], key="mapping_file")



# -----------------------------
# Main workflow with tabs
# -----------------------------
if "chat_bytes" not in SS:
    # صفحة ترحيب محسنة بالعربية البسيطة
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h1 style='color: var(--primary); margin-bottom: 0.5rem;'>🚀 Welcome to Talmazo WhatsApp Analyzer!</h1>
        <p style='font-size: 1.3rem; color: var(--text-muted); margin-bottom: 2rem;'>
            أدق أداة لتحليل مجموعات واتساب وتقييم المشاركة
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # تقسيم الصفحة بطريقة أكثر تنظيمًا
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # بطاقة ترحيب رئيسية
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📱</div>
            <h2 style="color: var(--primary);">ابدأ تحليل مجموعتك</h2>
            <p style="font-size: 1.1rem;">حمل ملف المحادثة من واتساب وشوف تحليل مفصل لمشاركة الأعضاء</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    features_col1, features_col2, features_col3 = st.columns(3)
    
    with features_col1:
        st.markdown("""
        <div class="card">
            <div style="text-align: center; font-size: 2.5rem; margin-bottom: 1rem;">✅</div>
            <h4>تقييم دقيق</h4>
            <p>اعرف عدد الأيام اللي كل عضو شارك فيها</p>
        </div>
        """, unsafe_allow_html=True)
    
    with features_col2:
        st.markdown("""
        <div class="card">
            <div style="text-align: center; font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
            <h4>تقارير مفصلة</h4>
            <p>احصل على تقارير Excel وPDF سهلة القراءة</p>
        </div>
        """, unsafe_allow_html=True)
    
    with features_col3:
        st.markdown("""
        <div class="card">
            <div style="text-align: center; font-size: 2.5rem; margin-bottom: 1rem;">🔒</div>
            <h4>خصوصية كاملة</h4>
            <p>البيانات بتكون على جهازك ومش هتطلع على النت</p>
        </div>
        """, unsafe_allow_html=True)
    
    # خطوات العمل
    st.markdown("### 🛠️ خطوات سهلة")
    
    steps_col1, steps_col2, steps_col3, steps_col4 = st.columns(4)
    
    with steps_col1:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">1</div>
            <h4>📤 ارفع الملف</h4>
            <p>من واتساب > تصدير الدردشة</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col2:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">2</div>
            <h4>📅 حدد الفترة</h4>
            <p>اختار من امتى لامتى تعمل التحليل</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col3:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">3</div>
            <h4>👥 ربط الأسماء</h4>
            <p>اعرف مين هو مين في المجموعة</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col4:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">4</div>
            <h4>📊 شوف النتائج</h4>
            <p>اطلع على التقارير وحملها</p>
        </div>
        """, unsafe_allow_html=True)
    
    # قسم الأسئلة الشائعة
    with st.expander("❓ أسئلة بتتكرر", expanded=False):
        st.markdown("""
        <div class="card">
            <h4>🤔 ازاي أصدّر المحادثة من واتساب؟</h4>
            <p>• افتح المجموعة في واتساب<br>• اضغط على الأسماء أعلى الشاشة<br>• اضغط على "المزيد" ثم "تصدير الدردشة"<br>• اختار "بدون وسائط"</p>
            
            <h4>🔢 هل الأرقام لازم تكون بنفس الشكل؟</h4>
            <p>لا، البرنامج هيعرف يطابق الأرقام حتى لو مختلفة في الشكل</p>
            
            <h4>⏳ كم من الوقت ياخد التحليل؟</h4>
            <p>ثواني قليلة فقط، حسب عدد الرسائل</p>
        </div>
        """, unsafe_allow_html=True)
    
    # دعوة للعمل مع تصميم جذاب
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 1rem;">
        <h2 style="color: var(--primary);">جاهز تبدأ؟</h2>
        <p style="font-size: 1.2rem; margin-bottom: 2rem;">ابدأ رحلة التحليل دلوقتي وخطوة خطوة</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 ابدأ التحليل المتقدم", type="primary", use_container_width=True):
        with st.spinner("⏳ جارٍ تحليل المحادثة..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            txt_content = SS["chat_bytes"].decode("utf-8", errors="ignore")
            status_text.text("📥 جارٍ معالجة الملف...")
            progress_bar.progress(20)
            
            df = parse_chat_txt(txt_content)
            status_text.text("🔍 جارٍ تحليل المحادثة...")
            progress_bar.progress(60)
            
            SS["analysis_done"] = True
            SS["df"] = df
            df["sender_norm"] = df["sender"].apply(normalize_phone)
            
            status_text.text("✅ تم التحليل بنجاح!")
            progress_bar.progress(100)
            time.sleep(0.5)
            status_text.empty()         

    # تذييل الصفحة
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center;">
        <p class="small">تم التطوير بواسطة Streamlit • الإصدار 2.1.0</p>
        <p class="small">طور بواسطة ملاك عاطف © 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()



# إذا كان هناك ملف محادثة، نعرض التبويبات
tabs = option_menu(
    menu_title=None,
    options=["التحليل", "النتائج", "التفاصيل", "الأسماء", "التقارير"],
    icons=["graph-up", "bar-chart", "list-ul", "people", "download"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "var(--card)"},
        "nav-link": {"font-size": "16px", "font-weight": "bold", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "var(--primary)"},
    }
)

df = None
if tabs == "التحليل":
    st.header("📈 تحليل متقدم للمحادثة")
    
    # زر ثابت لبدء التحليل
    if st.button("🚀 ابدأ التحليل المتقدم", type="primary", use_container_width=True):
        with st.spinner("⏳ جارٍ تحليل المحادثة..."):
            progress_bar = st.progress(0)
            
            txt_content = SS["chat_bytes"].decode("utf-8", errors="ignore")
            progress_bar.progress(30)
            
            df = parse_chat_txt(txt_content)
            progress_bar.progress(60)
            
            SS["analysis_done"] = True
            SS["df"] = df
            df["sender_norm"] = df["sender"].apply(normalize_phone)
            
            progress_bar.progress(100)
            st.success("تم تحليل المحادثة بنجاح")
            time.sleep(0.5)

# لو عندك نتيجة محفوظة في الجلسة من قبل (علشان بعد التحديث أو إعادة تشغيل مش يضيع)
if "df" in SS and df is None:
    df = SS["df"]

if df is None or df.empty:
    st.error("لم يتم التعرف على أي رسائل. تأكدي أن الملف من 'تصدير الدردشة' القياسي لواتس آب وأن التنسيق مدعوم.")
    st.stop()

if tabs == "التحليل":
    st.success(f"تم تحميل المحادثة: {len(df):,} رسالة بعد استبعاد الرسائل النظامية.")
    
    # عرض تحليل سريع
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("إجمالي الرسائل", len(df))
    with col2:
        st.metric("عدد المشاركين", df["sender"].nunique())
    with col3:
        date_range = f"{df['date'].min()} إلى {df['date'].max()}"
        st.metric("الفترة الزمنية", date_range)
    

    with st.expander("عرض أول 200 رسالة (بعد التنظيف)", expanded=False):
        st.dataframe(df.head(200), use_container_width=True, hide_index=True)

# Prepare mapping
unique_senders = sorted(df["sender"].dropna().unique().tolist())

# أولوية التحميل: ملف محفوظ محليًا للمجموعة -> ملف مرفوع الآن -> جدول محرر
mapping_df = None
if "loaded_mapping_df" in SS:
    mapping_df = SS["loaded_mapping_df"]
elif mapping_file is not None:
    try:
        mapping_df = pd.read_csv(mapping_file, encoding="utf-8-sig")
        # نضبط الأعمدة ونشيل المسافات
        mapping_df.columns = mapping_df.columns.str.strip().str.lower()
        mapping_df = mapping_df.rename(columns={
            "sender_key": "sender_key",
            "real_name": "real_name"
        })
        # إزالة العمود الأول إذا كان يحتوي على أرقام متسلسلة
        if "unnamed: 0" in mapping_df.columns:
            mapping_df = mapping_df.drop(columns=["unnamed: 0"])
        
        required_cols = {"sender_key", "real_name"}
        if not required_cols.issubset(set(mapping_df.columns)):
            st.warning("ملف CSV لازم يحتوي على عمودين: sender_key, real_name. تم تجاهله.")
            mapping_df = None
        else:
            # ✨ هنا بقى ننضف عمود sender_key
            mapping_df["sender_key"] = mapping_df["sender_key"].astype(str).str.strip()

    except Exception as e:
        st.warning(f"تعذر قراءة ملف CSV: {e}")
        mapping_df = None

if tabs == "الأسماء":
    # Show mapping editor (pre-filled with detected senders)
    edited_map = build_mapping_ui(unique_senders)
    SS["current_mapping_df"] = edited_map  

# استخدمي المابنج اللي تم تحميله لو موجود، وإلا الجداول المحررة
mapping_df = mapping_df if mapping_df is not None else SS.get("current_mapping_df", None)

# Apply mapping باستخدام الدالة الموحدة
df_mapped = apply_mapping(df, mapping_df)

# Compute participation
result_df = compute_participation(df_mapped, SS["start_date"], SS["end_date"], int(SS["min_days"]))

if tabs == "النتائج":
    st.header("📊 نتائج المشاركة")
    
    if result_df.empty:
        st.warning("""
        <div class="card">
            <h4>⚠️ مفيش رسائل في الفترة دي</h4>
            <p>• حاول تغير الفترة الزمنية<br>• أو اتأكد من ملف المحادثة</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # حساب الإحصائيات الأساسية
        total_members = len(result_df)
        active_members = len(result_df[result_df["active_days"] >= int(SS["min_days"])])
        inactive_members = len(result_df[result_df["active_days"] < int(SS["min_days"])])
        under_df = result_df[result_df["active_days"] < int(SS["min_days"])].copy()
        
        # نظرة سريعة على النتائج
        st.markdown("### 📈 النظرة العامة")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👥</div>
                <div style="font-size: 2rem; font-weight: 800; color: var(--primary);">{total_members}</div>
                <div style="font-size: 1rem; color: var(--text-muted);">إجمالي الأعضاء</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">✅</div>
                <div style="font-size: 2rem; font-weight: 800; color: var(--success);">{active_members}</div>
                <div style="font-size: 1rem; color: var(--text-muted);">وصلوا للحد المطلوب</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">❌</div>
                <div style="font-size: 2rem; font-weight: 800; color: var(--error);">{inactive_members}</div>
                <div style="font-size: 1rem; color: var(--text-muted);">ماوصلوش للحد</div>
            </div>
            """, unsafe_allow_html=True)
        
        # ملاحظة توضيحية للمستخدم
        st.info(f"""
        **ملاحظة:** الحد الأدنى للمشاركة اللي انت حددتها هو **{int(SS['min_days'])} يوم**.
        - اللي مشاركتهو وصلت أو زادت عن {int(SS['min_days'])} يوم يعتبر نشط ✅
        - اللي مشاركتهو أقل من {int(SS['min_days'])} يوم يعتبر غير نشط ❌
        """)
        
        # رسم بياني بسيط
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['النشطين', 'غير النشطين'],
            y=[active_members, inactive_members],
            marker_color=['#00CC96', '#EF553B'],
            text=[active_members, inactive_members],
            textposition='auto',
        ))
        
        fig.update_layout(
            title='عدد النشطين مقابل غير النشطين',
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تفاصيل النشطين
        st.markdown("### ✅ الأعضاء النشطين (اللي وصلوا للحد)")
        if active_members > 0:
            active_df = result_df[result_df["active_days"] >= int(SS["min_days"])].copy()
            st.dataframe(
                active_df.sort_values("active_days", ascending=False),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name": st.column_config.TextColumn("اسم العضو", width="large"),
                    "active_days": st.column_config.NumberColumn("أيام المشاركة", width="small"),
                    "status": st.column_config.TextColumn("الحالة", width="medium")
                }
            )
        else:
            st.warning("مفيش أعضاء نشطين في الفترة دي")
        
        # تفاصيل غير النشطين
        st.markdown("### ❌ الأعضاء غير النشطين (اللي ماوصلوش للحد)")
        if inactive_members > 0:
            st.dataframe(
                under_df.sort_values("active_days", ascending=False),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name": st.column_config.TextColumn("اسم العضو", width="large"),
                    "active_days": st.column_config.NumberColumn("أيام المشاركة", width="small"),
                    "status": st.column_config.TextColumn("الحالة", width="medium")
                }
            )
            
            # تحميل قائمة غير النشطين
            csv_under = under_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 نزل قائمة غير النشطين",
                data=csv_under,
                file_name="الاعضاء_غير_النشطين.csv",
                mime="text/csv",
                use_container_width=True,
                help="نزل ملف اكسل فيه قائمة الأعضاء اللي ماوصلوش للحد المطلوب"
            )
        else:
            st.success("🎉 مبروك! كل الأعضاء نشطين ووصلوا للحد المطلوب")
        
        # جدول كامل بالنتائج
        with st.expander("📋 شوف الجدول الكامل لكل الأعضاء", expanded=False):
            st.markdown("""
            <div class="card">
                <p>دي القائمة الكاملة لكل الأعضاء وعدد أيام المشاركة بتاعتهم:</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(
                result_df.sort_values("active_days", ascending=False),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name": st.column_config.TextColumn("اسم العضو", width="large"),
                    "active_days": st.column_config.NumberColumn("أيام المشاركة", width="small"),
                    "status": st.column_config.TextColumn("الحالة", width="medium")
                }
            )
            csv_all = result_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 نزل الجدول الكامل",
                data=csv_all,
                file_name="الاعضاء_المشاركة_الكاملة.csv",
                mime="text/csv",
                use_container_width=True,
                help="نزل ملف اكسل فيه الجدول الكامل لكل الأعضاء"
            )        
else:
     st.warning("مفيش مشاركة في الفترة دي")


if tabs == "التفاصيل":
    st.header("📋 تفاصيل المحادثة")
    mask = (df_mapped["date"] >= SS["start_date"]) & (df_mapped["date"] <= SS["end_date"])
    details_df = df_mapped.loc[mask, ["timestamp", "date", "name", "message"]].sort_values(["date", "name"])
    st.dataframe(details_df, use_container_width=True, hide_index=True)
if tabs == "التقارير":
    st.header("📊 تقارير قابلة للتنزيل")
    
    # شرح الخيارات
    st.markdown("""
    <div class="card">
        <h4>🎯 اختر نوع التقرير المناسب</h4>
        <p>يمكنك إنشاء وتحميل تقارير بمختلف الصيغ حسب احتياجاتك:</p>
        <ul>
            <li><strong>Excel</strong>: تقرير شامل يحتوي على ملخص وتحليل مفصل</li>
            <li><strong>CSV</strong>: ملف نصي بسيط للملخص فقط (يتوافق مع معظم التطبيقات)</li>
            <li><strong>PDF</strong>: تقرير بتنسيق PDF مناسب للطباعة والمشاركة</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # أزرار إنشاء التقارير
    if st.button("🔄 إنشاء جميع التقارير", type="primary", use_container_width=True):
        with st.spinner("⏳ جارٍ إنشاء التقارير... قد تستغرق بضع ثوان"):
            progress_bar = st.progress(0)
            
            excel_bytes = to_excel_bytes(result_df, details_df if 'details_df' in locals() else None)
            progress_bar.progress(33)
            
            csv_bytes = df_to_csv_bytes(result_df)
            progress_bar.progress(66)
            
            pdf_bytes = make_pdf_bytes(result_df, title="WhatsApp Participation Summary")
            progress_bar.progress(100)
            
            SS["excel_bytes"] = excel_bytes
            SS["csv_bytes"] = csv_bytes
            SS["pdf_bytes"] = pdf_bytes
            
            st.success("تم إنشاء التقارير بنجاح ✅")
            time.sleep(0.5)
    
    # عرض أزرار التحميل بعد إنشاء التقارير
    if "excel_bytes" in SS:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📊 Excel (كامل)",
                data=SS["excel_bytes"],
                file_name="تقرير_المشاركة.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="يتضمن ملخص وتحليل مفصل",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                label="📝 CSV (ملخص)",
                data=SS["csv_bytes"],
                file_name="ملخص_المشاركة.csv",
                mime="text/csv",
                help="ملف نصي بسيط للملخص فقط",
                use_container_width=True
            )
        
        with col3:
            st.download_button(
                label="📄 PDF (تقرير)",
                data=SS["pdf_bytes"],
                file_name="تقرير_المشاركة.pdf",
                mime="application/pdf",
                help="تقرير PDF مناسب للطباعة",
                use_container_width=True
            )
    
    # قسم الإعدادات المتقدمة للتقارير
    with st.expander("⚙️ إعدادات متقدمة للتقارير", expanded=False):
        st.markdown("""
        <div class="card">
            <h5>خيارات إضافية للتقارير</h5>
            <p>يمكنك تخصيص التقارير حسب احتياجاتك الخاصة</p>
        </div>
        """, unsafe_allow_html=True)
        
        report_title = st.text_input("عنوان التقرير", value="تقرير مشاركة واتساب")
        include_details = st.checkbox("تضمين التفاصيل الكاملة", value=True)
        add_timestamp = st.checkbox("إضافة الطابع الزمني", value=True)
        
        if st.button("تطبيق الإعدادات", use_container_width=True):
            st.success("تم تطبيق إعدادات التقارير بنجاح")

# إعدادات الخادم للأداء الأمثل
def configure_server():
    st.markdown("""
    <script>
    // إعدادات أداء إضافية
    console.log("TALMZO WhatsApp Analyzer - Optimized Version");
    </script>
    """, unsafe_allow_html=True)

# تشغيل إعدادات الخادم
configure_server()

# Tips / help
with st.expander("ℹ️ تعليمات سريعة"):
    st.markdown("""
**طريقة الاستخدام:**
1) من واتس آب → المزيد → **تصدير الدردشة** → بدون وسائط → احفظ ملف `.txt`.
2) ارفع الملف هنا.
3) حدّد الفترة الزمنية والحد الأدنى.
4) راجع أسماء المرسلين الظاهرة، وعدّلها في الجدول لو لازم (أو ارفع CSV mapping).
5) نزّل التقارير من الأسفل.

**صيغة CSV للأسماء:** عمودان بالضبط: `sender_key,real_name`
    """)

st.caption("تم الإنشاء بواسطة Streamlit. لا يتم رفع أي بيانات لخوادم خارجية – كل شيء يعمل محليًا.")
st.caption("الإصدار 2.0.0")
st.caption("طور بواسطة ملاك عاطف © 2025")