from pathlib import Path
import random
import shutil

# Change this path to the directory containing the 4 class folders
SOURCE_DIR = Path("datasets/cotton/cotton")

OUTPUT_DIR = Path("datasets/cotton_split")

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

random.seed(42)


def split_dataset():

    if not SOURCE_DIR.exists():
        raise FileNotFoundError(
            f"Dataset folder not found: {SOURCE_DIR}"
        )

    class_folders = [
        folder for folder in SOURCE_DIR.iterdir()
        if folder.is_dir()
    ]

    if not class_folders:
        raise ValueError(
            "No class folders found. Check SOURCE_DIR."
        )

    for class_folder in class_folders:

        images = [
            file for file in class_folder.iterdir()
            if file.suffix.lower() in IMAGE_EXTENSIONS
        ]

        random.shuffle(images)

        total = len(images)

        if total < 5:
            raise ValueError(
                f"Too few images in {class_folder.name}"
            )

        train_end = int(total * 0.70)
        val_end = int(total * 0.85)

        splits = {
            "train": images[:train_end],
            "validation": images[train_end:val_end],
            "test": images[val_end:]
        }

        for split_name, files in splits.items():

            destination = (
                OUTPUT_DIR / split_name / class_folder.name
            )
            destination.mkdir(parents=True, exist_ok=True)

            for image_file in files:
                shutil.copy2(
                    image_file,
                    destination / image_file.name
                )

        print(
            class_folder.name,
            "Total:", total,
            "Train:", len(splits["train"]),
            "Validation:", len(splits["validation"]),
            "Test:", len(splits["test"])
        )

    print("\nDataset splitting completed!")


if __name__ == "__main__":
    split_dataset()