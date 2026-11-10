# Live-Demo: GitHub Actions für eine Python-/ML-nahe Pipeline

## Ziel und Dauer

- Ziel: Den Weg von einer Codeänderung bis zum veröffentlichten Container-Image zeigen.
- Empfohlene Dauer: 25–30 Minuten.
- Story: **grün → absichtlich rot → Diagnose → Fix → grün → Merge → Publish**.

## Vor der Lehrveranstaltung vorbereiten

1. Python 3.11, Git und Docker lokal prüfen.
2. Repository auf GitHub anlegen.
3. Projektdateien einmal lokal vollständig ausführen.
4. Initialen `main`-Lauf erfolgreich abschließen lassen.
5. Unter **Packages** prüfen, ob das GHCR-Image sichtbar ist.
6. Browser-Tabs vorbereiten: Repository, Actions, Pull Requests, Packages.
7. Optional: Einen zweiten Browser oder Inkognito-Modus für die Studierendenansicht öffnen.

## Schritt 1 — Lokalen Ausgangszustand prüfen (ca. 4 Min.)

```bash
python -m pip install --requirement requirements.txt
python -m ruff check src tests
python -m ruff format --check src tests
python -m pytest -v
docker build --tag ml-ci-demo:test .
docker run --rm ml-ci-demo:test
```

Erwartung: Alle Prüfungen sind grün, pytest meldet fünf erfolgreiche Testfälle.

Sprechtext: „Lokal prüfen wir dieselben Qualitätsstufen wie später auf GitHub. CI macht diese Checks reproduzierbar und unabhängig von meinem Laptop.“

## Schritt 2 — Workflow und Trigger erklären (ca. 3 Min.)

In `.github/workflows/ml-pipeline.yml` zeigen:

- `push` auf `main` und `dev`
- `pull_request` nach `main`
- manueller Start mit `workflow_dispatch`
- Pip-Cache in `actions/setup-python`
- Lint, Formatcheck, Unit Tests, Hadolint
- Docker-Build und Test im Container
- GHCR-Login und Push ausschließlich auf `main`

Kernaussage: Pull Requests prüfen; nur ein erfolgreicher Push auf `main` veröffentlicht.

## Schritt 3 — Feature-Branch erstellen (ca. 2 Min.)

```bash
git switch -c demo/break-tokenizer
```

In `src/preprocess.py` ändern:

```python
def tokenize_text(text: str) -> list[str]:
    """Split text into whitespace-separated tokens."""
    return text.split()
```

Dann:

```bash
git add src/preprocess.py
git commit -m "Break token normalization intentionally"
git push -u origin demo/break-tokenizer
```

## Schritt 4 — Pull Request öffnen und roten Lauf zeigen (ca. 5 Min.)

1. Auf GitHub **Compare & pull request** wählen.
2. Basisbranch `main` kontrollieren.
3. Pull Request erstellen.
4. **Checks** oder **Actions** öffnen.
5. Job `Lint, test, build and publish` öffnen.
6. Den Fehler bei **Run unit tests** zeigen.

Erwartete Abweichung:

```text
actual:   ["Hello", "World"]
expected: ["hello", "world"]
```

Wichtig: Nach dem fehlerhaften Schritt werden die nachfolgenden Standardschritte übersprungen. Es findet kein Docker-Build und kein Image-Push statt.

Sprechtext: „Der Pull Request verhindert, dass die Regression unbemerkt nach `main` gelangt.“

## Schritt 5 — Fehler reparieren (ca. 3 Min.)

`src/preprocess.py` wieder korrigieren:

```python
def tokenize_text(text: str) -> list[str]:
    """Convert text to lowercase whitespace-separated tokens."""
    return text.lower().split()
```

Dann:

```bash
git add src/preprocess.py
git commit -m "Fix token normalization"
git push
```

Der bestehende Pull Request aktualisiert sich automatisch. Den neuen Lauf öffnen und zeigen, dass alle Schritte erfolgreich sind.

Caching korrekt erklären: Der GitHub Runner ist pro Lauf frisch. Der wiederhergestellte Pip-Cache kann Paketdownloads vermeiden; die Installation wird trotzdem ausgeführt.

## Schritt 6 — Mergen und Image veröffentlichen (ca. 4 Min.)

1. Grünen Pull Request mergen.
2. Den durch den Merge ausgelösten `main`-Lauf öffnen.
3. Zeigen, dass jetzt zusätzlich Login, Tagging und Push ausgeführt werden.
4. Unter **Packages** das Image öffnen.
5. Tags erklären:
   - `latest`: bequemer Verweis auf den neuesten erfolgreichen `main`-Stand
   - Commit-SHA: unverwechselbare Zuordnung von Image zu Quellcode

Beispiel:

```bash
docker pull ghcr.io/DEIN-USERNAME/ml-ci-demo:latest
```

Bei privatem Package zuerst authentifizieren oder die Sichtbarkeit anpassen.

## Schritt 7 — Optionalen Ruff-Fehler zeigen (ca. 3 Min.)

Am Anfang von `src/preprocess.py` absichtlich ergänzen:

```python
import os
```

Dann lokal:

```bash
python -m ruff check src tests
```

Erwartung: `F401` für einen unbenutzten Import.

Automatische Korrektur demonstrieren:

```bash
python -m ruff check --fix src tests
```

## Abschlussbotschaft

**Pull Requests prüfen Änderungen. Nur geprüfter Code auf `main` wird als Container-Image veröffentlicht.**

## Notfallplan für die Live-Demo

- GitHub Actions startet nicht: Reiter **Actions** öffnen und den Workflow über **Run workflow** manuell starten.
- Docker lokal nicht verfügbar: Lokale Container-Schritte überspringen; der GitHub-Runner übernimmt sie.
- GHCR-Push scheitert: Unter **Settings → Actions → General → Workflow permissions** und im Workflow `packages: write` prüfen.
- Package nicht sichtbar: Repository-Seite neu laden und **Packages** prüfen; Sichtbarkeit des Packages kontrollieren.
- Zu wenig Zeit: Direkt mit vorbereitetem fehlerhaften Pull Request beginnen und nur Diagnose, Fix, Merge und Publish zeigen.
