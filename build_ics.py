#!/usr/bin/env python3
"""Erzeugt ferien-janick.ics aus den exportierten Ferienplaner-Daten.

Aufruf: python3 build_ics.py <ordner-mit-JAHR.json> [ausgabe.ics]
Jede JAHR.json hat die Form {"days": {"2027-04-01": "FE"}, "guthaben": 25, "updated": "..."}.
Codes: FE = Ferientag (08:00-17:00), FG = Ferientag geschenkt (08:00-17:00),
       FEM = frei morgens (08:00-12:00), FEN = frei nachmittags (13:00-17:00).
Jeder Tag wird ein eigener Termin (Zeitzone Europe/Zurich).
"""
import json, sys, datetime as dt
from pathlib import Path

TIMES = {"FE": ("0800", "1700"), "FG": ("0800", "1700"), "FEM": ("0800", "1200"), "FEN": ("1300", "1700"),
         # aeltere Codes (halbe Tage ohne Tageszeit) als Vormittag behandeln
         "FEH": ("0800", "1200"), "FGH": ("0800", "1200")}
SUMMARY = {"FE": "Ferien Janick", "FG": "Ferien Janick (geschenkt)", "FEM": "Ferien Janick (Vormittag)",
           "FEN": "Ferien Janick (Nachmittag)", "FEH": "Ferien Janick (Vormittag)", "FGH": "Ferien Janick (Vormittag, geschenkt)"}
DESC = {"FE": "Ferientag", "FG": "Ferientag (geschenkt)", "FEM": "Halber Ferientag: frei morgens",
        "FEN": "Halber Ferientag: frei nachmittags", "FEH": "Halber Ferientag", "FGH": "Halber Ferientag (geschenkt)"}
VTIMEZONE = ["BEGIN:VTIMEZONE", "TZID:Europe/Zurich",
             "BEGIN:DAYLIGHT", "TZOFFSETFROM:+0100", "TZOFFSETTO:+0200", "TZNAME:CEST",
             "DTSTART:19700329T020000", "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU", "END:DAYLIGHT",
             "BEGIN:STANDARD", "TZOFFSETFROM:+0200", "TZOFFSETTO:+0100", "TZNAME:CET",
             "DTSTART:19701025T030000", "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU", "END:STANDARD",
             "END:VTIMEZONE"]


def main():
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).with_name("ferien-janick.ics")
    days, stamps = {}, []
    for f in sorted(src.glob("*.json")):
        if not f.stem.isdigit():
            continue
        doc = json.loads(f.read_text(encoding="utf-8"))
        for k, v in (doc.get("days") or {}).items():
            if v in TIMES:
                days[dt.date.fromisoformat(k)] = v
        if doc.get("updated"):
            stamps.append(doc["updated"])
    stamp = max(stamps) if stamps else "2026-01-01T00:00:00Z"
    stamp = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00")).strftime("%Y%m%dT%H%M%SZ")

    L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Janick//Ferienplaner//DE",
         "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:Ferien Janick",
         "X-WR-TIMEZONE:Europe/Zurich", "REFRESH-INTERVAL;VALUE=DURATION:PT6H",
         "X-PUBLISHED-TTL:PT6H", *VTIMEZONE]
    for d in sorted(days):
        c, ds = days[d], d.strftime("%Y%m%d")
        a, b = TIMES[c]
        L += ["BEGIN:VEVENT", f"UID:ferien-{ds}@ferienplaner-janick", f"DTSTAMP:{stamp}",
              f"DTSTART;TZID=Europe/Zurich:{ds}T{a}00", f"DTEND;TZID=Europe/Zurich:{ds}T{b}00",
              f"SUMMARY:{SUMMARY[c]}", f"DESCRIPTION:{DESC[c]}",
              "TRANSP:OPAQUE", "X-MICROSOFT-CDO-BUSYSTATUS:OOF", "END:VEVENT"]
    L.append("END:VCALENDAR")
    dst.write_bytes(("\r\n".join(L) + "\r\n").encode("utf-8"))
    print(f"{dst.name}: {len(days)} Termine")


if __name__ == "__main__":
    main()
