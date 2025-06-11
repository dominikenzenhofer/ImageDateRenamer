# Image Renamer

This repository contains Python scripts to help you organize your image files by renaming them based on their creation dates.
rename_images_by_creation_datetime.py (Current Version)

This script renames image files (JPG, PNG, JPEG) in a specified folder. It intelligently prioritizes extracting the original creation date and time from the EXIF data embedded within the image. If EXIF data isn't available, it gracefully falls back to using the file system's creation date. This ensures your photos are consistently named, making them easier to sort and manage.
rename_images_by_creation_datetime_old.py (Previous Version)

This older version of the script renames image files solely based on their file system creation date. It does not attempt to read EXIF data. While functional, it may not reflect the true capture date if the file system's creation date has been altered (e.g., by copying files).
