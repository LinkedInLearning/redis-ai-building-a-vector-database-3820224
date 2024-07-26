import torchvision.transforms as transforms
import torch
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image

import redis
import  numpy  as  np

# Load the pre-trained ResNet model
model = resnet50(weights=ResNet50_Weights.DEFAULT)
model.eval()  # Set the model to evaluation mode

preprocess_pipeline = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


r = redis.Redis(
  host='redis-18659.c73.us-east-1-2.ec2.redns.redis-cloud.com',
  port=18659,
  password='VDgT8dXUTK1af9DLMxkUHxy9yjk2zs0v')

index_name = "index_images_RN_1"
EMBEDDINGS_FIELD = "vectors"
KEY_PREFIX = "images_"




# Function to generate embeddings for an image
def generate_image_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    image = preprocess_pipeline(image).unsqueeze(0)

    with torch.no_grad():
      embedding = model(image).numpy().flatten()
    return embedding

