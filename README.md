# ferien-kalender

Abo-Kalender (ICS) mit meinen Ferientagen.

Abo-Link: webcal://raw.githubusercontent.com/jaaanick/ferien-kalender/main/ferien-janick.ics

- Quelle: mein Ferienplaner (Claude-Artifact). Eine geplante Aufgabe exportiert die Daten täglich und aktualisiert `ferien-janick.ics`.
- `build_ics.py` erzeugt die Datei aus den exportierten `JAHR.json`-Dateien.
- Termine: ganztägig «Ferien Janick» (bzw. «(geschenkt)»), in Outlook als abwesend markiert. Aufeinanderfolgende Ferientage werden zu einem Termin zusammengefasst.
