from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Cargar modelo
model = load_model("model/sentibotv2.h5")

# Labels de emociones (ajusta según tu modelo)
EMOTIONS = ['Feliz', 'Triste', 'Enojado', 'Sorprendido', 'Neutral']

def prepare_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("L")  # escala de grises
    img = img.resize((48,48))  # tamaño que espera tu modelo
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # normalización
    return img_array

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    img_array = prepare_image(image_bytes)
    prediction = model.predict(img_array)
    emotion_idx = np.argmax(prediction)
    confidence = float(np.max(prediction))
    return JSONResponse({
        "emotion": EMOTIONS[emotion_idx],
        "confidence": confidence
    })
