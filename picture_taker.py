import cv2
from pathlib import Path
import random, string
import argparse
import time
import os

def get_video():
    # load the video
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    time.sleep(1)
    return camera


def get_pictures(picture_directory, base_image_name, image_suffix=None, use_random=True):

    # make directory
    Path(picture_directory).mkdir(parents=True, exist_ok=True)

    camera = get_video()
    pictures = []

    print("Taking Picture! ")
    print("Press 's' to take  picture")
    print("Press 'q' to stop taking pictures")
    print("Make sure you select the video window before pressing 'q' or 's'")
    while True:
        # q - to quit this loop
        # s to take a picture

        (grabbed, frame) = camera.read()

        if not grabbed:
            print("OOPS.. did not grab a picture")
            break

        cv2.imshow("Frame: ", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            if use_random:
                rand_val = ''.join(
                    random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(5))
                rand_val = f"_{rand_val}"
            else:
                rand_val = ""

            if image_suffix:
                image_name = f"{picture_directory}/{base_image_name}{rand_val}_{image_suffix}.png"
            else:
                image_name = f"{picture_directory}/{base_image_name}{rand_val}.png"

            print(f"Saving picture to: {image_name}")
            cv2.imwrite(image_name, img=frame)

        elif key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-name", type=str, required=True, help="name of the dataset")
    ap.add_argument("--image-suffix", type=str, required=False, help="suffix added to image as, _<suffix>")
    ap.add_argument("--data-dir", type=str, required=True, help="folder containing the datasets")
    ap.add_argument("--random-part", type=str, required=False, default="true", help="true - put random string in file, false no random string")
    # ap.add_argument("-n", "--s3_path", type=str, required=True, help="sftp hostname")

    args = vars(ap.parse_args())

    dataset_name = args['dataset_name']
    suffix = args['image_suffix']
    data_dir = args['data_dir']
    random_suffix = args['random_part']
    if random_suffix == 'true':
        random_suffix = True
    else:
        random_suffix = False

    print(random_suffix)


    new_pictures_path = os.path.join('.', 'data', data_dir, dataset_name)
    get_pictures(new_pictures_path, dataset_name, image_suffix=suffix, use_random=random_suffix)

