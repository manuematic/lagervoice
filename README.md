Konfigruationsdateien und Skript für Abfrage von homebox (https://homebox.software/en) um Gegenstände im eigenen Lager zu finden.

Die yaml Dateien sind Beispiele und sollten in eure vorhandenen Konfigurationsdateien eingefügt werden.

Zuerst muss ein API-Key in Homebox erstellt werden (Links Profil anklicken und dann unter API-KEYS genereiren). 
Diesen dann in eure secrets.yaml kopieren an die Stelle die markiert ist (secrets.yaml.example zeigt das Format, secrets.yaml selbst wird nicht ins Repo übernommen).

homebox_search.py - Skript welches den API Aufruf zum suchen in Homebox realisiert, in Zeile 12 muss die DEFAULT_URL angepasst werden je nachdem unetr welcher IP, Name und Port bei euch Homebox läuft.

configuration.yaml - Kommt so in die configurations.yaml

secrets.yaml - Wie oben schon gesagt kommt dort der Homebox API_KEY rein.

intents.yaml - Das ist die Antwort die Home Assistant ausgibt, die kommt entweder in eine vorhandene Konfigrationsdatei mit intents oder in configuration.yaml unter intents:

custom_sentences/de/homebox_suche.yaml - Das ist die Datei mit den Templates für Suchanfragen, Sätze können nach Bedarf angepasst werden. Wichtig ist das lists unten da ansonsten nicht mehrere Suchwörter erkannt werden.
