
import os
import shutil
from pathlib import Path

# Map file extensions to categories
EXTENSION_MAP = {
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".pptx": "Documents",
    ".xlsx": "Documents",
    ".csv": "Documents",

    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",

    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",

    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",

    ".py": "Code",
    ".java": "Code",
    ".c": "Code",
    ".cpp": "Code",
    ".html": "Code",
    ".css": "Code",
    ".js": "Code",
    ".php": "Code"
}


def get_unique_path(destination):
    """Avoid overwriting a file with the same name."""
    destination = Path(destination)

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_path = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )

        if not new_path.exists():
            return new_path

        counter += 1


def organize_folder(folder_path):
    folder = Path(folder_path).expanduser().resolve()

    if not folder.is_dir():
        print("Error: Folder does not exist.")
        return

    moved = 0
    failed = 0

    print("\n=== DESKTOP FILE ORGANIZER ===")

    try:
        with os.scandir(folder) as entries:
            for entry in entries:
                if not entry.is_file():
                    continue

                source = Path(entry.path)

                # Do not move this running script
                if source.resolve() == Path(__file__).resolve():
                    continue

                category = EXTENSION_MAP.get(
                    source.suffix.lower(), "Others"
                )
                destination_folder = folder / category

                try:
                    destination_folder.mkdir(
                        parents=True, exist_ok=True
                    )

                    destination = get_unique_path(
                        destination_folder / source.name
                    )

                    shutil.move(str(source), str(destination))

                    print(
                        f"Moved: {source.name} -> "
                        f"{category}/{destination.name}"
                    )
                    moved += 1

                except (PermissionError, OSError) as error:
                    print(f"Could not move {source.name}: {error}")
                    failed += 1

    except PermissionError:
        print("Permission denied: Cannot access this folder.")
        return

    print("\n" + "=" * 35)
    print("       EXECUTION SUMMARY")
    print("=" * 35)
    print(f"Files relocated : {moved}")
    print(f"Files failed    : {failed}")
    print("=" * 35)
    print("Organization completed!")


if __name__ == "__main__":
    path = input(
        "Enter the folder path to organize: "
    ).strip().strip('"')

    organize_folder(path)
