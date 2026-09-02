import os
import torch
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim

DATASET_DIR = "onion_quality_dataset"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "onion_model.pth")

os.makedirs(MODEL_DIR, exist_ok=True)

BATCH_SIZE = 2
EPOCHS = 10
LEARNING_RATE = 0.001

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

dataset = datasets.ImageFolder(
    DATASET_DIR,
    transform=transform
)

print("Classes:", dataset.classes)
print("Number of images:", len(dataset))

train_loader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)

model = models.mobilenet_v2(weights="DEFAULT")

for parameter in model.parameters():
    parameter.requires_grad = False

model.classifier[1] = nn.Linear(
    model.last_channel,
    len(dataset.classes)
)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Using device:", device)

model = model.to(device)

criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    model.classifier[1].parameters(),
    lr=LEARNING_RATE
)

print("\nStarting training...\n")

for epoch in range(EPOCHS):

    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        _, predicted = torch.max(outputs, 1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total

    print(
        f"Epoch [{epoch + 1}/{EPOCHS}] "
        f"Loss: {running_loss:.4f} "
        f"Accuracy: {accuracy:.2f}%"
    )

torch.save(
    {
        "model_state_dict": model.state_dict(),
        "classes": dataset.classes
    },
    MODEL_PATH
)

print("\nTraining complete!")
print("Model saved to:", MODEL_PATH)