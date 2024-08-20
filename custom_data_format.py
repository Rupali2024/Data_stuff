import os
import pandas as pd
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader

# dataset/
#     A/
#         img1.jpg
#         img2.jpg
#         ...
#     B/
#         img1.jpg
#         img2.jpg
#         ...


class CustomDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        """
        Args:
            root_dir (string): Directory with all the images organized in subfolders named after class labels.
            transform (callable, optional): Optional transform to be applied on a sample.
        """
        self.root_dir = root_dir
        self.transform = transform
        
        # List all the subfolders (class names)
        self.class_names = sorted(os.listdir(root_dir))
        self.class_to_idx = {class_name: i for i, class_name in enumerate(self.class_names)}
        
        # Collect all image file paths and their corresponding labels
        self.image_paths = []
        self.labels = []
        
        for class_name in self.class_names:
            class_dir = os.path.join(root_dir, class_name)
            for img_name in os.listdir(class_dir):
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):  # You can add more extensions if needed
                    self.image_paths.append(os.path.join(class_dir, img_name))
                    self.labels.append(self.class_to_idx[class_name])
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label


if __name__ == "__main__":
    # Define any transformations you want to apply
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
    ])

    # Instantiate the dataset
    dataset = CustomDataset(root_dir='path/to/dataset', transform=transform)

    # Create a DataLoader
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)

    for images, labels in dataloader:
        # Your training code here
        print(images,labels)