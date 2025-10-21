import os
import base64
from io import BytesIO
from flask import Flask, render_template, request, jsonify
from PIL import Image
from ml_model import predict_emotion

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/predict_emotion', methods=['POST'])
def predict():
    data = request.get_json()
    image_base64 = data.get("image")

    if not image_base64:
        return jsonify({"label": "Null", "confidence": 0})

    # Si la imagen tiene encabezado tipo "data:image/png;base64,"
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]

    try:
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_bytes)).convert("L")
    except Exception as e:
        return jsonify({"label": "Null", "confidence": 0, "error": str(e)})

    label, confidence = predict_emotion(image)
    return jsonify({"label": label, "confidence": confidence})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Puerto dinámico para Railway
    app.run(host='0.0.0.0', port=port)
