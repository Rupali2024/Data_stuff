import os

def get_base_name(file_name):
    """Extract the base name from a file name, ignoring the extension."""
    return os.path.splitext(file_name)[0]

def list_base_names(directory):
    """List all base names of files in a given directory."""
    return {get_base_name(file) for file in os.listdir(directory)}

def list_files(directory):
    """List all files in a given directory."""
    return set(os.listdir(directory))

def compare_folders(folder1, folder2):
    """Compare files in two folders and identify files with the same names and different names."""
    # files_folder1 = list_files(folder1)
    # files_folder2 = list_files(folder2)

    files_folder1 = list_base_names(folder1)
    files_folder2 = list_base_names(folder2)

    # Files with the same names in both folders
    common_files = files_folder1.intersection(files_folder2)

    # Files only in folder1
    unique_to_folder1 = files_folder1 - files_folder2

    # Files only in folder2
    unique_to_folder2 = files_folder2 - files_folder1

    return {
        'common_files': common_files,
        'unique_to_folder1': unique_to_folder1,
        'unique_to_folder2': unique_to_folder2
    }

folder1 = 'LINKNET/linknet_data/masked'
folder2 = 'LINKNET/tst'

results = compare_folders(folder1, folder2)
import cv2

print("Files with the same names in both folders:")
for filename in results['common_files']:
    print(filename)
    path = filename+'.jpg'
    image = cv2.imread(os.path.join(folder2,path))

    new_path = os.path.join("LINKNET/linknet_data/images",filename+".png")
    cv2.imwrite(new_path,image)
    

print("\nFiles only in the first folder:")
for filename in results['unique_to_folder1']:
    print(filename)

print("\nFiles only in the second folder:")
for filename in results['unique_to_folder2']:
    print(filename)
