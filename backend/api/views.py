import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import torch
from PIL import Image
from torchvision import transforms
from transformers import CLIPModel, CLIPProcessor
from .models import ClothItem, UserProfile
from .serializers import ClothItemSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status

from pinecone import Pinecone
import os
from langchain_pinecone import PineconeVectorStore

os.environ["PINECONE_API_KEY"] = "pcsk_6JLk9t_PANwkAZxWTq36FKFwYUmphy5F1XRYcTUTskjj5nbqPwoSUnH9n35Rk4gofE8C7Y"

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

index_name = "dechacks-clozyt-db"

index = pc.Index(index_name)

@api_view(["POST"])
def create_user(request):
    """
    Create a new user profile.
    """
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        hashed_password = make_password(password)
        user_vector = [0] * 2049
        UserProfile.objects.create(
            email=email, password=hashed_password, user_vector=user_vector
        )
        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

@api_view(["POST"])
def swipe(request):
    direction = request.data.get("direction")
    item_id = request.data.get("item_id")
    user_id = request.data.get("user_id")

    user = UserProfile.objects.filter(id=user_id).first()
    if not user:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    item = ClothItem.objects.filter(id=item_id).first()
    if not item:
        return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND) 
    
    if direction not in ["left", "right"]:
        return Response({"error": "Invalid direction."}, status=status.HTTP_400_BAD_REQUEST)
    

    alpha = 0.15

    fetch_response = index.fetch(ids=[f"item_{item_id}"])
    item_vector = fetch_response.vectors[f"item_{item_id}"]

    if direction == "right":
        item.likes += 1
        return (1 - alpha) * user.user_vector + alpha * direction * item_vector