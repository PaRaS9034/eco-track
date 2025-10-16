from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from classifier_stub import classify_image
from PIL import Image

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def health():
    return jsonify({"status": "EcoTrack backend running"})

@app.route("/classify", methods=["POST"])
def classify():
    if "image" not in request.files:
        return jsonify({"error": "No image part"}), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Validate image
        try:
            img = Image.open(file_path)
            img.verify()
        except Exception as e:
            return jsonify({"error": "Invalid image file", "details": str(e)}), 400

        # Call classifier stub
        result = classify_image(file_path)

        bin_suggestion = {
            "plastic": "Plastic Bin",
            "organic": "Organic/Bio Bin",
            "metal": "Metal Bin",
            "glass": "Glass Bin",
            "paper": "Paper Bin",
            "unknown": "General Waste"
        }.get(result["label"], "General Waste")

        response = {
            "label": result["label"],
            "confidence": result["confidence"],
            "suggested_bin": bin_suggestion
        }
        return jsonify(response)
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
