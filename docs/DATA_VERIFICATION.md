# Data verification sheet

**Why this matters:** 30% of the grade is *Materials Science Accuracy*. The values in `data/materials_seed.json` are typical textbook figures. Before submission, each row must be checked against its cited reference by a team member.

**How to verify a row**

1. Open the reference named in *Source* (Callister Appendix B, MatWeb search, or Ashby).
2. Compare density, modulus, strength and (loosely) cost. Small differences are normal; they depend on grade, temper and test method.
3. If your reference differs by more than a few percent, edit `scripts/build_seed.py`, run `python scripts/build_seed.py`, and use *Database → Reset* in the app (or delete `data/materials.db`).
4. Tick the box below and tell the app: *Database → Edit or delete → Data verified*.
5. Write the reference page number in the *Checked against* column. Your instructor can then see where each number came from.

| ✔ | Material | Class | ρ kg/m³ | E GPa | σ MPa (basis) | Cost USD/kg | Cited source | Checked against (page/URL) | Verified by |
|---|---|---|---|---|---|---|---|---|---|
| ☐ | AISI 1020 Steel (hot rolled) | Metal | 7870 | 207 | 350 (yield) | 0.8 | MatWeb typical properties |  |  |
| ☐ | AISI 304 Stainless Steel (annealed) | Metal | 8000 | 193 | 215 (yield) | 3.5 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | AISI 4140 Steel (normalized) | Metal | 7850 | 205 | 655 (yield) | 1.5 | MatWeb typical properties |  |  |
| ☐ | Ductile Iron 65-45-12 | Metal | 7100 | 169 | 310 (yield) | 1 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | Aluminum 6061-T6 | Metal | 2700 | 69 | 275 (yield) | 3 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | Aluminum 7075-T6 | Metal | 2810 | 72 | 503 (yield) | 4.5 | MatWeb typical properties |  |  |
| ☐ | Titanium Ti-6Al-4V (annealed) | Metal | 4430 | 114 | 880 (yield) | 35 | MatWeb typical properties |  |  |
| ☐ | Copper C11000 (annealed) | Metal | 8940 | 110 | 69 (yield) | 9 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | Brass 70Cu-30Zn (annealed) | Metal | 8530 | 110 | 75 (yield) | 7 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | Magnesium AZ31B (extruded) | Metal | 1770 | 45 | 200 (yield) | 4.5 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | Inconel 718 (aged) | Metal | 8190 | 200 | 1034 (yield) | 40 | MatWeb typical properties |  |  |
| ☐ | HDPE | Polymer | 960 | 1 | 26 (yield) | 1.3 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | Polypropylene (PP) | Polymer | 905 | 1.5 | 35 (yield) | 1.4 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | Nylon 6,6 (dry) | Polymer | 1140 | 2.8 | 55 (yield) | 3.5 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | PMMA (acrylic) | Polymer | 1190 | 3 | 70 (tensile) | 2.5 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | PEEK | Polymer | 1300 | 3.6 | 100 (yield) | 90 | MatWeb typical properties |  |  |
| ☐ | PVC (rigid) | Polymer | 1400 | 3 | 45 (yield) | 1.3 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | Polycarbonate (PC) | Polymer | 1200 | 2.4 | 62 (yield) | 3.5 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | Alumina Al2O3 (99.5%) | Ceramic | 3890 | 375 | 380 (flexural) | 15 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | Silicon Carbide (sintered) | Ceramic | 3100 | 410 | 450 (flexural) | 20 | MatWeb typical properties |  |  |
| ☐ | Silicon Nitride (hot pressed) | Ceramic | 3300 | 304 | 700 (flexural) | 50 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | Zirconia Y-TZP | Ceramic | 6050 | 205 | 900 (flexural) | 40 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | Soda-Lime Glass | Ceramic | 2500 | 69 | 69 (flexural) | 1 | Callister & Rethwisch, Materials Science and Engineering, App. B |  |  |
| ☐ | CFRP unidirectional (0 deg) | Composite | 1600 | 135 | 1500 (tensile) | 60 | Ashby, Materials Selection in Mechanical Design |  |  |
| ☐ | CFRP quasi-isotropic | Composite | 1550 | 60 | 550 (tensile) | 60 | Ashby, Materials Selection in Mechanical Design |  |  |
| ☐ | GFRP (E-glass / epoxy) | Composite | 1900 | 25 | 350 (tensile) | 6 | Ashby, Materials Selection in Mechanical Design |  |  |

**Cost column:** costs are indicative raw-material prices, not quotes. State this in your presentation.

**Strength basis:** ceramics use flexural strength and some polymers/composites use tensile strength because they have no true yield point. The app shows this in the *Basis* column and warns the user.
