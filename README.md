# STEP-Repair-Tool

Ein Open-Source Web-Tool zur automatisierten Bereinigung, Reparatur und Konvertierung von fehlerhaften STEP (.step/.stp) und STL (.stl) Dateien für den zuverlässigen Einsatz in FEM-, CFD- und anderen Simulationsprogrammen.

---

## Projektüberblick

In industriellen Entwicklungsprozessen werden 3D-CAD-Modelle häufig zwischen verschiedenen CAD-, CAM- und Simulationssystemen ausgetauscht. Dabei treten regelmäßig Geometrieprobleme auf, beispielsweise:

* offene Kanten (Open Edges)
* nicht geschlossene Volumenkörper
* inkonsistente Mesh-Strukturen
* fehlerhafte oder degenerierte Flächen
* fehlende Solid-Definitionen
* importierte STL-Dateien ohne Volumenstruktur

Solche Fehler verhindern oder verfälschen FEM- und CFD-Simulationen.

Dieses Tool automatisiert die Analyse, Reparatur und Solid-Erstellung von STEP- und STL-Dateien und stellt saubere Exportdateien für nachgelagerte Simulationsprozesse bereit.

---

## Motivation

Während der Arbeit mit FEM- und Simulationssoftware wurde deutlich, dass:

* viele importierte STEP-Dateien keine geschlossenen Solids sind
* STL-Dateien lediglich Mesh-Geometrien enthalten
* manuelle Reparatur in CAD-Systemen zeitaufwendig ist
* nicht jedes Teammitglied über CAD-Reparatur-Know-how verfügt

Ziel dieses Projekts ist es, einen einfachen, reproduzierbaren und lokal ausführbaren Reparatur-Workflow bereitzustellen, der:

* automatisiert Geometrie prüft
* Solids erzwingt
* Mesh in Solid-Geometrie konvertiert
* bereinigte Dateien exportiert
* ohne externe Cloud-Dienste funktioniert

---

## Technologiestack

**Backend:**

* Python 3.x
* Flask
* FreeCAD Python API (Part, MeshPart)

**Frontend:**

* HTML5
* CSS3
* Vanilla JavaScript

**Architektur:**

* Lokale Web-Anwendung
* Serverseitige Geometrieverarbeitung
* Automatisierte Datei- und Statusverwaltung

---

## Kernfunktionen

### 1. Datei-Upload

Unterstützte Dateiformate:

* `.step`
* `.stp`
* `.stl`

### 2. Geometrieanalyse

Nach dem Upload werden folgende Parameter ermittelt:

* Anzahl Vertices
* Anzahl Edges
* Anzahl Faces
* Anzahl offener Kanten
* Volumen
* Berechnetes Gewicht (Stahl-Dichte: 7.85 g/cm³)

### 3. Automatische Reparatur

Je nach Dateityp:

#### STEP:

* Einlesen der Shape-Struktur
* Prüfung auf Null-Shape
* Solid-Erstellung über Compound
* Solid-Erzwingung mit `Part.makeSolid`
* Optionales Refine zur Topologie-Bereinigung

#### STL:

* Mesh-Import
* Konvertierung Mesh → Shape
* Solid-Erstellung
* Geometrische Nachbearbeitung

### 4. Export

Automatischer Export in:

* Bereinigte STEP-Datei
* Bereinigte STL-Datei

Dateinamen:

```
originalname_clean.step
originalname_clean.stl
```

### 5. Status-Reset

* Löscht alle Upload- und Exportdateien
* Setzt Geometrieanzeige zurück
* Ermöglicht sauberen Neustart

---

## Technische Architektur

### Verzeichnisstruktur

```
project/
│
├── app.py
├── templates/
│   └── index.html
├── uploads/
├── exports/
└── README.md
```

### Workflow

1. Datei-Upload
2. FreeCAD-Dokument wird erzeugt
3. Geometrie wird eingelesen
4. Shape-Validierung
5. Solid-Erstellung
6. Refinement
7. Export
8. FreeCAD-Dokument wird geschlossen
9. Status + Download-Links werden angezeigt

---

## Installation

### Voraussetzungen

* Linux (empfohlen)
* Python 3.x
* FreeCAD mit Python-Bindings

### FreeCAD installieren

Ubuntu / Debian:

```bash
sudo apt install freecad python3-freecad
```

### Python-Abhängigkeiten

```bash
pip install flask
```

### Projekt starten

```bash
python app.py
```

Die Anwendung läuft anschließend unter:

```
http://localhost:5055
```

---

## Anwendungsfälle

* FEM-Vorbereitung (z.B. ANSYS, Abaqus, CalculiX, COMSOL)
* CFD-Preprocessing
* Rapid Prototyping
* STL → Solid Konvertierung
* Automatisierte Geometrieprüfung in kleinen Entwicklungsabteilungen
* Lehr- und Hochschulprojekte

---

## Besonderheiten des Projekts

* Rein lokal ausführbar (keine Cloud)
* Keine proprietäre CAD-Lizenz notwendig
* Automatisierter Reparatur-Workflow
* Klar strukturierte Backend-Architektur
* Saubere Trennung von Frontend und Geometrie-Logik
* Fehlerbehandlung mit Traceback-Reporting
* Erweiterbar für Batch-Verarbeitung

---

## Mögliche Erweiterungen

* Batch-Verarbeitung mehrerer Dateien
* Geometrie-Healing mit erweiterten FreeCAD-Funktionen
* Unterstützung für IGES-Dateien
* Docker-Containerisierung
* REST-API für Integration in CI/CD-Pipelines
* Automatische Materialwahl
* Einheiten-Erkennung
* Geometrie-Qualitätsbewertung (z.B. Self-Intersections)

---

## Sicherheit & Designentscheidungen

* Dateien werden lokal gespeichert
* Keine persistente Datenbank
* Keine externen Uploads
* FreeCAD-Dokumente werden nach Verarbeitung geschlossen
* Fehler werden abgefangen und angezeigt

---

## Warum dieses Projekt für Industrie & Simulation relevant ist

Simulationen scheitern häufig nicht an der Physik – sondern an der Geometrie.

Ein automatisiertes Reparaturtool:

* spart Entwicklungszeit
* reduziert Iterationszyklen
* erhöht Prozesssicherheit
* ermöglicht reproduzierbare Workflows

Dieses Projekt zeigt:

* Verständnis für CAD-Datenstrukturen
* Erfahrung mit Geometrieverarbeitung
* Kenntnisse in Python-Backend-Entwicklung
* Schnittstellenarbeit zwischen Mechanik und Software
* Praxisorientiertes Problemlösen

---

## Kontext

Dieses Projekt demonstriert:

* Eigenständige Entwicklung einer technischen Webanwendung
* Integration von CAD-Geometrie-APIs in Python
* Verständnis von FEM-Vorverarbeitung
* Systematisches Error-Handling
* Saubere Projektstruktur
* Technisches Denken an der Schnittstelle von Mechanik & Software

Es verbindet klassische Maschinenbau-Themen mit moderner Softwareentwicklung.

---

## Lizenz

MIT License 

---

## Kontakt

GitHub: Robotvalley19
Projekt: STEP-Repair-Tool
