# MatEIS Select – Materials Selection & Ashby Plotter

**Course:** CSC-214 MATLAB and Python – CEP/OEL · **Theme 2:** Materials Selection & Ashby Plotter
**Instructor:** Dr.-Ing. Waseem Amin · **Team:** _add names and registration numbers here_

MatEIS Select is a web app for design engineers. You enter design constraints (for example *yield strength ≥ 200 MPa*), pick a design objective (for example *light, stiff beam*), and the app ranks 26 engineering materials by the matching **Ashby performance index**, draws an interactive log-log Ashby chart with the best material highlighted, and exports a CSV or PDF report.

<!-- Add a screenshot: save it as docs/screenshot.png and uncomment the next line -->
<!-- ![MatEIS Select screenshot](docs/screenshot.png) -->

## Features

| Feature | Where |
|---|---|
| 26 materials (metals, polymers, ceramics, composites) with density, Young's modulus, strength, cost and a cited source | `data/materials_seed.json`, SQLite `data/materials.db` |
| Constraint filters on class, strength, modulus, density, cost (min/max, inclusive) | sidebar |
| 9 performance indices (light/cheap × stiff/strong × tie/beam/plate) with live formula and units | *Select materials* tab |
| Interactive Plotly Ashby chart: class envelopes, excluded points in grey, guide line, best material starred | *Select materials* tab |
| Ranked table, material detail view, runner-up comparison | *Select materials* tab |
| CSV export and PDF report (matplotlib chart + ranked table) | *Export and save* |
| Add / edit / delete / verify materials, reset to original data | *Database* tab |
| History of saved analyses (SQLite) | *History* tab |
| In-app user guide and limitations | *Guide* tab |
| 166 automated tests including boundary-value tests | `tests/` |

## Install and run

Requires Python 3.11 or newer.

```bash
git clone <your-repo-url> matEIS
cd matEIS
python -m venv .venv
# Windows:  .venv\Scripts\activate        macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501. The database is created and filled automatically on first run.

## Run the tests

```bash
pip install -r requirements-dev.txt
pytest -q          # 166 tests, about 6 seconds
ruff check .       # style and lint
```

## Deploy (free, about 5 minutes)

1. Create a GitHub repository and push this folder (the `data/materials.db` file is git-ignored; it is rebuilt from the JSON).
2. Go to <https://share.streamlit.io>, sign in with GitHub, choose **Create app**, select the repository and branch, and set the main file path to `app.py`.
3. In advanced settings choose Python 3.12 (or 3.11) and deploy. Paste the public URL into this README and your presentation.

Note: free hosting has a temporary file system. Materials you add in the live app can disappear when the app restarts; the original 26 always return from the JSON seed. For permanent changes, edit `scripts/build_seed.py` and regenerate the JSON.
Alternative hosts: Hugging Face Spaces (Streamlit SDK) or Render.

## Project structure

```
app.py                  Streamlit entry point (wiring only)
core/                   Business logic, no UI code
  properties.py         Property keys, units, colours (single source of truth)
  material.py           Material dataclass with validation
  database.py           SQLite access (materials + history), all SQL lives here
  filters.py            Constraints + apply_constraints
  indices.py            PerformanceIndex, ranking, guide-line maths
  report.py             CSV and PDF export (matplotlib)
  exceptions.py         Custom exceptions
ui/
  pages.py              Page renderers (sidebar, tabs)
  plots.py              Plotly Ashby chart
data/materials_seed.json  Source data (edit via scripts/build_seed.py)
scripts/build_seed.py   Generates the JSON from one readable table
tests/                  pytest suite
docs/                   User guide, architecture, verification sheet, presentation, video script
```

See `docs/ARCHITECTURE.md` for the design and `docs/USER_GUIDE.md` for step-by-step usage.

## The science in one paragraph

A performance index M combines properties so that a larger M always means a better material for an objective. For a light, stiff beam, M = E^½/ρ; for a light, strong beam, M = σy^⅔/ρ; replacing density ρ with cost per volume gives the cheapest material instead. On a log-log chart of E (or σy) against ρ, all materials with the same M lie on a straight line of slope 1/p, so a single guide line drawn through the best material shows which materials beat it. This follows M. F. Ashby, *Materials Selection in Mechanical Design*.

## Data sources and honesty about accuracy

Values are typical room-temperature figures from Callister & Rethwisch (*Materials Science and Engineering*, Appendix B), MatWeb typical-property pages and Ashby. They vary with grade, processing and test method. Costs are indicative raw-material prices. Every row starts as **unverified**; `docs/DATA_VERIFICATION.md` lists how the team checked each one. The commercial Ashby (CES) database is proprietary and was not copied.

## Limitations

- Indices ignore toughness, fatigue, corrosion, temperature and manufacturability; results are a shortlist.
- Ceramic strength is flexural strength; composites are anisotropic.
- Single-user app without authentication.
