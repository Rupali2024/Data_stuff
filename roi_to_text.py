import cv2
import os

def convert_to_yolo_format(x1, y1, x2, y2, img_width, img_height):
    # Calculate YOLO format coordinates
    x_center = (x1 + x2) / 2 / img_width
    y_center = (y1 + y2) / 2 / img_height
    width = (x2 - x1) / img_width
    height = (y2 - y1) / img_height
    return x_center, y_center, width, height

def save_yolo_annotation(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img,(640,500))
    rois = cv2.selectROI(img)
    img_height, img_width = img.shape[:2]

    base_name = os.path.splitext(os.path.basename(image_path))[0]

    txt_file_path = f"{base_name}.txt"
    img_file_path = f"{base_name}.jpg"
    txt_file_path = os.path.join(dst_path,txt_file_path)
    img_file_path = os.path.join(dst_path_img,img_file_path)
    cv2.imwrite(img_file_path,img)


    with open(txt_file_path, 'w') as f:
        print(rois)
        # for roi in rois:
        x1, y1, x2, y2 = rois
        x_center, y_center, width, height = convert_to_yolo_format(x1, y1, x1+x2, y1+y2, img_width, img_height)
        # Assuming object class is 0 (adjust as needed)
        f.write(f"0 {x_center} {y_center} {width} {height}\n")

def main(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            
            save_yolo_annotation(image_path)

if __name__ == "__main__":
    folder_path = "LINKNET/final_data/images/val"  
    dst_path = "LINKNET/final_data1/labels/val"
    dst_path_img = "LINKNET/final_data1/images/val"
    os.makedirs(dst_path,exist_ok=True)
    os.makedirs(dst_path_img,exist_ok=True)
    main(folder_path)
