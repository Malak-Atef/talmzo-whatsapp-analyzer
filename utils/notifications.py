import re

def normalize_phone(raw: str) -> str:
    if not isinstance(raw, str):
        return raw
    num = re.sub(r"\D", "", raw)
    if num.startswith("20"):  # Egypt prefix
        num = num[2:]
    return num
