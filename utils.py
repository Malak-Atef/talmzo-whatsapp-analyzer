import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import io
import base64

# Constants
APP_DATA_DIR = Path("data")
APP_DATA_DIR.mkdir(exist_ok=True)

def add_notification(msg, type="info"):
    """Add a notification to the Streamlit app"""
    if type == "success":
        st.success(msg)
    elif type == "warning":
        st.warning(msg)
    elif type == "error":
        st.error(msg)
    else:
        st.info(msg)

def set_if_none(key, value):
    """Set a session state value if it doesn't exist"""
    if key not in st.session_state:
        st.session_state[key] = value

def to_excel_bytes(part_df: pd.DataFrame, details_df: pd.DataFrame | None) -> bytes:
    """Create Excel file in-memory with summary and details sheets."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        part_df.to_excel(writer, index=False, sheet_name="Summary")
        if details_df is not None and not details_df.empty:
            det = details_df.copy()
            det.to_excel(writer, index=False, sheet_name="Details")
    return output.getvalue()

def process_whatsapp_file(file_bytes, encoding='utf-8'):
    """Process WhatsApp chat export file"""
    try:
        content = file_bytes.decode(encoding)
        # Process chat content and return DataFrame
        # Add your WhatsApp chat processing logic here
        pass
    except UnicodeDecodeError:
        # Try alternative encodings if utf-8 fails
        try:
            content = file_bytes.decode('utf-16')
        except:
            raise ValueError("Could not decode file with UTF-8 or UTF-16 encoding")
    return content

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the data"""
    # Add your data cleaning logic here
    return df

def load_mapping_file(file_path: Path) -> pd.DataFrame:
    """Load name mapping file"""
    if file_path.exists():
        return pd.read_csv(file_path)
    return pd.DataFrame(columns=['raw_name', 'mapped_name'])

def save_mapping_file(df: pd.DataFrame, file_path: Path):
    """Save name mapping file"""
    df.to_csv(file_path, index=False)

def get_download_link(data, filename, text):
    """Generate a download link for any data"""
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{text}</a>'
    return href
