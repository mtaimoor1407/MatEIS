# Presentation outline (8–10 minutes, 9 slides)

1. **Title** – MatEIS Select; team names, registration numbers, session years, instructor.
2. **The problem** – Engineers must choose among thousands of materials. Picking by habit wastes mass and money. Example: a bicycle frame, a drone arm.
3. **Our solution** – One sentence pitch plus a screenshot: *enter constraints, choose an objective, get a ranked, explained answer.*
4. **The science** – Performance indices (E^½/ρ, σy^⅔/ρ, cost variants), why the guide line has slope 1/p. Show one derivation line: beam mass minimised → index.
5. **Architecture** – The diagram from `docs/ARCHITECTURE.md`; say "core has no UI code, so it is fully testable."
6. **Data** – 26 materials, four classes, cited sources, verification sheet. Be upfront: typical values, ceramics use flexural strength.
7. **Live demo** (3 min) – Script below.
8. **Quality** – 166 tests, boundary cases, error handling, ruff, deployed link.
9. **Limitations and next steps** – Add temperature, toughness, more materials, multi-objective trade-off, user accounts. Q&A.

## Live demo script
1. Open the deployed link. Say what the four tabs do.
2. Type **200** as minimum strength → candidates drop. Point at grey points.
3. Choose **Light, stiff beam** → show formula, star and guide line. Explain what "above the line" means.
4. Switch to **Cheap, strong beam** → the winner changes from a composite to a steel. Explain why cost changes the answer.
5. Enter an impossible strength (50000) → friendly warning, nothing crashes.
6. Enter min 100, max 10 → error message.
7. Build the PDF, open it.
8. Database tab → add a material, show a validation error for a negative density, then fix and save.

## Likely questions (prepare answers)
- *Why does a ceramic win some strength rankings?* Flexural strength is not yield strength; the app warns about it. Ceramics are brittle, so toughness would rule them out; our indices do not model that yet.
- *Where do the numbers come from?* Callister App. B and MatWeb typical values; each row verified by a team member.
- *Why not FastAPI/React?* Single user, single runtime; extra layers add risk without adding requirements.
- *How do you know the guide line is right?* A test checks that M is constant at every point of the line.
