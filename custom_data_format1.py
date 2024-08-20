import os
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader

# images/
#     img1_classA.jpg
#     img2_classB.jpg
#     img3_classA.jpg
#     ...


class CustomDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        """
        Args:
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied on a sample.
        """
        self.root_dir = root_dir
        self.transform = transform
        
        # List all image file paths
        self.image_paths = []
        self.labels = []
        
        # Collect image paths and labels
        for img_name in os.listdir(root_dir):
            if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):  # You can add more extensions if needed
                class_label = img_name.split('_')[1].split('.')[0]  # Extract class label from filename
                img_path = os.path.join(root_dir, img_name)
                
                self.image_paths.append(img_path)
                self.labels.append(class_label)
        
        # Create a mapping from class labels to indices
        self.class_names = sorted(set(self.labels))
        self.class_to_idx = {class_name: i for i, class_name in enumerate(self.class_names)}
        self.labels = [self.class_to_idx[label] for label in self.labels]
    
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
    dataset = CustomDataset(root_dir='path/to/images', transform=transform)

    # Create a DataLoader
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)

    for images, labels in dataloader:
        # Your training code here
        print(images, labels)
