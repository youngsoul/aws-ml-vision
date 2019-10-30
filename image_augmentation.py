# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import numpy as np
import argparse
import logging
from pathlib import Path


def augment_images(files, output_dir, total=10):

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for image_name in files:
        print(image_name)
        image_file_name = image_name.split("/")[-1]
        # load the input image, convert itto a numpy array and then reshape it to have an extra dimension
        image = load_img(image_name)
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)

        # construct the actual python generator
        logging.debug("generating images...")
        imageGen = aug.flow(image, batch_size=1, save_to_dir=output_dir, save_prefix=image_file_name, save_format="jpg")

        for image in imageGen:
            # increment counter
            total += 1

            # if we have reach the specifiedc number of examples, break from the loop
            if total == total:
                break

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':

    # construct the argument parser


    # construct the image generator for the data augmentation then
    # initialize the total number of images generated thus far
    aug = ImageDataGenerator(
        rotation_range=30,
        zoom_range=0.15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    total = 0


    path = Path('./data/dataset/coffee')
    files = [e for e in path.iterdir() if e.is_file()]

    augment_images(files, './data/dataset_aug/coffee', 10)