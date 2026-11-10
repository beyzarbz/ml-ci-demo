# ML CI/CD Demo mit GitHub Actions

Kompakte Lehrdemo für einen vollständigen Qualitäts- und Veröffentlichungsfluss:

**Code → Ruff → pytest → Hadolint → Docker-Build → Container-Test → GHCR-Push**

Das Beispiel ist bewusst klein: Eine Textvorverarbeitungsfunktion wird lokal, in GitHub Actions und im gebauten Container geprüft. Der Fokus liegt auf CI/CD, nicht auf Modelltraining.

## Projektstruktur

```text
ml-ci-demo/
├── .github/
│   └── workflows/
│       └── ml-pipeline.yml
├── src/
│   ├── __init__.py
│   └── preprocess.py
├── tests/
│   ├── __init__.py
│   └── test_preprocess.py
├── .dockerignore
├── .gitignore
├── DEMO_SCRIPT.md
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Voraussetzungen

- Git
- Python 3.11
- Docker Desktop oder Docker Engine
- GitHub-Konto mit Berechtigung, ein Repository und Packages anzulegen

## Lokal ausführen

### 1. Virtuelle Umgebung anlegen

Linux/macOS:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Abhängigkeiten installieren

```bash
python -m pip install --upgrade pip
python -m pip install --requirement requirements.txt
```

### 3. Qualitätsprüfungen ausführen

```bash
python -m ruff check src tests
python -m ruff format --check src tests
python -m pytest -v
```

### 4. Container bauen und testen

```bash
docker build --tag ml-ci-demo:test .
docker run --rm ml-ci-demo:test
```

## Workflow-Verhalten

| Ereignis | Prüfungen | Image-Push nach GHCR |
|---|---|---|
| Pull Request nach `main` | ja | nein |
| Push nach `dev` | ja | nein |
| Push nach `main` | ja | ja |
| Manuell (`workflow_dispatch`) | ja | nein |

Für den Image-Push verwendet der Workflow das automatisch bereitgestellte `GITHUB_TOKEN` und die Job-Berechtigung `packages: write`. Das Image wird mit `latest` und dem vollständigen Commit-SHA getaggt.

## Repository erstmalig veröffentlichen

1. Auf GitHub ein leeres Repository `ml-ci-demo` anlegen.
2. Lokal ausführen:

```bash
git init
git add .
git commit -m "Add ML CI/CD demo"
git branch -M main
git remote add origin https://github.com/DEIN-USERNAME/ml-ci-demo.git
git push -u origin main
```

3. Im Repository den Reiter **Actions** öffnen.
4. Nach erfolgreichem Lauf unter **Packages** das veröffentlichte Image prüfen.

Hinweis: Ein neu veröffentlichtes GHCR-Package kann privat sein. Zum lokalen Pull ist dann eine Authentifizierung erforderlich oder die Package-Sichtbarkeit muss angepasst werden.

## Didaktische Fehlerdemo

Die vollständige Schrittfolge steht in [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md). Kernidee:

1. Feature-Branch erstellen.
2. `text.lower().split()` absichtlich durch `text.split()` ersetzen.
3. Pull Request öffnen und den fehlgeschlagenen pytest-Schritt zeigen.
4. Implementierung reparieren und denselben Pull Request aktualisieren.
5. Nach grüner Pipeline mergen.
6. Den neuen `main`-Lauf und den GHCR-Push zeigen.

## Technische Einordnung

- **Ruff** findet statisch erkennbare Python-Probleme und prüft die Formatierung.
- **pytest** prüft erwartetes Verhalten.
- **Hadolint** findet Dockerfile-Antipatterns und Best-Practice-Verstöße; es ist kein CVE-Scanner.
- **Docker Build** prüft, ob das Image gebaut werden kann.
- **Docker Run** prüft, ob die Tests im Image tatsächlich starten und erfolgreich sind.
- **GHCR-Push** veröffentlicht nur bei einem Push auf `main` das geprüfte Artefakt.

Für eine Produktionsumgebung wären zusätzlich sinnvoll: Action-Versionen auf Commit-SHAs pinnen, Abhängigkeiten automatisiert aktualisieren, SBOM/Provenance erzeugen und das Image mit einem Scanner wie Trivy, Grype oder Docker Scout prüfen.
