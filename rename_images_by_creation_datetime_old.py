import os
from datetime import datetime

def rename_images_by_creation_datetime(folder_path):
    for filename in os.listdir(folder_path):
        current_file_path = os.path.join(folder_path, filename)
        if os.path.isfile(current_file_path) and (filename.lower().endswith(('.jpg', '.png', '.jpeg'))):
            try:
                creation_timestamp = os.path.getctime(current_file_path)
                creation_datetime = datetime.fromtimestamp(creation_timestamp)
            
                # format for date in filename
                base_name = creation_datetime.strftime('%Y-%m-%d_%H-%M-%S')
                file_extension = os.path.splitext(filename)[1].lower()

                new_file_name = f"{base_name}{file_extension}"
                new_file_path = os.path.join(folder_path, new_file_name)

                # handle potential duplicate filenames
                counter = 1;
                while os.path.exists(new_file_path) and new_file_path != current_file_path:
                    new_file_name = f"{base_name}_{counter}{file_extension}"
                    new_file_path = os.path.join(folder_path, new_file_name)
                    counter += 1

                if current_file_path != new_file_path:
                    os.rename(current_file_path, new_file_path)
                    print(f"Renamed '{filename}' to '{new_file_name}'")
                else:
                    print(f"Skipped '{filename}': Already has the correct filename based on its EXIF/creation date.")

            except Exception as e:
                print(f"Error processing '{filename}': {e}")

folder_path = os.getcwd()
rename_images_by_creation_datetime(folder_path)


