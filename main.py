import os
import shutil
import csv

def organize_folder():
    #input
    folder_path = input("Enter folder path: ").strip().replace('"', '')

    if not os.path.exists(folder_path):
        print("Folder not found!")
        return

    # Loop
    for file_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_name)

        # Skip if  folder 
        if os.path.isdir(full_path) or file_name == "history.csv":
            continue

        # Detect file types
        name, ext = os.path.splitext(file_name)
        ext = ext.lower()

        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            category = "Images"
        elif ext in ['.pdf', '.docx', '.txt', '.xlsx']:
            category = "Documents"
        elif ext in ['.mp4', '.mkv', '.mov']:
            category = "Videos"
        elif ext in ['.zip', '.rar']:
            category = "Archives"
        else:
            category = "Others"

        #Create folder
        dest_folder = os.path.join(folder_path, category)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        #Handle duplicates
        target_path = os.path.join(dest_folder, file_name)
        if os.path.exists(target_path):
            target_path = os.path.join(dest_folder, name + "_copy" + ext)

        #Move and Record in CSV
        try:
            shutil.move(full_path, target_path)
            with open("history.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([file_name, category])
            print("Moved:", file_name)
        except:
            print("Error moving:", file_name)

if __name__ == "__main__":
    organize_folder()