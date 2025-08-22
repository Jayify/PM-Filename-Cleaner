import os
import re
import tinify
from dotenv import load_dotenv

# Load secrets
load_dotenv()
tinify.key = os.getenv("TINIFY_API_KEY")


def clean_filename(name: str) -> str:
    # Remove leading "Fig 3", "Fig. 3", "Figure 3", etc.
    name = re.sub(r"^(fig(?:ure)?\.?\s*[-–—]?\s*\d+\s*)", "", name, flags=re.IGNORECASE)

    # Remove '-min', '–min', '—min' at the end
    name = re.sub(r"[-–—]min$", "", name, flags=re.IGNORECASE)

    # Lowercase
    name = name.lower()

    # Replace commas and brackets
    name = name.replace(",", "")
    name = name.replace("(", " ")
    name = name.replace(")", " ")

    # Replace spaces and any dashes with underscores
    name = re.sub(r"[ \t\-–—]+", "_", name)

    # Remove leading/trailing underscores
    name = name.strip("_")

    return name


def rename_and_compress(folder_path: str, compress: bool):
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    count = 0

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

        if compress:
            try:
                source = tinify.from_file(new_path)
                source.to_file(new_path)
                print(f"- Renamed + Compressed: {filename} -> {new_name}")
                count += 1
            except tinify.Error as e:
                print(f"Tinify error for {new_name}: {e}")
        else:
            print(f"- Renamed: {filename} -> {new_name}")
            count += 1
    print(f"\nTotal files processed: {count}")


if __name__ == "__main__":
    print("Filename Cleaner\n")

    folder = input("Enter the folder path: ").strip('"')

    choice = input("Compress images with TinyPNG? This will take a lot longer. (y/n): ").strip().lower()
    compress = choice.startswith("y")
    print()

    rename_and_compress(folder, compress)
