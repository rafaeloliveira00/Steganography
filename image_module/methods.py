from image_module import bytes_manipulation as bm
import cv2 as cv
import message
import utils
import os


def sequence_hide(image_file, result_file, message_file, shuffle=False):
    """Method to hide the message, it consists in hiding the message sequential along the pixels.

        Parameters:
          image_file: Location of the audio file
          result_file: Location to save the modified audio file
          message_file: Location of the file to hide
          shuffle: if true then the shuffle method will be used

    """

    # open the image file and retrieve the data
    frame = cv.imread(image_file)

    # open the file to hide and get the bytes
    message_bytes = message.read_file(message_file)

    assert bm.check_size(frame, len(message_bytes)) is True, 'The given data can not be hidden in the frame'

    index_dict = None
    if shuffle:
        # generate the dictionary of indexes
        index_dict = utils.generate_dictionary(10)

    modified_frame = bm.hide_in_frame(frame, message_bytes, index_dict)

    # write the result
    cv.imwrite(result_file, modified_frame)

    # get the file name
    message_file_name = os.path.basename(message_file)

    # generate the file to retrieve the message
    utils.generate_key_file(message_file_name, len(message_bytes), index_dict)

    print('Message hidden successful')


def sequence_retrieve(image_file, key_file):
    """Retrieve the hidden message using the sequence method

        Parameters:
          image_file: Location of the image file
          key_file: Location of the file containing the keys information

    """

    # open the image file
    frame = cv.imread(image_file)

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

    # retrieve the hidden data
    retrieved_data = bm.retrieve_in_frame(frame, bytes_length, dictionary)

    # create the file
    result = message.write_file(result_file, retrieved_data)

    if result:
        print('Message extracted successful')
    else:
        print('Error creating the final file')
