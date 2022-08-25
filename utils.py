from importlib.resources import path
import logging


def get_images_from_folder(folderPath):
    """
    Takes a folder path and returns a ([actual_images],[not_images]) from the folder.
    Returns only names. Not complete path
    """
    from os import listdir
    from os.path import isdir, join
    from PIL import Image

    if not isdir(folderPath):
        raise Exception("Please provide a valid input folder")

    all_files = listdir(folderPath)
    actual_images, not_images = [], []
    for file in all_files:
        try:
            img = Image.open(join(folderPath, file))
            if img.format.lower() in ["png", "jpg", "jpeg", "tiff"]:
                actual_images.append(file)
        except Exception as E:
            logging.debug(E)
            not_images.append(file)

    return actual_images, not_images


def join_path_list(basePath, filenames):
    from os.path import join

    final_paths = []
    for filename in filenames:
        final_paths.append(join(basePath, filename))
    return final_paths


def verify_folder(folder_path, create=False):
    from os.path import isdir
    from os import mkdir

    if not folder_path:
        raise Exception("Please provide a video input file with -i or --input_file")
    if not isdir(folder_path):
        if create:
            logging.info("Creating folder at path {}".format(folder_path))
            mkdir(folder_path)
        else:
            raise Exception(
                "{} is not a valid directory. Please provide a valid directory".format(
                    folder_path
                )
            )
