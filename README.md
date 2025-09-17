# WhatsApp Group Participation Analyzer (Streamlit)

Analyze members' participation in a WhatsApp group over a selected date range and flag members who participated fewer days than a chosen threshold.

## Features
- Upload exported WhatsApp chat `.txt` (no media).
- Robust parser for common iOS/Android export formats.
- Excludes system messages and media placeholders.
- Map raw sender names/numbers to real names (via in-app editor or CSV).
- Compute **distinct active days** per member within a date range.
- Download **Excel (Summary + Details)**, **CSV**, and **PDF** reports.
- Works locally; no data leaves your machine.

## Quickstart
```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open the local URL printed by Streamlit (usually http://localhost:8501).

## CSV Mapping format
Create a file `mapping.csv` with **two columns** (no header changes):
```
sender_key,real_name
+201001234567, ملاك عاطف
+201112345678, مايكل يوسف
```
You can also edit the mapping table interactively inside the app.

## Notes
- Export a chat from WhatsApp **without media** for a clean `.txt` file.
- Date formats vary by locale; the parser tries several patterns automatically.
- "Active days" means days where the member sent **≥1** message.
