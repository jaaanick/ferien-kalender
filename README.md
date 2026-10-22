# ferien-kalender

Ferienplaner und Abo-Kalender (ICS) mit meinen Ferientagen.

- Ferienplaner: https://jaaanick.github.io/ferien-kalender/ (GitHub Pages, `index.html`)
- Abo-Link: webcal://raw.githubusercontent.com/jaaanick/ferien-kalender/main/ferien-janick.ics

Ablauf:

- Der Ferienplaner speichert pro Jahr eine Datei `data/JAHR.json` (`{"days": {"2027-04-01": "FE"}, "guthaben": 25, "updated": "..."}`) über die GitHub-API. Zum Bearbeiten braucht er pro Gerät einmal einen Fine-grained Token mit «Contents: Read and write» nur für dieses Repo.
- Bei jeder Änderung in `data/` erzeugt die GitHub Action `.github/workflows/ics.yml` mit `build_ics.py` die Datei `ferien-janick.ics` neu.
- Codes: FE = Ferientag (08:00–17:00), FG = geschenkt (08:00–17:00), FEM = frei morgens (08:00–12:00), FEN = frei nachmittags (13:00–17:00). In Outlook als abwesend markiert.
