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
    """Hides a byte of the message

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
