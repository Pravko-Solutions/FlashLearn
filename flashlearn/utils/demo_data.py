import os
import random
import base64
import csv
from io import BytesIO

import kagglehub
from PIL import Image


def encode_image_to_base64(image_path: str) -> str:
    """
    Encodes an image to a base64 JPEG string.
    :param image_path: File path of the image
    :return: Base64 encoded string of the image
    """
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")


def cats_and_dogs(sample: int = 100, train_ratio: float = 0.5):
    """
    Returns two lists of dictionaries (train_data, test_data) with base64-encoded
    images of cats and dogs. Each dictionary has:
      {
        "image_base64": <base64encodedimage>,
        "label": 0 or 1
      }
    The first list is the 'train' portion, and the second is 'test'.

    :param sample: Total number of images to sample from the dataset.
    :param train_ratio: Fraction of data to put in the training set.
    :return: (train_data, test_data)
    """
    # Download and locate the dataset
    path = kagglehub.dataset_download("samuelcortinhas/cats-and-dogs-image-classification")
    cats_dir = os.path.join(path, "train", "cats")
    dogs_dir = os.path.join(path, "train", "dogs")

    # Gather and sample file paths
    cat_images = [os.path.join(cats_dir, f) for f in os.listdir(cats_dir)
                  if f.lower().endswith((".jpg", ".jpeg"))]
    dog_images = [os.path.join(dogs_dir, f) for f in os.listdir(dogs_dir)
                  if f.lower().endswith((".jpg", ".jpeg"))]

    # Sample equally from cats and dogs
    half_sample = sample // 2
    cat_sample = random.sample(cat_images, half_sample)
    dog_sample = random.sample(dog_images, half_sample)

    # Encode images and build list of dicts
    data = []
    for img_path in cat_sample:
        encoded_image = encode_image_to_base64(img_path)
        data.append({"image_base64": encoded_image, "label": 0})
    for img_path in dog_sample:
        encoded_image = encode_image_to_base64(img_path)
        data.append({"image_base64": encoded_image, "label": 1})

    return data


def imdb_reviews_50k(sample: int = 100, full=False):
    """
    Returns IMDb reviews as two lists of dicts (train_data, test_data).
    Each dict has:
      {
        "review": <the text>,
        "sentiment": <"positive" or "negative">
      }

    The first list is the 'train' portion (10% by default),
    the second list is the 'test' portion.

    :param sample: Number of total samples to extract from the dataset.
    :return: (train_data, test_data)
    """
    # Download and load the IMDb dataset (CSV)
    dataset_path = kagglehub.dataset_download("lakshmi25npathi/imdb-dataset-of-50k-movie-reviews")
    csv_path = os.path.join(dataset_path, "IMDB Dataset.csv")

    # Read CSV as list of dicts
    all_rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # fieldnames from header: "review","sentiment"
        for row in reader:
            # row is {"review": ..., "sentiment": ...}
            all_rows.append(row)

    if not full:
        # Sample a random subset if needed
        if sample < len(all_rows):
            all_rows = random.sample(all_rows, sample)

        # Shuffle the data
        random.shuffle(all_rows)

    return all_rows