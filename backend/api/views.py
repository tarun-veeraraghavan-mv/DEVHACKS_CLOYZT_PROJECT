import os
import random
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import torch
from PIL import Image
from torchvision import transforms
from transformers import CLIPModel, CLIPProcessor
from .models import ClothItem, UserProfile, Waitlist
from .serializers import ClothItemSerializer, WaitlistSerializer, UserProfileSerializer
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
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserProfileSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    item_id = int(request.data.get("item_id"))
    user_id = request.data.get("user_id")

    user = UserProfile.objects.filter(id=user_id).first()
    if not user:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    item = ClothItem.objects.filter(id=item_id).first()
    if not item:
        return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND) 
    
    if user.swiped_items is None:
        user.swiped_items = []
    user.swiped_items.append(item_id)

    if direction not in ["left", "right"]:
        return Response({"error": "Invalid direction."}, status=status.HTTP_400_BAD_REQUEST)
    

    alpha = 0.15
    lmbda = 0.01 # regularization parameter

    fetch_response = index.fetch(ids=[f"{item_id}"])
    item_vector_data = fetch_response.vectors[f"{item_id}"].values

    user_vector_tensor = torch.tensor(user.user_vector, dtype=torch.float32)
    item_vector_tensor = torch.tensor(item_vector_data, dtype=torch.float32)

    if direction == "right":
        item.like_count += 1
        dir_val = 1
    else:
        item.dislike_count += 1
        dir_val = -1
    item.save()
    
    # Calculate predicted rating (dot product)
    predicted_rating = torch.dot(user_vector_tensor, item_vector_tensor)
    
    # Calculate error
    error = dir_val - predicted_rating
    
    # SGD update rule
    new_user_vector_tensor = user_vector_tensor + alpha * (error * item_vector_tensor - lmbda * user_vector_tensor)
    
    user.user_vector = new_user_vector_tensor.tolist()
    user.save()

    # --- Exploration vs. Exploitation ---
    # 20% chance to explore by showing a random item
    if random.random() < 0.2:
        # EXPLORATION LOGIC
        all_item_ids = set(ClothItem.objects.values_list('id', flat=True))
        swiped_item_ids = set(user.swiped_items if user.swiped_items else [])
        unseen_item_ids = list(all_item_ids - swiped_item_ids)

        if unseen_item_ids:
            random_item_id = random.choice(unseen_item_ids)
            random_item = ClothItem.objects.get(id=random_item_id)
            serializer = ClothItemSerializer(random_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # If no unseen random items, fall through to exploitation.

    # EXPLOITATION LOGIC (the original approach, but more robust)
    related_items = index.query(
        vector=user.user_vector,
        top_k=200,  # Keep existing larger top_k for a bigger candidate pool
        include_metadata=True,
    )
    print(related_items)

    swiped_items_str = [str(i) for i in user.swiped_items]
    for match in related_items.get("matches", []):
        if match.get("id") not in swiped_items_str:
            # Found an item that has not been swiped
            try:
                item_id = int(match.get("id"))
                fresh_item = ClothItem.objects.get(id=item_id)
                serializer = ClothItemSerializer(fresh_item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except (ClothItem.DoesNotExist, ValueError):
                # This can happen if Pinecone index is out of sync with DB,
                # or if the ID is not a valid integer.
                # In this case, we just continue to the next match.
                continue

    # Final fallback if exploitation also fails
    return Response({"message": "No new items to recommend."}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def add_to_waitlist(request):
    """
    Add a user to the waitlist for a cloth item.
    """
    serializer = WaitlistSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def remove_from_waitlist(request, waitlist_id):
    """
    Remove a user from the waitlist for a cloth item.
    """
    try:
        waitlist_entry = Waitlist.objects.get(id=waitlist_id)
        waitlist_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Waitlist.DoesNotExist:
        return Response({"error": "Waitlist entry not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def get_waitlist_items(request, user_id):
    """
    Get all waitlist items for a user.
    """
    try:
        user = UserProfile.objects.get(id=user_id)
        waitlist_items = Waitlist.objects.filter(user=user)
        cloth_items = [item.cloth_item for item in waitlist_items]
        serializer = ClothItemSerializer(cloth_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
