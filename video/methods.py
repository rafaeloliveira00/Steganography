from image_module import bytes_manipulation as bm
from video import video
from os import path
import message
import utils
import sys
import cv2

# raw video (no codec)
VIDEO_CODEC = 'RGBA'


def hide(video_file_input, video_file_output, message_file, will_shuffle=False, dict_index=None):
    """Method responsible to manage the files, it will convert the audio formats if necessary before starting the
    coding of the data

        Parameters:
          video_file_input: Location of the video file
          video_file_output: Location to save the modified video file
          message_file: Location of the file to hide
          will_shuffle: if true then the shuffle method will be used
          dict_index: dictionary containing the index lists (optional)

    """

    # open video file
    video_file = cv2.VideoCapture(video_file_input)

    # retrieve some information about the video file
    fps = video.frames_per_second(video_file)
    width = video.video_width(video_file)
    height = video.video_height(video_file)

    # create object writer
    writer = cv2.VideoWriter(video_file_output, cv2.VideoWriter_fourcc(*VIDEO_CODEC), fps, (width, height), True)

    # open the file to hide and get the bytes
    message_bytes = message.read_file(message_file)

    # length of the bytes to hide
    message_bytes_length = len(message_bytes)

    # equals to dict_index, if the user did not input no dict_index then it is None and one will be generated
    index_dict = dict_index

    # check if it is necessary to generate dictionary of indexes
    if will_shuffle and index_dict is None:
        # generate the dictionary of indexes
        index_dict = utils.generate_dictionary(10)

    # counter of the frames
    frame_count = 0

    # number of bytes that a frame can hide
    frames_bytes_length = video.bytes_to_hide_frame_count(video_file)

    # number of bytes that can be hidden in the video
    video_bytes_to_hide = video.bytes_to_hide_count(video_file)

    # check if the message can be hidden
    if message_bytes_length > video_bytes_to_hide:
        print('Insufficient space to hide the message')
        sys.exit()

    print('Generating file...')
    # loop thought the video frame by frame
    while video_file.isOpened():
        ret, frame = video_file.read()

        # check if we have a frame
        if not ret:
            break

        # calculate the limit
        start = frames_bytes_length * frame_count
        stop = frames_bytes_length * frame_count + frames_bytes_length

        # check if there are more bytes to hide
        if start <= message_bytes_length:
            # get a sublist to byte the frames
            bytes_to_hide_sub_list = message_bytes[start:stop]
            # hide the message in the frame
            modified_frame = bm.hide_in_frame(frame, bytes_to_hide_sub_list, index_dict)
            # save the frame to the output file
            writer.write(modified_frame)
        else:
            # if not continue to save the default frames
            writer.write(frame)

        frame_count += 1

    # generate the file to retrieve the message
    utils.generate_key_file(message_file, len(message_bytes), index_dict)

    video_file.release()
    writer.release()

    # copy the audio stream from the original file to the carrier file
    video.copy_audio(video_file_input, video_file_output)

    print('File created successfully')


def retrieve(video_file_location, key_file):
    """Retrieve the hidden message using the sequence method

        Parameters:
          video_file_location: Location of the video file
          key_file: Location of the file containing the keys information

    """
    # open video file
    try:
        video_file = cv2.VideoCapture(video_file_location)
    except ImportError:
        print('Error opening the file')
        sys.exit()

    # retrieve from the file the data
    keys_data = utils.read_key_file(key_file)

    # number of bytes
    bytes_length = keys_data['length']

    # dictionary containing the indexes
    dictionary = None

    # check if method is shuffle
    if keys_data['method'] == 'shuffle':
        dictionary = keys_data['indexes_dictionary']

    # get the name of result file
    result_file = keys_data['file_name']

    # calculate the output file location
    file_directory = path.dirname(video_file_location)
    if file_directory != '':
        final_name = file_directory + '/' + result_file
    else:
        final_name = result_file

    # array with the bytes extracted
    extracted_bytes_array = []

    # number of bytes that a frame can hide
    frames_bytes_length = video.bytes_to_hide_frame_count(video_file)

    # bytes left to retrieve
    bytes_left = bytes_length

    # retrieve the data
    # loop thought the video frame by frame
    while video_file.isOpened():
        if bytes_left <= 0:
            break

        ret, frame = video_file.read()

        # If we have more bytes to retrieve and not more frames, then something is wrong
        if not ret:
            print('Invalid video file and/or keys file')
            sys.exit()

        if bytes_left >= frames_bytes_length:
            bytes_to_get = frames_bytes_length
            bytes_left -= bytes_to_get
        else:
            bytes_to_get = bytes_left
            bytes_left = 0

        # extract the bytes in the frame
        extracted_bytes = bm.retrieve_in_frame(frame, bytes_to_get, dictionary)

        # add the extracted bytes to the final result
        extracted_bytes_array.extend(extracted_bytes)

    video_file.release()

    # create the hidden file
    result = message.write_file(final_name, extracted_bytes_array)

    if result:
        print('Message extracted successful')
    else:
        print('Error creating the final file')
