# Requirements traceability

Every line of the project document, and where it is satisfied.

## Project requirements
| Requirement (document) | Evidence |
|---|---|
| Python GUI application (desktop or web) | `app.py`, Streamlit web app |
| Practical materials-engineering problem / interactive tool | Theme 2: Ashby selection tool |
| Teams of 2–3 (1 from 2024, 1 from 2023, 1–2 from 2026) | Fill in team names in `README.md` |
| Standard libraries (numpy, pandas, matplotlib, Streamlit etc.) | `requirements.txt` |

## Theme 2 core features
| Core feature | Evidence |
|---|---|
| Built-in database of **at least 15** materials (metals, polymers, ceramics, composites) with density, Young's modulus, yield strength, cost | 26 materials in `data/materials_seed.json`; test `test_at_least_15_materials_and_all_four_classes` |
| User input filters for constraints (e.g. yield strength > 200 MPa) | Sidebar; `core/filters.py`; test `test_document_example_yield_above_200` |
| Interactive plot comparing two properties, highlighting the optimal material for a performance index | `ui/plots.py`; Custom axes option; star marker + guide line |

## Timeline items
| Item | Evidence |
|---|---|
| Define formulas (Ashby indices); numpy/pandas backend | `core/indices.py`, `docs/ARCHITECTURE.md` |
| GUI in Streamlit; matplotlib charts | `ui/`, `core/report.py` (matplotlib static chart in PDF) |
| Connect UI to backend; JSON or sqlite3 storage | `core/database.py` (SQLite, seeded from JSON); History table |
| Boundary-value testing | `tests/` (166 tests; e.g. `test_numeric_boundaries`, `test_min_greater_than_max_shows_error_not_crash`) |
| Refactor, documentation, user guide, presentation | `README.md`, `docs/` |

## Grading rubric
| Criterion (weight) | How it is met |
|---|---|
| Materials science accuracy (30%) | Correct Ashby indices and guide-line maths with tests; cited data; `docs/DATA_VERIFICATION.md` sign-off; strength-basis caveat for ceramics |
| Code architecture and logic (25%) | OOP `Material` / `MaterialDatabase` / `PerformanceIndex`; `core/` has no UI code; numpy + pandas + matplotlib; custom exceptions; ruff-clean |
| UI/UX and functionality (15%) | Sidebar constraints, tabs, friendly errors, empty-result handling, exports |
| Documentation and comments (10%) | README, user guide, architecture, docstrings, comments |
| Final presentation and demo (10%) | `docs/PRESENTATION_OUTLINE.md`, live deployed link |
| Video documentation (10%) | `docs/VIDEO_SCRIPT.md` |
