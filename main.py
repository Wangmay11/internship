import os
import shutil

# a text file to remember log for the undo
LOG_FILE = "undo_data.txt"

def organize_me():
    folder_path = input("Paste the folder path here: ").strip().replace('"', '')
    
    if not os.path.exists(folder_path):
        print("That folder doesn't exist!")
        return

    # Get all files in the folder
    files = os.listdir(folder_path)

    for f in files:
        full_path = os.path.join(folder_path, f)

        # skip folders, we only want files
        if os.path.isdir(full_path):
            continue
        
        # skip own file log if in the same folder
        if f == LOG_FILE:
            continue

        # extension call
        name, ext = os.path.splitext(f)
        ext = ext.lower()

        # Decides the folder
        subfolder = "Other" # default
        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            subfolder = "Images"
        elif ext in ['.pdf', '.docx', '.txt', '.xlsx', '.csv']:
            subfolder = "Documents"
        elif ext in ['.mp4', '.mov', '.avi']:
            subfolder = "Videos"
        elif ext in ['.zip', '.rar']:
            subfolder = "Archives"

        # Create the subfolder path
        target_dir = os.path.join(folder_path, subfolder)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)

        # Handling if file already exists 
        final_destination = os.path.join(target_dir, f)
        if os.path.exists(final_destination):
            final_destination = os.path.join(target_dir, name + "_new" + ext)

        # Move file
        try:
            shutil.move(full_path, final_destination)
            
            # Save the move to our log for undo
            # Format: CurrentPath|OldPath
            with open(LOG_FILE, "a") as my_log:
                my_log.write(final_destination + "|" + full_path + "\n")
                
            print(f"Moved {f} to {subfolder}")
        except:
            print(f"Could not move {f}")

def undo_everything():
    if not os.path.exists(LOG_FILE):
        print("Nothing to undo.")
        return

    with open(LOG_FILE, "r") as my_log:
        lines = my_log.readlines()

    if not lines:
        print("Log is empty.")
        return

    print("Undoing moves...")
    # Reverse the lines to move back the last things first
    for line in reversed(lines):
        parts = line.strip().split("|")
        if len(parts) == 2:
            now_at = parts[0]
            was_at = parts[1]
            if os.path.exists(now_at):
                shutil.move(now_at, was_at)
                print(f"Moved back: {os.path.basename(was_at)}")

    # Delete log content after undo
    open(LOG_FILE, "w").close()
    print("All back to normal!")

# choice
while True:
    print("\n--- MY FOLDER CLEANER ---")
    print("1. Organize")
    print("2. Undo")
    print("3. Exit")
    
    cmd = input("Pick 1, 2, or 3: ")
    
    if cmd == "1":
        organize_me()
    elif cmd == "2":
        undo_everything()
    elif cmd == "3":
        print("wasted")
        break
    else:
        print("Wrong input!")