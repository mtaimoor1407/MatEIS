"""MatEIS Select – Materials Selection & Ashby Plotter (Streamlit entry point).

Run locally:   streamlit run app.py
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.database import MaterialDatabase  # noqa: E402
from core.exceptions import DatabaseError  # noqa: E402
from ui.pages import render_database, render_guide, render_history, render_select, render_sidebar  # noqa: E402

SEED_PATH = ROOT / "data" / "materials_seed.json"
DB_PATH = Path(os.environ.get("MATEIS_DB_PATH", ROOT / "data" / "materials.db"))

st.set_page_config(page_title="MatEIS Select", page_icon="⚙️", layout="wide")


@st.cache_resource(show_spinner=False)
def get_database() -> MaterialDatabase:
    """Open (and seed on first run) the SQLite database; fall back to a temp file if read-only."""
    try:
        db = MaterialDatabase(DB_PATH)
    except (DatabaseError, OSError):
        db = MaterialDatabase(Path(tempfile.gettempdir()) / "mateis_materials.db")
    if db.count() == 0:
        db.seed_from_json(SEED_PATH)
    return db


def main() -> None:
    st.title("MatEIS Select")
    st.caption("Materials Engineering Interactive Suite · pick the right material for a design "
               "objective with Ashby charts and performance indices.")
    try:
        db = get_database()
    except DatabaseError as exc:
        st.error(f"Could not open the materials database: {exc}")
        st.stop()
    constraints = render_sidebar()
    tab_select, tab_db, tab_hist, tab_guide = st.tabs(["Select materials", "Database", "History", "Guide"])
    with tab_select:
        render_select(db, constraints)
    with tab_db:
        render_database(db, SEED_PATH)
    with tab_hist:
        render_history(db)
    with tab_guide:
        render_guide()


main()
