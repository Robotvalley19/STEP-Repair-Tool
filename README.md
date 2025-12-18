# STEP-Repair-Tool

Ein Open-Source Tool zur Bereinigung und Reparatur von STEP (.step/.stp) und STL (.stl) Dateien, damit sie für FEM- und andere Simulationsprogramme zuverlässig nutzbar sind.

## Beweggrund

Bei der Arbeit mit 3D-Modellen für FEM- und Simulationssoftware kommt es häufig vor, dass STEP- oder STL-Dateien Fehler enthalten (z.B. offene Kanten oder nicht-solide Geometrien), die eine Simulation unmöglich machen.  
Dieses Projekt wurde gestartet, um:

- fehlerhafte STEP/STL-Dateien automatisch zu reparieren  
- den Export in saubere STEP/STL-Dateien zu ermöglichen  
- den Workflow für Simulationen zu vereinfachen  
- den Aufwand manueller Reparaturen deutlich zu reduzieren  

Das Ziel ist ein **schnelles, sicheres und einfaches Web-Tool**, das in einer lokal laufenden Umgebung ohne externe Abhängigkeiten funktioniert.

## Funktionen

- Upload von STEP und STL Dateien  
- Automatische Reparatur von fehlerhaften Geometrien  
- Export in STEP und STL  
- Alles-löschen Button für Uploads/Exports  

## Installation

1. Systemabhängige FreeCAD-Python-Bindings installieren:

   ```bash
   sudo apt install freecad python3-freecad
