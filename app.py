from flask import Flask, render_template, request, jsonify
import base64
from io import BytesIO
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
    app.run(debug=True)
