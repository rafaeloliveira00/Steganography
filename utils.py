import more_itertools


def check_size(n_bytes_file, n_bytes_message):
    """Check if the message can be hidden

        Parameters:
          n_bytes_file: Number of bytes in the file
          n_bytes_message: Number of the bytes in the message to hide

        Returns:
          True if the message can be hidden in the given file, otherwise False

    """
    t = n_bytes_file / 8
    return t >= n_bytes_message


def modify_bit(number, bit):
    """Changes the last bit of a integer

        Parameters:
          number: The integer that will suffer the transformation
          bit: The bit has integer

        Returns:
          The modified integer.

    """
    assert bit is 0 or bit is 1, 'The bit must be 0 or 1'

    return (number & ~1) | ((bit << 0) & 1)


def hide_byte(array, byte_to_hide):
    """Hides a byte in an array

        Parameters:
          array: Array of bytes (must be 8) as integers, of the file to hide the message
          byte_to_hide: The byte to hide as integer

        Returns:
          Array with the hidden byte

    """
    assert len(array) is 8, 'The length of the array must be 8'
    assert 0 <= byte_to_hide <= 255, 'The byte to hide must be between 0 and 255 (inclusive)'

    # make a copy to prevent the change of the original array
    array_copy = array.copy()

    bits_to_hide = '{:08b}'.format(byte_to_hide)

    for i, byte in enumerate(array_copy):
        # modify the original byte and save it at the original location
        array_copy[i] = modify_bit(byte, int(bits_to_hide[i]))

    return array_copy


def retrieve_byte(array):
    """Retrieve a hidden byte from an array

        Parameters:
          array: Array of bytes (must be 8) as integers containing a hidden byte

        Returns:
          The hidden byte as a integer

    """
    assert len(array) is 8, 'The length of the array must be 8'

    hidden_byte = ''
    for i, byte in enumerate(array):
        # transform to a string of bits
        hidden_bit = '{:08b}'.format(byte)
        # get the last bit
        hidden_bit = hidden_bit[-1]
        # add to the string
        hidden_byte += hidden_bit

    # convert the string to a integer
    hidden_byte = int(hidden_byte, 2)

    return hidden_byte


def hide_bytes(array, bytes_to_hide):
    """Hides a set of bytes in an array

        Parameters:
          array: Array of bytes (must be at least 8) as integers, of the file to hide the message
          bytes_to_hide: List of bytes to hide in the array

        Returns:
          Array with the hidden bytes

    """
    assert check_size(len(array),
                      len(bytes_to_hide)), 'The array provided do not have sufficient space to hide the message'

    bytes_to_hide_length = len(bytes_to_hide)

    array_copy = array.copy()
    array_output = []

    for i, [a, b, c, d, e, f, g, h] in enumerate(more_itertools.grouper(array_copy, 8)):
        sub_array = [a, b, c, d, e, f, g, h]

        # check if there're more bytes to hide
        if bytes_to_hide_length > i:
            byte = bytes_to_hide[i]

            # hide byte in the sub-array
            result = hide_byte(sub_array, byte)

            # add the result to the output array
            array_output.extend(result)

        # if not continue to add the default values
        else:
            array_output.extend(sub_array)

    # remove the None values (may have in the end of the array)
    array_output = list(filter(None.__ne__, array_output))

    return array_output


def retrieve_bytes(array, number_bytes_hidden):
    """Retrieve the bytes hidden in the array

        Parameters:
          array: Array of bytes with the hidden message
          number_bytes_hidden: Number of hidden bytes

        Returns:
          List containing the hidden bytes

    """

    assert check_size(len(array),
                      number_bytes_hidden), 'The array provided can not have the number of hidden bytes provided'

    array_output = []

    for i, [a, b, c, d, e, f, g, h] in enumerate(more_itertools.grouper(array, 8)):
        sub_array = [a, b, c, d, e, f, g, h]

        # check if the hidden bytes has been recovered
        if i >= number_bytes_hidden:
            break

        # retrieve the hidden byte in the sub-array
        byte = retrieve_byte(sub_array)

        # add the byte to the list
        array_output.append(byte)

    return array_output
