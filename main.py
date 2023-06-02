# This is the image sorting program that I built
# It takes a directory of images and sorts them into folders based on their
#  resolution and aspect ratio
# Also, it can be used to sort images based on their content (OCR) and (Face Recognition)

import os
import os.path as path
import shutil as sh
from keywords import CLASSIFIERS, ALBUM_ART, IMAGES
from fnmatch import fnmatch
from PIL import Image, UnidentifiedImageError
import pytesseract
import face_recognition

# Path to the directory containing the images
FOLDER_TO_SCAN = "C:/Users/Advik/Pictures/Imported"

# List all the files in the directory (and subdirectories)
files = []
album_art = []
broken = []
people = []

FOLDER_TO_SCAN = path.abspath(FOLDER_TO_SCAN)
pytesseract.pytesseract.tesseract_cmd = path.abspath("./Tesseract-OCR/tesseract.exe")


for root, dirnames, filenames in os.walk(FOLDER_TO_SCAN):
    for filename in filenames:
        files.extend(
            path.join(root, filename)
            for pattern in IMAGES
            if fnmatch(filename, pattern)
        )

# Create a directory for each classifier
for classifier in CLASSIFIERS:
    if not path.isdir(classifier):
        os.mkdir(classifier)


_face_recognition = True

# Loop over each image
for image in files:
    _face_recognition = True
    # Get the image size (width, height)
    try:
        img_object = Image.open(image)
        size = img_object.size

    except UnidentifiedImageError:
        print(f"Broken Image: {image}")
        broken.append(image)
        continue


    # If the size matches any of the classifiers, mark it for moving
    if size == ALBUM_ART:
        album_art.append(image)
        print(f"Album art: {image}")
        continue

    # OCR the Image
    text = pytesseract.image_to_string(img_object)
    text = text.casefold()
    for classifier in CLASSIFIERS:
        for keyword in CLASSIFIERS[classifier]:
            if keyword in text:
                # sh.move(image, classifier)
                print(f"Moved {image} to {classifier}")
                _face_recognition = False
                break

    # Face Recognition
    # if _face_recognition:

