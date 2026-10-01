"""Streamlit page renderers. Pure presentation: all logic lives in ``core/``."""
from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from core.database import MaterialDatabase
from core.exceptions import MatEISError, ValidationError
from core.filters import Constraints, apply_constraints
from core.indices import INDICES, rank_materials
from core.material import Material
from core.properties import CLASS_COLORS, MATERIAL_CLASSES, PROPERTIES, STRENGTH_BASES
from core.report import csv_bytes, pdf_report
from ui.plots import ashby_figure

FILTER_WIDGETS = [  # (property key, step)
    ("strength", 10.0), ("modulus", 5.0), ("density", 0.5), ("cost", 1.0),
]
STATE_KEYS = [f"f_{k}_{b}" for k, _ in FILTER_WIDGETS for b in ("min", "max")] + ["f_classes"]


# --------------------------------------------------------------------------- sidebar
def _reset_filters() -> None:
    for key in STATE_KEYS:
        st.session_state[key] = list(MATERIAL_CLASSES) if key == "f_classes" else None


def render_sidebar() -> Constraints | None:
    """Draw the constraint widgets and return validated Constraints (or None if invalid)."""
    st.sidebar.header("Design constraints")
    st.sidebar.caption("Leave a box empty for no limit. Limits are inclusive (≥ min, ≤ max).")
    classes = st.sidebar.multiselect("Material classes", MATERIAL_CLASSES,
                                     default=list(MATERIAL_CLASSES), key="f_classes")
    ranges: dict[str, tuple] = {}
    for key, step in FILTER_WIDGETS:
        prop = PROPERTIES[key]
        with st.sidebar.expander(f"{prop.label} ({prop.unit})", expanded=(key == "strength")):
            c1, c2 = st.columns(2)
            low = c1.number_input("Min", min_value=0.0, value=None, step=step,
                                  placeholder="no limit", key=f"f_{key}_min")
            high = c2.number_input("Max", min_value=0.0, value=None, step=step,
                                   placeholder="no limit", key=f"f_{key}_max")
            ranges[key] = (low, high)
    st.sidebar.button("Reset all constraints", on_click=_reset_filters, width="stretch")
    constraints = Constraints(classes=tuple(classes), ranges=ranges)
    try:
        return constraints.validate()
    except ValidationError as exc:
        st.sidebar.error(str(exc))
        return None


# --------------------------------------------------------------------------- select page
def render_select(db: MaterialDatabase, constraints: Constraints | None) -> None:
    df = db.to_dataframe()
    if df.empty:
        st.warning("The materials database is empty. Add materials in the **Database** tab.")
        return

    st.subheader("1. Choose a design objective")
    key = st.selectbox("Objective", list(INDICES), format_func=lambda k: INDICES[k].label,
                       key="index_key")
    index = INDICES[key]
    st.markdown(f"Performance index **M = `{index.formula}`**  ·  units: `{index.unit}`  ·  "
                f"{index.use_case} **Higher M is better.**")

    if constraints is None:
        st.warning("Fix the constraint error shown in the sidebar to see results.")
        return

    filtered = apply_constraints(df, constraints)
    ranked = rank_materials(filtered, index)

    st.subheader("2. Result")
    if ranked.empty:
        st.warning("No material meets every constraint. Relax a limit or add a material class. "
                   "Grey points below show what was excluded.")
    else:
        best = ranked.iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.metric("Best material", best["name"])
        c2.metric(f"Index M ({index.formula})", f"{best['index_value']:.3g}")
        c3.metric("Candidates left", f"{len(ranked)} of {len(df)}")
        if len(ranked) > 1:
            second = ranked.iloc[1]
            st.caption(f"Runner-up: **{second['name']}** (M = {second['index_value']:.3g}, "
                       f"{second['index_value'] / best['index_value']:.0%} of the best).")

    with st.expander("Chart options", expanded=False):
        mode = st.radio("Axes", ["Match the index (shows the guide line)", "Custom axes"],
                        horizontal=True, key="axes_mode")
        x_key, y_key = index.axes
        if mode == "Custom axes":
            keys = list(PROPERTIES)
            a, b = st.columns(2)
            x_key = a.selectbox("X axis", keys, index=keys.index("density"),
                                format_func=lambda k: PROPERTIES[k].axis_label, key="x_axis")
            y_key = b.selectbox("Y axis", keys, index=keys.index("modulus"),
                                format_func=lambda k: PROPERTIES[k].axis_label, key="y_axis")
        show_hulls = st.checkbox("Show class envelopes", value=True, key="hulls")

    fig = ashby_figure(df, ranked, index, x_key, y_key, show_hulls=show_hulls)
    st.plotly_chart(fig, width="stretch")
    st.caption("Log-log Ashby chart. The dashed line has constant M and passes through the best "
               "material: points above and left of it perform better. Grey = excluded by constraints.")

    if ranked.empty:
        return

    if index.numerator == "strength" and (ranked["strength_basis"] != "yield").any():
        st.info("Ceramics, some polymers and composites have no true yield point; their tensile or "
                "flexural strength is used (column *Basis*). Treat strength rankings across classes with care.")

    st.subheader("3. Ranked materials")
    table = ranked[["rank", "name", "material_class", "density", "modulus", "strength",
                    "strength_basis", "cost", "index_value", "verified"]]
    st.dataframe(
        table, hide_index=True, width="stretch",
        column_config={
            "rank": st.column_config.NumberColumn("#", width="small"),
            "name": "Material", "material_class": "Class",
            "density": st.column_config.NumberColumn("Density (Mg/m³)", format="%.2f"),
            "modulus": st.column_config.NumberColumn("E (GPa)", format="%.3g"),
            "strength": st.column_config.NumberColumn("Strength (MPa)", format="%.4g"),
            "strength_basis": "Basis",
            "cost": st.column_config.NumberColumn("Cost (USD/kg)", format="%.3g"),
            "index_value": st.column_config.NumberColumn(f"M = {index.formula}", format="%.3g"),
            "verified": st.column_config.CheckboxColumn("Data verified"),
        })

    st.subheader("4. Export and save")
    sig = json.dumps([key, constraints.to_dict()], sort_keys=True)
    b1, b2, b3 = st.columns(3)
    b1.download_button("Download CSV", csv_bytes(ranked), file_name="mateis_ranking.csv",
                       mime="text/csv", width="stretch")
    if b2.button("Build PDF report", width="stretch"):
        with st.spinner("Rendering report…"):
            st.session_state["pdf"] = (sig, pdf_report(df, ranked, index, constraints))
    cached = st.session_state.get("pdf")
    if cached and cached[0] == sig:
        b2.download_button("Download PDF report", cached[1], file_name="mateis_report.pdf",
                           mime="application/pdf", width="stretch")
    if b3.button("Save to history", width="stretch"):
        best = ranked.iloc[0]
        db.log_analysis(key, constraints.to_dict(), len(ranked), best["name"], float(best["index_value"]))
        st.success("Analysis saved. See the History tab.")

    with st.expander("Material details"):
        choice = st.selectbox("Material", ranked["name"].tolist(), key="detail_choice")
        row = ranked[ranked["name"] == choice].iloc[0]
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Density", f"{row['density']:.2f} Mg/m³")
        d2.metric("Young's modulus", f"{row['modulus']:.3g} GPa")
        d3.metric(f"Strength ({row['strength_basis']})", f"{row['strength']:.4g} MPa")
        d4.metric("Cost", f"{row['cost']:.3g} USD/kg")
        st.write(f"**Class:** {row['material_class']}  ·  **Specific stiffness E/ρ:** "
                 f"{row['modulus'] / row['density']:.3g}  ·  **Specific strength σ/ρ:** "
                 f"{row['strength'] / row['density']:.3g}")
        st.write(f"**Source:** {row['source'] or '—'}  ·  **Verified:** {'yes' if row['verified'] else 'not yet'}")
        if row["notes"]:
            st.write(row["notes"])


# --------------------------------------------------------------------------- database page
def _material_form(prefix: str, m: Material | None = None) -> dict:
    """Shared add/edit field set. Returns the raw values entered."""
    a, b = st.columns([2, 1])
    name = a.text_input("Name", value=m.name if m else "", key=f"{prefix}_name")
    cls = b.selectbox("Class", MATERIAL_CLASSES, key=f"{prefix}_class",
                      index=MATERIAL_CLASSES.index(m.material_class) if m else 0)
    c1, c2, c3, c4 = st.columns(4)
    rho = c1.number_input("Density (kg/m³)", min_value=0.0, value=m.density_kg_m3 if m else None, key=f"{prefix}_rho")
    e = c2.number_input("Young's modulus (GPa)", min_value=0.0, value=m.youngs_modulus_gpa if m else None, key=f"{prefix}_e")
    s = c3.number_input("Strength (MPa)", min_value=0.0, value=m.yield_strength_mpa if m else None, key=f"{prefix}_s")
    cost = c4.number_input("Cost (USD/kg)", min_value=0.0, value=m.cost_usd_per_kg if m else None, key=f"{prefix}_c")
    basis = st.selectbox("Strength basis", STRENGTH_BASES, key=f"{prefix}_basis",
                         index=STRENGTH_BASES.index(m.strength_basis) if m else 0)
    source = st.text_input("Source (book, page, or URL)", value=m.source if m else "", key=f"{prefix}_src")
    notes = st.text_area("Notes", value=m.notes if m else "", key=f"{prefix}_notes")
    return dict(name=name, material_class=cls, density_kg_m3=rho, youngs_modulus_gpa=e,
                yield_strength_mpa=s, cost_usd_per_kg=cost, strength_basis=basis, source=source, notes=notes)


def render_database(db: MaterialDatabase, seed_path) -> None:
    df = db.to_dataframe()
    st.subheader("Materials database")
    n_ver = int(df["verified"].sum()) if not df.empty else 0
    st.caption(f"{len(df)} materials · {n_ver} marked as verified against a reference. "
               "Data are stored in SQLite (`data/materials.db`).")
    if not df.empty:
        st.dataframe(df[["name", "material_class", "density", "modulus", "strength", "strength_basis",
                         "cost", "source", "verified"]], hide_index=True, width="stretch",
                     column_config={"density": "Density (Mg/m³)", "modulus": "E (GPa)",
                                    "strength": "Strength (MPa)", "cost": "Cost (USD/kg)",
                                    "strength_basis": "Basis", "material_class": "Class",
                                    "name": "Material", "source": "Source",
                                    "verified": st.column_config.CheckboxColumn("Verified")})
        st.download_button("Download database as CSV", df.drop(columns=["id"]).to_csv(index=False).encode("utf-8-sig"),
                           file_name="mateis_materials.csv", mime="text/csv")

    with st.expander("Add a material"):
        values = _material_form("add")
        if st.button("Add material", key="add_btn"):
            try:
                added = db.add(Material(**values))
                st.success(f"Added {added.name}.")
                st.rerun()
            except MatEISError as exc:
                st.error(str(exc))

    if not df.empty:
        with st.expander("Edit or delete a material"):
            names = {f"{r['name']}": int(r["id"]) for _, r in df.iterrows()}
            pick = st.selectbox("Material", list(names), key="edit_pick")
            mid = names[pick]
            current = db.get(mid)
            values = _material_form(f"edit_{mid}", current)
            verified = st.checkbox("Data verified against the cited source", value=current.verified, key=f"ver_{mid}")
            c1, c2 = st.columns(2)
            if c1.button("Save changes", key=f"save_{mid}"):
                try:
                    db.update(mid, Material(**values, verified=verified))
                    st.success("Saved.")
                    st.rerun()
                except MatEISError as exc:
                    st.error(str(exc))
            confirm = c2.checkbox("I want to delete this material", key=f"del_ok_{mid}")
            if c2.button("Delete material", key=f"del_{mid}", disabled=not confirm):
                db.delete(mid)
                st.success("Deleted.")
                st.rerun()

    with st.expander("Reset to the original 26 materials"):
        st.write("Replaces every material with the original dataset. History is kept.")
        ok = st.checkbox("Yes, replace the current materials", key="reset_ok")
        if st.button("Reset database", disabled=not ok, key="reset_btn"):
            try:
                db.seed_from_json(seed_path, replace=True)
                st.success("Database reset.")
                st.rerun()
            except MatEISError as exc:
                st.error(str(exc))


# --------------------------------------------------------------------------- history & guide
def render_history(db: MaterialDatabase) -> None:
    st.subheader("Saved analyses")
    hist = db.get_history()
    if hist.empty:
        st.info("Nothing saved yet. Use **Save to history** on the Select tab to keep a record of an analysis.")
        return
    hist = hist.assign(index_key=hist["index_key"].map(lambda k: INDICES[k].label if k in INDICES else k))
    st.dataframe(hist, hide_index=True, width="stretch", column_config={
        "created_at": "Saved at", "index_key": "Objective", "constraints": "Constraints (JSON)",
        "n_candidates": "Candidates", "top_material": "Best material",
        "top_value": st.column_config.NumberColumn("Best M", format="%.3g")})
    if st.button("Clear history"):
        db.clear_history()
        st.rerun()


def render_guide() -> None:
    st.subheader("How to use MatEIS Select")
    st.markdown(
        """
1. **Set constraints** in the sidebar, for example *Strength min = 200 MPa*.
2. **Pick a design objective** (what you want to minimise: mass or cost, for which loading case).
3. **Read the chart**: the red star is the best material; the dashed line is the performance-index guide line.
4. **Check the ranked table**, open *Material details*, then **export** a CSV or PDF report.
5. Use the **Database** tab to add, edit, verify or delete materials.
        """)
    st.subheader("Performance indices")
    st.markdown("Each index is built so that a **larger value is better**. "
                "Derivations follow Ashby, *Materials Selection in Mechanical Design*.")
    st.dataframe(pd.DataFrame([{"Objective": i.label, "Index": i.formula, "Units": i.unit,
                                "Guide-line slope": f"{i.guide_slope:g}", "Use": i.use_case}
                               for i in INDICES.values()]), hide_index=True, width="stretch")
    st.subheader("Limitations")
    st.markdown(
        """
- Values are **typical room-temperature figures**; real properties vary with processing, heat treatment and grade.
- Ceramic strength is **flexural strength**; composites are **anisotropic** (properties given along the fibre direction or quasi-isotropic in plane).
- Cost is an **indicative raw-material price** and changes with the market.
- The indices ignore toughness, fatigue, corrosion, temperature and manufacturability; use the results to **shortlist**, not to finalise a design.
        """)
    legend = " · ".join(f"<span style='color:{c}'>●</span> {k}" for k, c in CLASS_COLORS.items())
    st.markdown(f"Class colours: {legend}", unsafe_allow_html=True)
