import more_itertools
import numpy as np
import utils


def check_size(frame, n_bytes_message):
    """Check if the message can be hidden

        Parameters:
          frame: Image numpy data
          n_bytes_message: Number of the bytes in the message to hide

        Returns:
          True if the message can be hidden in the given frame, otherwise False

    """
    total_pixels = frame.shape[0] * frame.shape[1]

    t = total_pixels // 3
    return t >= n_bytes_message


def hide_byte(array, byte_to_hide, index_dict=None, index=None):
    """Hides a byte in an array, the array consists in 3 pixels, where each element are 3 bytes one for each color
    channel (RGB)

           Parameters:
             array: Array of elements (must be 3) representing 3 pixels, the element of each inner element are 3
                bytes represented in integers, one for each color channel
             byte_to_hide: The byte to hide as integer
             index_dict: Dictionary containing the lists to shuffle the bytes
             index: byte index of the message to hide

           Returns:
             Array with the hidden byte

       """

    # make a copy to prevent the change of the original array
    array_copy = array.copy()

    bits_to_hide = '{:08b}'.format(byte_to_hide)

    # if the dictionary is not none then shuffle the byte
    if index_dict is not None:
        bits_to_hide = utils.shuffle_elements(bits_to_hide, index_dict, index)

    for i, pixel in enumerate(array):

        # red channel
        array_copy[i][0] = utils.modify_bit(pixel[0], int(bits_to_hide[i * 3 + 0]))

        # green channel
        array_copy[i][1] = utils.modify_bit(pixel[1], int(bits_to_hide[i * 3 + 1]))

        # if is the blue channel of the 3th pixel, discard it
        if i * 3 + 2 != 8:
            array_copy[i][2] = utils.modify_bit(pixel[2], int(bits_to_hide[i * 3 + 2]))

    return array_copy


def retrieve_byte(array, index_dict=None, index=None):
    """Retrieve a hidden byte from an array

        Parameters:
          array: Array containing 3 pixels
          index_dict: Dictionary containing the lists to shuffle the bytes
          index: byte index of the message to hide

        Returns:
          The hidden byte as a integer

    """
    assert len(array) is 3, 'The length of the array must be 3'

    hidden_byte = ''
    for i, pixel in enumerate(array):
        # transform to a string of bits
        hidden_bit = '{:08b}'.format(pixel[0])
        # get the last bit
        hidden_bit = hidden_bit[-1]
        # add to the string
        hidden_byte += hidden_bit

        hidden_bit = '{:08b}'.format(pixel[1])
        hidden_bit = hidden_bit[-1]
        hidden_byte += hidden_bit

        # if the 3th pixel is behind analysed ignore the blue channel,
        if i != 2:
            hidden_bit = '{:08b}'.format(pixel[2])
            hidden_bit = hidden_bit[-1]
            hidden_byte += hidden_bit

    # if the dictionary is not none then shuffle the byte
    if index_dict is not None:
        hidden_byte = utils.shuffle_elements(hidden_byte, index_dict, index)

    # convert the string to a integer
    hidden_byte = int(hidden_byte, 2)

    return hidden_byte


def hide_bytes(array, bytes_to_hide, index_dict=None):
    """Hides a set of bytes in an array

        Parameters:
          array: Array of bytes (must be at least 8) as integers, of the image to hide the message
          bytes_to_hide: List of bytes to hide in the array
          index_dict: Dictionary containing the lists to shuffle the bytes

        Returns:
          Array with the hidden bytes

    """
    assert check_size(array,
                      len(bytes_to_hide)), 'The array provided do not have sufficient space to hide the message'

    bytes_to_hide_length = len(bytes_to_hide)

    array_copy = array.copy()
    array_output = []

    for i, [a, b, c] in enumerate(more_itertools.grouper(array_copy, 3)):
        sub_array = [a, b, c]

        # check if there're more bytes to hide
        if bytes_to_hide_length > i:
            byte = bytes_to_hide[i]

            # hide byte in the sub-array
            result = hide_byte(sub_array, byte, index_dict, i)

            # add the result to the output array
            array_output.extend(result)

        # if not continue to add the default values
        else:
            array_output.extend(sub_array)

    # remove the None values (may have in the end of the array)
    array_output = list(filter(None.__ne__, array_output))

    return array_output


def retrieve_bytes(array, number_bytes_hidden, index_dict=None):
    """Retrieve the bytes hidden in the array

        Parameters:
          array: Array of bytes with the hidden message
          number_bytes_hidden: Number of hidden bytes
          index_dict: Dictionary containing the lists to shuffle the bytes

        Returns:
          List containing the hidden bytes

    """
    assert check_size(array,
                      number_bytes_hidden), 'The array provided can not have the number of hidden bytes provided'

    array_output = []

    for i, [a, b, c] in enumerate(more_itertools.grouper(array, 3)):
        sub_array = [a, b, c]

        # check if the hidden bytes has been recovered
        if i >= number_bytes_hidden:
            break

        # retrieve the hidden byte in the sub-array
        byte = retrieve_byte(sub_array, index_dict, i)

        # add the byte to the list
        array_output.append(byte)

    return array_output


def hide_in_frame(frame, bytes_to_hide, index_dict=None):
    """Hide the given bytes in the frame

        Parameters:
          frame: Array of bytes with the hidden message
          bytes_to_hide: Number of hidden bytes
          index_dict:  Dictionary containing the lists to shuffle the bytes

        Returns:
          List containing the hidden bytes

    """
    # get the rows and columns of the image
    rows = frame.shape[0]
    cols = frame.shape[1]

    # calculate the size of the row vector
    row_vector = rows * cols

    # reshape to row vector (easier to perform the operations), and get the first row (only row)
    row_vector = frame.reshape(1, row_vector, 3)[0]

    # hide the bytes and get the result
    result = hide_bytes(row_vector, bytes_to_hide, index_dict)

    # transform to numpy array to reshape
    result = np.array(result)
    # reshape to the original shape
    result = result.reshape(rows, cols, 3)

    return result


def retrieve_in_frame(frame, bytes_length, index_dict=None):
    """Retrieve the hidden bytes in the frame

        Parameters:
          frame: Array of bytes with the hidden message
          bytes_length: Number of bytes to retrieve
          index_dict:  Dictionary containing the lists to shuffle the bytes

        Returns:
          List containing the hidden bytes

    """
    # get the rows and columns of the image
    rows = frame.shape[0]
    cols = frame.shape[1]

    # calculate the size of the row vector
    row_vector = rows * cols

    # reshape to row vector (easier to perform the operations), and get the first row (only row)
    row_vector = frame.reshape(1, row_vector, 3)[0]

    # retrieve the bytes of the image
    result = retrieve_bytes(row_vector, bytes_length, index_dict)

    return result
