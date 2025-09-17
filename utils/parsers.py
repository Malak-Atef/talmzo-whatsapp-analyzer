# utils/parsers.py
import re
import pandas as pd
from datetime import datetime, date
import streamlit as st

# أنماط التاريخ
DATE_PATTERNS = [
    r"^\[(?P<dt>\d{1,2}/\d{1,2}/\d{2,4}),\s+(?P<time>\d{1,2}:\d{2}(?::\d{2})?)\]\s(?P<sender>[^:\n]+?):\s(?P<msg>.*)$",
    r"^(?P<dt>\d{1,2}/\d{1,2}/\d{2,4}),\s+(?P<time>\d{1,2}:\d{2})\s+-\s+(?P<sender>[^:\n]+?):\s(?P<msg>.*)$",
    r"^(?P<dt>\d{1,2}/\d{1,2}/\d{2,4}),\s+(?P<time>\d{1,2}:\d{2}:\d{2})\s+-\s+(?P<sender>[^:\n]+?):\s(?P<msg>.*)$",
    r"^(?P<dt>\d{1,2}/\d{1,2}/\d{2,4}),\s+(?P<time>\d{1,2}:\d{2}(?:\s?[AP]M)?)\s+-\s+(?P<sender>[^:\n]+?):\s(?P<msg>.*)$",
]