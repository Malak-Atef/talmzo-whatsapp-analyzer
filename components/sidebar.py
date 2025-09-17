import streamlit as st
from pathlib import Path
import pandas as pd
from utils import add_notification, load_mapping_file, process_whatsapp_file

def render_sidebar():
    """Render the sidebar with file upload and settings"""
    with st.sidebar:
        st.image("assets/logo/logo.jpg", width=100)
        st.title("محلل واتساب")

        # File upload
        uploaded_file = st.file_uploader(
            "📱 حدد ملف محادثة واتساب",
            type=["txt"],
            help="قم بتصدير محادثة واتساب كملف نصي ثم ارفعه هنا"
        )

        # Theme switcher
        theme = st.selectbox(
            "🎨 المظهر",
            ["فاتح", "داكن"],
            index=0 if st.session_state.get('theme', 'light') == 'light' else 1
        )
        st.session_state.theme = 'light' if theme == "فاتح" else 'dark'

        # Name mapping
        st.subheader("🔄 تخصيص الأسماء", divider=True)
        mapping_type = st.radio(
            "طريقة تخصيص الأسماء:",
            ["تلقائي", "ملف CSV", "يدوي"],
            index=0,
            horizontal=True
        )

        if mapping_type == "ملف CSV":
            mapping_file = st.file_uploader(
                "ارفع ملف تخصيص الأسماء",
                type=["csv"],
                help="ملف CSV يحتوي على عمودين: raw_name و mapped_name"
            )
            if mapping_file:
                try:
                    mapping_df = pd.read_csv(mapping_file)
                    st.session_state['mapping_df'] = mapping_df
                    add_notification("تم تحميل ملف التخصيص بنجاح!", "success")
                except Exception as e:
                    add_notification(f"خطأ في تحميل ملف التخصيص: {str(e)}", "error")

        elif mapping_type == "يدوي":
            if 'raw_names' in st.session_state:
                st.write("قم بتخصيص الأسماء:")
                for name in st.session_state.raw_names:
                    mapped = st.text_input(f"الاسم الأصلي: {name}", value=name)
                    # Update mapping
                    if 'mapping_df' not in st.session_state:
                        st.session_state.mapping_df = pd.DataFrame(columns=['raw_name', 'mapped_name'])
                    st.session_state.mapping_df.loc[
                        st.session_state.mapping_df['raw_name'] == name, 'mapped_name'
                    ] = mapped

        # Process uploaded file
        if uploaded_file:
            try:
                chat_content = process_whatsapp_file(uploaded_file.read())
                st.session_state['chat_content'] = chat_content
                add_notification("تم تحميل ملف المحادثة بنجاح!", "success")
            except Exception as e:
                add_notification(f"خطأ في تحميل الملف: {str(e)}", "error")

        return uploaded_file is not None
