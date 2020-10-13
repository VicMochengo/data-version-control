from pathlib import Path

import pandas as pd

FOLDERS_TO_LABELS = {"n03445777": "golf ball", "n03888257": "parachute"}
#maps labels to what is contained in the folders i.e. files in folder "n03445777" all contain images of golf 
#in this case we only want to label images containing golf balls and parachutes

def get_files_and_labels(source_path):
    """this function does a series of related events that access image files and label them:
    - creates empty lists for the images and labels
    - looks in to the source path for files with jpeg extension and identifies them as images
    - matches the image files folder to the parent folder
    - labels images based on connection between parent folder and assigned labels
    - returns images with assigned labels
    """
    images = []
    labels = []
    for image_path in source_path.rglob("*/*.JPEG"):
        filename = image_path.absolute()
        folder = image_path.parent.name
        if folder in FOLDERS_TO_LABELS:
            images.append(filename)
            label = FOLDERS_TO_LABELS[folder]
            labels.append(label)
    return images, labels


def save_as_csv(filenames, labels, destination):
    """this function creates a dictionary and saves the identified images in CSV format containing two columns i.e image file path, label.\
    Each image file record is stored in a new row.\
    The CSVs are then stored in a specified file path.
    """
    data_dictionary = {"filename": filenames, "label": labels}
    data_frame = pd.DataFrame(data_dictionary)
    data_frame.to_csv(destination)


def main(repo_path):
    """runs the functionality of get_files_and_labels() and save_as_csv() functions, and points final storage paths accordingly
    """
    data_path = repo_path / "data"
    train_path = data_path / "raw/train"
    test_path = data_path / "raw/val"
    train_files, train_labels = get_files_and_labels(train_path)
    test_files, test_labels = get_files_and_labels(test_path)
    prepared = data_path / "prepared"
    save_as_csv(train_files, train_labels, prepared / "train.csv")
    save_as_csv(test_files, test_labels, prepared / "test.csv")


if __name__ == "__main__":
    repo_path = Path(__file__).parent.parent
    main(repo_path)
