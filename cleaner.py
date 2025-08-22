import os
import re

def clean_filename(name: str) -> str:
    # Remove leading "Fig - <number>" if present
    name = re.sub(r"^(fig(?:ure)?\.?\s*[-–—]?\s*\d+\s*)", "", name, flags=re.IGNORECASE)

    # Remove '-min' or similar endings
    name = re.sub(r"-min$", "", name, flags=re.IGNORECASE)

    # Lowercase
    name = name.lower()

    # Replace commas, hyphens, and brackets
    name = name.replace(",", "")
    name = name.replace("(", " ")
    name = name.replace(")", " ")

    # Replace spaces and dashes with underscores
    name = re.sub(r"[ \t\-–—]+", "_", name)

    # Remove leading/trailing underscores
    name = name.strip("_")

    return name


def rename_images(folder_path: str):
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

    # Iterate over files in the folder, skip non-image files
    for filename in os.listdir(folder_path):
        old_path = os.path.join(folder_path, filename)
        if not os.path.isfile(old_path):
            continue

        name, ext = os.path.splitext(filename)
        if ext.lower() not in image_extensions:
            continue

        new_name = clean_filename(name) + ext.lower()
        new_path = os.path.join(folder_path, new_name)

        # Avoid overwriting
        if os.path.exists(new_path):
            print(f"Skipping {filename}, {new_name} already exists.")
            continue

        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")


if __name__ == "__main__":
    folder = input("Enter the folder path: ").strip('"')
    rename_images(folder)
