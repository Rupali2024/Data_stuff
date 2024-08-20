from PIL import Image, ImageDraw
import numpy as np

def read_yolo_annotations(file_path):
    """
    Reads the YOLO annotation file and returns a list of bounding boxes.
    Each bounding box is represented as (class_id, x_center, y_center, width, height).
    """
    annotations = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 5:
                raise ValueError("Each annotation line must have exactly 5 values.")
            class_id = int(parts[0])
            x_center, y_center, width, height = map(float, parts[1:])
            annotations.append((class_id, x_center, y_center, width, height))
    return annotations

def convert_to_pixel_coords(x_center, y_center, width, height, img_width, img_height):
    """
    Converts YOLO normalized coordinates to pixel coordinates.
    """
    x_center_pix = int(x_center * img_width)
    y_center_pix = int(y_center * img_height)
    width_pix = int(width * img_width)
    height_pix = int(height * img_height)
    
    # Compute bounding box corners
    x_min = x_center_pix - width_pix // 2
    x_max = x_center_pix + width_pix // 2
    y_min = y_center_pix - height_pix // 2
    y_max = y_center_pix + height_pix // 2
    
    return x_min, y_min, x_max, y_max

def create_blank_image(width, height):
    """
    Creates a blank binary image with the given dimensions.
    """
    return Image.new('L', (width, height), 0)  # 'L' mode for grayscale (binary)

def draw_annotations(image, annotations, img_width, img_height):
    """
    Draws bounding boxes from YOLO annotations on the image.
    """
    draw = ImageDraw.Draw(image)
    for _, x_center, y_center, width, height in annotations:
        x_min, y_min, x_max, y_max = convert_to_pixel_coords(
            x_center, y_center, width, height, img_width, img_height
        )
        draw.rectangle([x_min, y_min, x_max, y_max], outline=1, fill=1)  # Fill with white (255) for binary

def save_image(image, output_path):
    """
    Saves the image to the specified file path.
    """
    image.save(output_path)

def process_yolo_annotations(annotation_file, image_size, output_image_file):
    """
    Processes YOLO annotations and creates a binary image.
    """
    annotations = read_yolo_annotations(annotation_file)
    width, height = image_size
    image = create_blank_image(width, height)
    draw_annotations(image, annotations, width, height)
    save_image(image, output_image_file)

# Example usage
annotation_file = 'annotations.txt'  # Path to your YOLO annotation file
image_size = (512, 512)  # Replace with actual dimensions (width, height)
output_image_file = 'binary_image.png'  # Path to save the resulting image

process_yolo_annotations(annotation_file, image_size, output_image_file)
