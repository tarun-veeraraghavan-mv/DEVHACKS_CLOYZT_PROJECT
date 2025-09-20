import torch
from transformers import CLIPModel, CLIPProcessor
from PIL import Image
import requests
from io import BytesIO

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def text_to_vector(text: str):
    """
    Convert a string into a vector embedding using CLIP.
    """
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    with torch.no_grad():
        embedding = model.get_text_features(**inputs)

    # Normalize and convert to list
    vector = embedding[0] / embedding[0].norm(p=2)
    return vector.tolist()

def image_to_vector(image_url: str):
    """
    Convert an online image from a URL into a vector embedding using CLIP.
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        image = Image.open(BytesIO(response.content))
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from URL {image_url}: {e}")
        return None # Or handle the error as appropriate
    except Exception as e:
        print(f"Error opening image from URL {image_url}: {e}")
        return None

    # Use the globally defined processor and model
    inputs = processor(images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        embedding = model.get_image_features(**inputs)

    # Normalize and convert to list
    vector = embedding[0] / embedding[0].norm(p=2)
    return vector.tolist()