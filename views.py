from django.http import JsonResponse
from .ml_model import predict_emotion
from PIL import Image
import json, base64
from io import BytesIO

def predict_emotion_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        image_base64 = data.get("image")
        if not image_base64:
            return JsonResponse({"label": "Null", "confidence": 0})
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]
        try:
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_bytes)).convert("L")
        except Exception as e:
            return JsonResponse({"label": "Null", "confidence": 0, "error": str(e)})
        label, confidence = predict_emotion(image)
        return JsonResponse({"label": label, "confidence": confidence})
