# ferien-kalender

Abo-Kalender (ICS) mit meinen Ferientagen.

Abo-Link: webcal://raw.githubusercontent.com/jaaanick/ferien-kalender/main/ferien-janick.ics

- Quelle: mein Ferienplaner (Claude-Artifact). Eine geplante Aufgabe exportiert die Daten täglich und aktualisiert `ferien-janick.ics`.
- `build_ics.py` erzeugt die Datei aus den exportierten `JAHR.json`-Dateien.
- Termine: jeder Ferientag einzeln 08:00–17:00 «Ferien Janick» (bzw. «(geschenkt)»), frei morgens 08:00–12:00, frei nachmittags 13:00–17:00; in Outlook als abwesend markiert.
