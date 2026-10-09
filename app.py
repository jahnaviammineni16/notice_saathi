from dotenv import load_dotenv
load_dotenv()

import os
import json
import re
import time
import uuid
from html import escape
from datetime import date, datetime, timedelta
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

# ---------- SETTINGS ----------
APP_NAME = "Notice Saathi"
MODEL_NAME = os.getenv("MODEL_NAME", "gemma-4-31b-it")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

VOICE_CODES = {"English": "en-IN", "Kannada": "kn-IN", "Hindi": "hi-IN"}


# ---------- HELPERS ----------
def ask_model(parts):
    """Send text/image to Gemma 4. Tries 3 times if the internet drops."""
    last_error = None
    for attempt in range(3):
        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=parts)
            return response.text
        except Exception as e:
            last_error = e
            time.sleep(2)
    raise RuntimeError(
        "Could not reach the AI. Check your internet (try a phone hotspot) and click the button again. "
        f"Details: {last_error}"
    )


def get_json(text):
    """Remove ``` fences and convert the answer into a Python dict."""
    text = re.sub(r"```json|```", "", text).strip()
    start, end = text.find("{"), text.rfind("}")
    return json.loads(text[start:end + 1])


def js_text(text):
    """Make text safe to put inside JavaScript."""
    return json.dumps(text).replace("</", "<\\/")


def parse_date(value):
    """Turn 'YYYY-MM-DD' into a date. Returns None if it is not a valid date."""
    try:
        return datetime.strptime(str(value).strip(), "%Y-%m-%d").date()
    except Exception:
        return None


def ics_escape(text):
    """Make text safe for a calendar file."""
    return (
        str(text)
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r", "")
        .replace("\n", "\\n")
    )


def make_ics(title, deadline, details):
    """Build a calendar file with an all-day deadline and alerts 3 days and 1 day before."""
    start = deadline.strftime("%Y%m%d")
    end = (deadline + timedelta(days=1)).strftime("%Y%m%d")
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Notice Saathi//EN",
        "CALSCALE:GREGORIAN",
        "BEGIN:VEVENT",
        f"UID:{uuid.uuid4()}@noticesaathi",
        f"DTSTAMP:{stamp}",
        f"DTSTART;VALUE=DATE:{start}",
        f"DTEND;VALUE=DATE:{end}",
        f"SUMMARY:{ics_escape('Deadline: ' + title)}",
        f"DESCRIPTION:{ics_escape(details)}",
        "BEGIN:VALARM",
        "TRIGGER:-P3D",
        "ACTION:DISPLAY",
        "DESCRIPTION:Deadline in 3 days",
        "END:VALARM",
        "BEGIN:VALARM",
        "TRIGGER:-P1D",
        "ACTION:DISPLAY",
        "DESCRIPTION:Deadline tomorrow",
        "END:VALARM",
        "END:VEVENT",
        "END:VCALENDAR",
    ]
    return "\r\n".join(lines) + "\r\n"


def countdown_badge(deadline_date):
