import imutils
from pathlib import Path
import random, string
import argparse
import time
import os
import cv2
from collections import defaultdict

def resize_square(image, new_size, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    height = None
    width = None
    if h > w:
        height = new_size
    else:
        width = new_size


    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-dir", type=str, required=True, help="name of the directory that contains images")
    ap.add_argument("--to-dir", type=str, required=True, help="name of the directory to write resized images")
    ap.add_argument("--to-size", type=int, required=True, help="resize to square of size by size")
    ap.add_argument("--max-images-per-label", type=int, required=True, help="maximum number of images per label")
    # ap.add_argument("-n", "--s3_path", type=str, required=True, help="sftp hostname")

    args = vars(ap.parse_args())

    to_size = args['to_size']
    from_dir = args['from_dir']
    to_dir = args['to_dir']
    max_images_per_label = args['max_images_per_label']


    from_files_path = Path(from_dir).glob('**/*')
    from_files = [x for x in from_files_path if x.is_file()]

    max_images_per_label_count = defaultdict(int)

    for unresized_files in from_files:
        from_dir_leaf = unresized_files.parts[-2]
        current_label_count = max_images_per_label_count[from_dir_leaf]
        if current_label_count > max_images_per_label:
            continue
        else:
            max_images_per_label_count[from_dir_leaf] = current_label_count+1

        image_name = unresized_files.parts[-1]
        # create output
        Path(f"{to_dir}_{to_size}_{to_size}", from_dir_leaf).mkdir(parents=True, exist_ok=True)
        to_file = Path(f"{to_dir}_{to_size}_{to_size}", from_dir_leaf) / image_name
        unresized_image = cv2.imread(str(unresized_files))
        resized_image = resize_square(unresized_image, new_size=to_size)

        # we want a fixed size height and width so add/expand a border if we need to
        # https://jdhao.github.io/2017/11/06/resize-image-to-square-with-padding/
        resized_image_shape = resized_image.shape  # (rows, columns, channels )  (height, width, channels)
        delta_w = to_size - resized_image_shape[1]
        delta_h = to_size - resized_image_shape[0]

        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)

        new_im = cv2.copyMakeBorder(resized_image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0,0,0])

        cv2.imwrite(str(to_file), img=new_im)





