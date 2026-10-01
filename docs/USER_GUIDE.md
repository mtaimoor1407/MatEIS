# User guide

## 1. Start the app
Run `streamlit run app.py` (or open the deployed link). The page has four tabs: **Select materials**, **Database**, **History**, **Guide**. The constraint panel is on the left.

## 2. Find the best material (worked example)
*Goal: the lightest beam that is stiff, with yield strength of at least 200 MPa.*

1. In the sidebar open **Strength (MPa)** and type `200` in **Min**. The ranked list updates at once.
2. On the **Select materials** tab choose the objective **Light, stiff beam**. The panel shows M = E^½ / ρ.
3. Read the result cards: best material, its index value, and how many materials remain.
4. Study the chart. The red star is the best material, the dashed line is the line of constant M through it, and points above and left of the line beat it. Grey points were excluded by your constraints.
5. Scroll to **Ranked materials** for the full table and open **Material details** for specific stiffness, specific strength, source and verification status.

## 3. Constraints
| Control | Meaning |
|---|---|
| Material classes | Tick the classes to include. At least one is required. |
| Min / Max boxes | Inclusive limits. Leave empty for "no limit". Negative numbers are not accepted. |
| Reset all constraints | Clears everything. |

If **min is greater than max**, a red message appears in the sidebar and the results wait until you fix it. If **no material qualifies**, you get a warning and a grey chart so you can see what was excluded.

## 4. Chart options
Open **Chart options** to switch to **Custom axes** (any two properties, for example Strength vs Cost per kg) or to hide the class envelopes. The guide line is shown only when the axes match the objective, because that is the only chart on which the line is straight.

## 5. Export and save
- **Download CSV**: the ranked table.
- **Build PDF report**, then **Download PDF report**: two A4 pages with objective, constraints, recommended material, Ashby chart and top-ranked table.
- **Save to history**: stores the analysis in SQLite; see the **History** tab.

## 6. Manage materials (Database tab)
- **Add a material**: fill in all fields. Values are checked (for example density must be 1–25,000 kg/m³); mistakes show a clear message.
- **Edit or delete**: pick a material, change fields, tick **Data verified** once you checked it against its source, then **Save changes**. Deleting needs a confirmation tick.
- **Reset**: restores the original 26 materials.

## 7. Troubleshooting
| Problem | Fix |
|---|---|
| Blank results | Relax a constraint or select more classes. |
| "A material named … already exists" | Material names are unique; rename it. |
| Added materials vanished on the hosted app | Free hosting resets files on restart; add permanent data to `scripts/build_seed.py`. |
| PDF button missing | Click **Build PDF report** first; the download button appears next to it. |
