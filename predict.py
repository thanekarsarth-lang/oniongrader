import torch
from torchvision import transforms, models
from PIL import Image
import torch.nn as nn

MODEL_PATH = "models/onion_model.pth"

checkpoint = torch.load(
    MODEL_PATH,
    map_location=torch.device("cpu")
)

classes = checkpoint["classes"]

model = models.mobilenet_v2(weights=None)

model.classifier[1] = nn.Linear(
    model.last_channel,
    len(classes)
)

model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

def predict(image):
    image = image.convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)
        probabilities = torch.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    label = classes[predicted.item()]
    confidence = confidence.item() * 100

    return label, confidence