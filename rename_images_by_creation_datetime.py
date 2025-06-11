import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_creation_datetime(image_path):
    """
    Trys to extract the original creation date time form EXIF data of image.
    Uses 'DateTimeOriginial' oveer 'DateTimeDigitized' if possible.
    :param path of image
    :return: datetime object
    """
    try:
        img = Image.open(image_path)
        exif_data = img.getexif()

        if exif_data is not None:
            exif_tags = {TAGS.get(tag): value for tag, value in exif_data.items()}
            datetime_original_tag = 'DateTimeOriginal'
            datetime_digitized_tag = 'DateTimeDigitized'
            datetime_tag = 'DateTime'

            if datetime_original_tag in exif_tags:
                date_str = exif_tags[datetime_original_tag]
            elif datetime_digitized_tag in exif_tags:
                date_str = exif_tags[datetime_digitized_tag]
            elif datetime_tag in exif_tags:
                date_str = exif_tags[datetime_tag]
            else:
                return None

            # replace first two colons with dashes (YYYY:MM:DD HH:MM:SS to YYYY-MM-DD HH:MM:SS)
            date_str = date_str.replace(':', '-',2)
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        pass
    return None

def rename_images_by_creation_datetime(folder_path):
    """
    Renames image files (jpg, png, jpeg) in a specific folder to ther EXIF creation date and time
    Falls back to file system creation date if no EXIF date is found
    :param path of folder
    """

    if not os.path.isdir(folder_path):
        print(f"Error: The specified folder '{folder_path}' does not exist.")
        return

    print(f"Starting to rename image files in: '{folder_path}'")
    renamed_count = 0
    errors_count = 0
    skipped_count = 0

    for filename in os.listdir(folder_path):
        current_file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(current_file_path) and (filename.lower().endswith(('.jpg', '.png', '.jpeg'))):
            try:
                # Try to get EXIF creation date
                creation_datetime = get_exif_creation_datetime(current_file_path)

                if creation_datetime is None:
                    # Fallback to file creation date if no EXIF date is found
                    print(f"Warning: no EXIF date found for '{filename}'. Using file system creation date.")
                    creation_timestamp = os.path.getctime(current_file_path)
                    creation_datetime = datetime.fromtimestamp(creation_timestamp)

                base_name = creation_datetime.strftime('%Y-%m-%d_%H-%M-%S')
                file_extension = os.path.splitext(filename)[1].lower()

                new_file_name = f"{base_name}{file_extension}"
                new_file_path = os.path.join(folder_path, new_file_name)

                #handle potential duplicatie filenames
                counter = 1
                while os.path.exists(new_file_path) and new_file_path != current_file_path:
                    new_file_name = f"{base_name}_{counter}{file_extension}"
                    new_file_path = os.path.join(folder_path, new_file_name)
                    counter+=1

                if current_file_path != new_file_path:
                    os.rename(current_file_path, new_file_path)
                    print(f"Renamed '{filename}' to '{new_file_name}'")
                    renamed_count += 1
                else:
                    print(f"Skipped '{filename}': Already has the correct filename based on its EXIF/creation date.")
                    skipped_count += 1

            except Exception as e:
                print(f"Error processing '{filename}': {e}")
                errors_count += 1
        elif os.path.isfile(current_file_path):
            skipped_count += 1

        print(f"\n--- Renaming process complete ---")
        print(f"Total files renamed: {renamed_count}")
        print(f"Total files skipped (non-image or already named correctly): {skipped_count}")
        print(f"Total errors encountered: {errors_count}")

script_directory = os.path.dirname(os.path.abspath(__file__))
folder_to_process = script_directory # This is generally safer for scripts

rename_images_by_creation_datetime(folder_to_process)
