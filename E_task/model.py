import torch
import torch.nn as nn
from torchvision.models import resnet18, resnet50, resnet34
from torchvision.models.resnet import ResNet18_Weights, ResNet34_Weights, ResNet50_Weights


class OxfordPetsModel(nn.Module):
    def __init__(self, num_classes: int, num_layers_to_unfreeze: int):
        super().__init__()

        self.num_classes = num_classes
        self.model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
        # self.model = resnet34(weights=ResNet34_Weights.IMAGENET1K_V1)
        # self.model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
        for param in self.model.parameters():
            param.requires_grad = False

        # Get the total number of layers
        total_layers = len(list(self.model.parameters()))
        
        # Unfreeze the last num_layers_to_unfreeze layers
        for i, param in enumerate(self.model.parameters()):
            if total_layers - i <= num_layers_to_unfreeze:
                param.requires_grad = True
        
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)


    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)