#!/usr/bin/env python3
"""Erzeugt ferien-janick.ics aus den exportierten Ferienplaner-Daten.

Aufruf: python3 build_ics.py <ordner-mit-JAHR.json> [ausgabe.ics]
Jede JAHR.json hat die Form {"days": {"2027-04-01": "FE" | "FG"}, "guthaben": 25, "updated": "..."}.
FE = Ferientag, FG = Ferientag geschenkt. Aufeinanderfolgende Tage werden zu einem
Termin zusammengefasst; Wochenenden und Feiertage (Winterthur ZH) unterbrechen einen Block nicht.
"""
import json, sys, datetime as dt
from pathlib import Path


def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mo = (h + l - 7 * m + 114) // 31
    da = (h + l - 7 * m + 114) % 31 + 1
    return dt.date(y, mo, da)


def holidays(y):
    E = easter(y)
    off = lambda n: E + dt.timedelta(days=n)
    return {dt.date(y, 1, 1), dt.date(y, 1, 2), off(-2), off(0), off(1), dt.date(y, 5, 1),
            off(39), off(49), off(50), dt.date(y, 8, 1), dt.date(y, 12, 25), dt.date(y, 12, 26)}


def workday(d):
    return d.weekday() < 5 and d not in holidays(d.year)


def blocks(days):
    """days: {date: code} -> Liste von (code, start, end, anzahl)."""
    out, cur = [], None
    if not days:
        return out
    d, last = min(days), max(days)
    while d <= last:
        code = days.get(d)
        if code in ("FE", "FG"):
            if cur and cur["code"] == code and cur["open"]:
                cur["end"] = d
                cur["n"] += 1
            else:
                cur = {"code": code, "start": d, "end": d, "n": 1, "open": True}
                out.append(cur)
        elif workday(d) and cur:
            cur["open"] = False
        d += dt.timedelta(days=1)
    return out


def main():
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).with_name("ferien-janick.ics")
    days, stamps = {}, []
    for f in sorted(src.glob("*.json")):
        if not f.stem.isdigit():
            continue
        doc = json.loads(f.read_text(encoding="utf-8"))
        for k, v in (doc.get("days") or {}).items():
            if v in ("FE", "FG"):
                days[dt.date.fromisoformat(k)] = v
        if doc.get("updated"):
            stamps.append(doc["updated"])
    stamp = max(stamps) if stamps else "2026-01-01T00:00:00Z"
    stamp = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00")).strftime("%Y%m%dT%H%M%SZ")

    L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Janick//Ferienplaner//DE",
         "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:Ferien Janick",
         "X-WR-TIMEZONE:Europe/Zurich", "REFRESH-INTERVAL;VALUE=DURATION:PT6H",
         "X-PUBLISHED-TTL:PT6H"]
    for b in blocks(days):
        s = b["start"].strftime("%Y%m%d")
        e = (b["end"] + dt.timedelta(days=1)).strftime("%Y%m%d")
        g = b["code"] == "FG"
        n = b["n"]
        L += ["BEGIN:VEVENT", f"UID:ferien-{b['code']}-{s}@ferienplaner-janick", f"DTSTAMP:{stamp}",
              f"DTSTART;VALUE=DATE:{s}", f"DTEND;VALUE=DATE:{e}",
              "SUMMARY:Ferien Janick" + (" (geschenkt)" if g else ""),
              f"DESCRIPTION:{n} Ferientag{'' if n == 1 else 'e'}" + (" (geschenkt)" if g else ""),
              "TRANSP:OPAQUE", "X-MICROSOFT-CDO-BUSYSTATUS:OOF", "X-MICROSOFT-CDO-ALLDAYEVENT:TRUE",
              "END:VEVENT"]
    L.append("END:VCALENDAR")
    dst.write_bytes(("\r\n".join(L) + "\r\n").encode("utf-8"))
    print(f"{dst.name}: {len(blocks(days))} Termine aus {len(days)} Tagen")


if __name__ == "__main__":
    main()
