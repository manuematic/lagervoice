#!/usr/bin/env python3
"""Read-only Homebox inventory search with human-friendly German output."""
import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_URL = "http://1.1.1.1:3100"


def api_get(base_url, api_key, path, params=None):
    url = base_url.rstrip("/") + path
    if params:
        url += "?" + urlencode(params)
    request = Request(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    })
    try:
        with urlopen(request, timeout=10) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"Homebox meldet HTTP {exc.code} ({exc.reason}).") from exc
    except URLError as exc:
        raise RuntimeError(f"Homebox nicht erreichbar: {exc.reason}") from exc
    except (ValueError, UnicodeError) as exc:
        raise RuntimeError("Homebox hat keine gültige JSON-Antwort geliefert.") from exc


def location_path(base_url, api_key, item, cache):
    names = []
    seen = set()
    parent = item.get("parent")
    for _ in range(12):
        if not isinstance(parent, dict):
            break
        name = parent.get("name")
        if name:
            names.append(str(name))
        parent_id = parent.get("id")
        if not parent_id or parent_id in seen:
            break
        seen.add(parent_id)
        if parent_id not in cache:
            cache[parent_id] = api_get(base_url, api_key, f"/api/v1/entities/{parent_id}")
        parent = cache[parent_id].get("parent")
    return list(reversed(names))


def natural_list(values):
    if len(values) <= 1:
        return "".join(values)
    if len(values) == 2:
        return " und ".join(values)
    return ", ".join(values[:-1]) + " und " + values[-1]


def spoken_location(parts):
    if not parts:
        return "an einem unbekannten Lagerort"
    return "in " + ", ".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Homebox-Inventar durchsuchen")
    parser.add_argument("query", help="Suchbegriff, z. B. 'Netzteil CCU3'")
    parser.add_argument("--url", default=os.getenv("HOMEBOX_URL", DEFAULT_URL), help="Homebox-Basis-URL")
    args = parser.parse_args()
    api_key = os.getenv("HOMEBOX_API_KEY")
    if not api_key:
        print("Fehler: Umgebungsvariable HOMEBOX_API_KEY fehlt.", file=sys.stderr)
        return 2
    try:
        result = api_get(args.url, api_key, "/api/v1/entities", {"q": args.query})
        items = result.get("items", [])
        if not items:
            print(f"Ich habe für {args.query} keinen Gegenstand gefunden.")
            return 0
        cache = {}
        matches = []
        for item in items[:5]:
            parts = location_path(args.url, api_key, item, cache)
            matches.append(f"{item.get('name', 'Unbenannter Gegenstand')} {spoken_location(parts)}")
        if len(items) == 1:
            print(f"{matches[0]}.")
        else:
            count = result.get("total", len(items))
            print(f"Ich habe {count} Treffer gefunden: {natural_list(matches)}.")
            if len(items) > 5:
                print("Ich habe nur die ersten fünf Treffer vorgelesen.")
        return 0
    except (RuntimeError, TypeError, AttributeError) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
