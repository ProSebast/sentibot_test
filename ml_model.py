import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image

# Cargar el modelo una sola vez
model = load_model("model/sentibotv2.h5")
EMOTION_LABELS = ["Feliz", "Triste", "Neutral", "Enojado", "Sorprendido"]

def predict_emotion(image: Image.Image):
    try:
        image = image.resize((48,48))
        img_array = img_to_array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Asegurar escala de grises
        if img_array.shape[-1] != 1:
            img_array = img_array.mean(axis=-1, keepdims=True)

        preds = model.predict(img_array)
        label_idx = np.argmax(preds)
        confidence = float(np.max(preds) * 100)
        return EMOTION_LABELS[label_idx], confidence

    except Exception as e:
        print("Error en predicción:", e)
        return "Null", 0.0
