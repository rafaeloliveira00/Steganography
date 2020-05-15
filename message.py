import numpy
import sys
import os


def read_file(location):
    """Open the file and return an array containing the bytes

        Parameters:
          location: Location of the file

        Returns:
          Array of bytes in integer type

    """
    array_bytes = None

    try:
        array_bytes = numpy.fromfile(location, dtype="uint8")
    except FileNotFoundError:
        print("The file doesn't exist or no read permissions")
        sys.exit()

    return array_bytes


def write_file(location, byte_array):
    """Create a file with the given byte array (integer values)

        Parameters:
          location: Location and name of the file
          byte_array: The data

        Returns:
          True if it succeeds otherwise False

    """
    try:
        # check if a directory was provided
        if os.path.dirname(location) is not '':
            # create directory if don't exist
            os.makedirs(os.path.dirname(location), exist_ok=True)
        # convert the data to binary array
        byte_array = bytearray(byte_array)
        # write to the file
        with open(location, 'wb') as f:
            f.write(byte_array)
    except PermissionError:
        print("The message file doesn't exist or no read permissions")
        sys.exit()

    return True
