import logging, cv2, face_recognition
from tqdm import tqdm


def train_from_video(video_path, debug=False):
    logging.info(" Starting to train on video ")
    # Get a reference to input video

    input_video = cv2.VideoCapture(video_path)

    # Initialize variables
    face_locations = []
    face_encodings = []
    length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

    logging.info(
        "Total frames in video : {} . # of Frames used for training : {}".format(
            length, length // 5
        )
    )
    total_frames = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

    sample_rate = 5
    for fno in tqdm(range(0, total_frames, sample_rate)):

        input_video.set(cv2.CAP_PROP_POS_FRAMES, fno)
        _, frame = input_video.read()

        # Find all the faces in the current frame of video
        # face_locations = face_recognition.face_locations(rgb_frame)
        face_locations = face_recognition.face_locations(frame)

        # for encoding in face_recognition.face_encodings(frame,face_locations):
        #     face_encodings.append(encoding)

        encodings_found = face_recognition.face_encodings(frame, face_locations)
        if encodings_found:
            face_encodings.append(encodings_found[0])

        if debug == True:

            # Display the results
            for top, right, bottom, left in face_locations:
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # # Display the resulting image
            cv2.imshow("Video", frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    # Release handle to the video
    input_video.release()
    cv2.destroyAllWindows()
    return encodings_found


def train_from_images(image_list, debug=False):
    logging.info(" Starting to train on images ")
    # Get a reference to input video
    # cv2.imread()

    # Initialize variables
    face_locations = []
    face_encodings = []
    length = len(image_list)

    logging.info("Total images found : {}".format(length))

    for image in tqdm(image_list):

        frame = cv2.imread(image)

        # Find all the faces in the current frame of video
        # face_locations = face_recognition.face_locations(rgb_frame)
        face_locations = face_recognition.face_locations(frame)

        # for encoding in face_recognition.face_encodings(frame,face_locations):
        #     face_encodings.append(encoding)

        encodings_found = face_recognition.face_encodings(frame, face_locations)

        if encodings_found:
            face_encodings.append(encodings_found[0])

        if debug == True:

            # Display the results
            for top, right, bottom, left in face_locations:
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            frame = cv2.resize(frame, (800, 600))
            # # Display the resulting image
            cv2.imshow("Image", frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    # Release handle to the video
    cv2.destroyAllWindows()
    return face_encodings


################################################
###Sorting code


def check_presence(image, target_encodings, draw_output=False):
    flag = False
    face_locations = face_recognition.face_locations(image)
    encodings_found = face_recognition.face_encodings(image, face_locations)
    names = []
    # logging.info(face_locations)
    for encoding in encodings_found:
        matches = face_recognition.compare_faces(
            target_encodings, encoding, tolerance=0.5
        )
        if True in matches:
            flag = True
            names.append("Zae")
        else:
            names.append("Bhagwaan jaane")
    if draw_output:
        output = image.copy()
        for (top, right, bottom, left), name in zip(face_locations, names):
            # Draw a box around the face
            cv2.rectangle(output, (left, top), (right, bottom), (0, 0, 255), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(
                output, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2
            )
        return flag, output
    else:
        return flag, None


def get_random_samples(all_samples, n_samples=10):
    import random

    random.seed(15)
    return random.sample(all_samples, n_samples)


# Perfroming test on images
def perform_recognition(
    index=0,
    img_path="",
    target_encodings=[],
    debug=False,
    verbose=False,
    found_directory="",
    not_found_directory="",
    perform_transfer=False,
):
    import time
    from shutil import copy

    # ---------------------------
    if verbose:
        start = time.time()
    image = cv2.imread(img_path)
    # If debugging mode is on, then draw the output, else not
    presence, output = check_presence(image, target_encodings, draw_output=debug)
    # show the output image

    if verbose:
        logging.info("{} , {}".format(index, presence))
        logging.info("Time taken : {}".format(time.time() - start))

    if debug:
        imS = cv2.resize(output, (800, 600))
        cv2.imshow("Image", imS)
        # cv2.waitKey(0)
        cv2.waitKey(1)
        cv2.destroyAllWindows()

    img_name = img_path.split(sep="\\")[-1]

    if perform_transfer:
        if presence:
            copy(img_path, found_directory + "/" + img_name)
        else:
            copy(img_path, not_found_directory + "/" + img_name)
    # ---------------------------


def sort_into_directories(
    images_to_test=[],
    found_directory="found_directory",
    not_found_directory="not_found_directory",
    perform_transfer=True,
    target_encodings=None,
    verbose=False,
    debug=False,
    n_samples=None,
    threading=False,
    n_workers=1,
):
    from concurrent.futures import ProcessPoolExecutor
    import time
    from tqdm import tqdm

    # from shutil import copy

    if not target_encodings:
        raise ValueError("Target encodings cannot be Null")

    if verbose:
        all_start = time.time()

    # ---------------------------
    if not threading:
        logging.info("Starting recognition without multiprocessing ".format(n_workers))
        for index, img_path in enumerate(tqdm(images_to_test)):
            perform_recognition(
                index=index,
                img_path=img_path,
                target_encodings=target_encodings,
                debug=debug,
                found_directory=found_directory,
                not_found_directory=not_found_directory,
                verbose=verbose,
                perform_transfer=perform_transfer,
            )
    else:
        logging.info("Total images: {}".fomrat(len(images_to_test)))
        logging.info("Starting recognition with {} processes ".format(n_workers))
        # with ThreadPoolExecutor(n_threads) as exe:
        with ProcessPoolExecutor(n_workers) as exe:
            for index, img_path in enumerate(images_to_test):
                exe.submit(
                    perform_recognition,
                    index=index,
                    img_path=img_path,
                    target_encodings=target_encodings,
                    debug=debug,
                    found_directory=found_directory,
                    not_found_directory=not_found_directory,
                    verbose=verbose,
                    perform_transfer=perform_transfer,
                )
                # logging.info(future.result())

    # ---------------------------

    if verbose:
        logging.info("Overall Time taken : {} seconds".format(time.time() - all_start))
