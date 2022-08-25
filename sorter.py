import argparse, pickle, custom_logger
from asyncio.log import logger
from os.path import isfile
from logging import INFO, DEBUG, WARN
import utils
import logging

createModelString = "create_model"
performSortingString = "perform_sorting"
imageString = "image"
videoString = "video"

parser = argparse.ArgumentParser(
    description="A program to sort images based on face occourance"
)

parser.add_argument(
    "mode",
    choices=[createModelString, performSortingString],
    type=str,
    help="Tells the program which action to perform",
)

parser.add_argument(
    "-t",
    "--input_type",
    choices=["image", "video"],
    type=str,
    help="Specifies the type of input",
)

parser.add_argument(
    "-i",
    "--input_file",
    type=str,
    help="Input file for the video to perform training on",
)

parser.add_argument(
    "-f",
    "--input_folder",
    type=str,
    help="Input folder for the images to perform training on",
)

parser.add_argument(
    "-n",
    "--name",
    type=str,
    help="Name required to store the face modelogging.infoprocl used for recongition",
)

parser.add_argument(
    "--processes",
    type=int,
    default=1,
    help="Number of processes to use (for perfoming sorting)",
)

parser.add_argument(
    "--debug",
    action="store_true",
    help="Add this argument to enable debug mode",
)


args = parser.parse_args()

if args.debug:
    custom_logger.initialize_logger(logger_level=DEBUG)
else:
    custom_logger.initialize_logger(logger_level=INFO)

if args.mode == createModelString:
    if args.name == None:
        raise Exception(
            "Please provide your name to save your face model with -n or --name"
        )

    if args.input_type == "image":

        actual_images, not_images = utils.get_images_from_folder(args.input_folder)
        logging.info(
            "Images found in folder (These will be scanned) : {}".format(actual_images)
        )
        logging.info("Non-Images found in folder : {}".format(not_images))

        if len(actual_images) == 0:
            raise Exception("No suitable images found in folder provided")

        logging.info("Tests passed, starting scan now")
        import recognition_engine

        actual_images = utils.join_path_list(args.input_folder, actual_images)
        encodings = recognition_engine.train_from_images(
            actual_images, debug=args.debug
        )
        logging.debug(encodings)
        with open("{}.pkl".format(args.name), "wb") as f:
            pickle.dump(encodings, f)
        logging.info("Khatam!")

    elif args.input_type == "video":

        if args.input_file == None:
            raise Exception("Please provide a video input file with -i or --input_file")

        if not isfile(args.input_file):
            raise Exception(
                "'{}' is not a valid file. Please provide a valid file".format(
                    args.input_file
                )
            )

        import recognition_engine

        encodings = recognition_engine.train_from_video(
            video_path=args.input_file, debug=args.debug
        )
        with open("{}.pkl".format(args.name), "wb") as f:
            pickle.dump(encodings, f)
        logging.info("Khatam!")
    else:
        raise Exception("You need to specify input type with -t or --input_type")
elif args.mode == performSortingString:
    if args.name == None:
        raise Exception(
            "Please provide the name you gave while creating the model with -n or --name"
        )
    # TODO remove verify folder or change images to sort implementation
    utils.verify_folder(args.input_folder)

    images_to_sort, not_to_sort = utils.get_images_from_folder(args.input_folder)
    final_paths = utils.join_path_list(args.input_folder, images_to_sort)

    encodings = None
    try:
        with open("{}.pkl".format(args.name), "rb") as f:
            encodings = pickle.load(f)
    except Exception as E:
        logger.critical(E)
        exit(1)

    found_directory = "found_directory"
    not_found_directory = "not_found_directory"

    utils.verify_folder(folder_path=found_directory, create=True)
    utils.verify_folder(folder_path=not_found_directory, create=True)

    threading = False if args.processes == 1 else True

    import recognition_engine

    recognition_engine.sort_into_directories(
        images_to_test=final_paths,
        perform_transfer=True,
        debug=args.debug,
        verbose=True,
        threading=False,
        target_encodings=encodings,
        n_workers=args.processes,
    )

    logging.info("Khatam!")

    logging.info("Ruko zara, sabar kato")
