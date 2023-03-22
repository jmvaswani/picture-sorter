import argparse

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
    help="Name required to store the face model used for recongition",
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
