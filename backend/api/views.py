import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import torch
from PIL import Image
from torchvision import transforms
from transformers import CLIPModel, CLIPProcessor
from .models import ClothItem
from .serializers import ClothItemSerializer

@api_view(["GET"])
def hello(request):
    return Response("Hello")

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

@api_view(["GET"])
def image_to_vector(request):
    """
    Convert a PNG/JPG into a vector embedding using CLIP.
    """
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "download.jpg")
    image = Image.open(image_path)

    inputs = processor(images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        embedding = model.get_image_features(**inputs)

    # Normalize and convert to list
    vector = embedding[0] / embedding[0].norm(p=2)
    return Response(vector.tolist())

@api_view(["GET"])
def get_initial_cloth_items(request):
    items = ClothItem.objects.all()[:10]
    serializer = ClothItemSerializer(items, many=True)
    return Response(serializer.data)

