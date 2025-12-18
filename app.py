import os
import traceback
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for

# --- FreeCAD-Module ---
import FreeCAD
import Part
import MeshPart

# --- Ordnerdefinition ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
EXPORT_FOLDER = os.path.join(BASE_DIR, "exports")

# --- Flask App Setup ---
app = Flask(__name__, template_folder=TEMPLATES_DIR)

# --- Ordner anlegen ---
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

# ----------------- Hilfsfunktionen -----------------
def clear_all_files():
    """Löscht alle Dateien in Uploads und Exports."""
    for folder in [UPLOAD_FOLDER, EXPORT_FOLDER]:
        for f in os.listdir(folder):
            try:
                os.remove(os.path.join(folder, f))
            except Exception as e:
                print(f"[WARNUNG] Konnte {f} nicht löschen: {e}")

# ----------------- Routes -----------------
@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    report = None
    step_download = None
    stl_download = None

    if request.method == "POST":
        if "stepfile" not in request.files:
            message = "Keine Datei ausgewählt"
            return render_template("index.html", message=message)

        step_file = request.files["stepfile"]
        if step_file.filename == "":
            message = "Keine Datei ausgewählt"
            return render_template("index.html", message=message)

        filepath = os.path.join(UPLOAD_FOLDER, step_file.filename)
        step_file.save(filepath)

        ext = os.path.splitext(step_file.filename)[1].lower()

        try:
            doc = FreeCAD.newDocument("Analyse")

            # --- STEP/STP ---
            if ext in [".step", ".stp"]:
                shape = Part.Shape()
                shape.read(filepath)
                if shape.isNull():
                    raise ValueError("STEP-Datei konnte nicht gelesen werden")
            # --- STL ---
            elif ext == ".stl":
                import Mesh
                mesh = Mesh.Mesh(filepath)
                shape = Part.Shape()
                shape.makeShapeFromMesh(mesh.Topology, 0.1)
            else:
                raise ValueError("Nur STEP/STP oder STL Dateien erlaubt")

            # --- Geometrieprüfung ---
            open_edges = shape.check()
            num_open_edges = len(open_edges) if open_edges else 0
            report = {
                "vertices": len(shape.Vertexes),
                "edges": len(shape.Edges),
                "faces": len(shape.Faces),
                "open_edges": num_open_edges,
                "volume": shape.Volume
            }

            # Compound + Solid
            compound = Part.Compound([shape])
            solid = Part.makeSolid(compound)

            # Refine Shape
            try:
                from Part import refineShape
                solid = refineShape(solid)
            except Exception:
                pass

            # --- Export ---
            base_name = os.path.splitext(step_file.filename)[0]
            step_filename = f"{base_name}_clean.step"
            stl_filename = f"{base_name}_clean.stl"
            step_path = os.path.join(EXPORT_FOLDER, step_filename)
            stl_path = os.path.join(EXPORT_FOLDER, stl_filename)

            solid.exportStep(step_path)
            mesh_clean = MeshPart.meshFromShape(
                Shape=solid, LinearDeflection=0.1, AngularDeflection=0.2618, Relative=False
            )
            mesh_clean.write(stl_path)

            # Gewicht
            weight_kg = solid.Volume * 7.85e-6
            report["weight_kg"] = weight_kg

            FreeCAD.closeDocument(doc.Name)

            # Redirect nach GET
            return redirect(url_for(
                "index",
                message="Bereinigung erfolgreich abgeschlossen!",
                step_file=step_filename,
                stl_file=stl_filename,
                vertices=report["vertices"],
                edges=report["edges"],
                faces=report["faces"],
                open_edges=report["open_edges"],
                volume=report["volume"],
                weight_kg=weight_kg
            ))

        except Exception as e:
            message = f"Fehler bei der Verarbeitung: {str(e)}\n{traceback.format_exc()}"

    # GET Parameter aus Redirect
    message = request.args.get("message")
    step_download = request.args.get("step_file")
    stl_download = request.args.get("stl_file")
    if request.args.get("vertices"):
        report = {
            "vertices": int(request.args.get("vertices")),
            "edges": int(request.args.get("edges")),
            "faces": int(request.args.get("faces")),
            "open_edges": int(request.args.get("open_edges")),
            "volume": float(request.args.get("volume")),
            "weight_kg": float(request.args.get("weight_kg"))
        }

    return render_template(
        "index.html",
        message=message,
        report=report,
        step_download=step_download,
        stl_download=stl_download
    )

@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(EXPORT_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "Datei nicht gefunden", 404

@app.route("/clear", methods=["POST"])
def clear():
    clear_all_files()
    # Status auf Null zurücksetzen
    report = {
        "vertices": 0,
        "edges": 0,
        "faces": 0,
        "open_edges": 0,
        "volume": 0.0,
        "weight_kg": 0.0
    }
    return jsonify({
        "status": "ok",
        "message": "Uploads, Exports und Statusanzeigen vollständig gelöscht!",
        "report": report
    })

# ----------------- Server starten -----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055, debug=False)
