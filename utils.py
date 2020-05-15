import random
import os


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


def shuffle_elements(byte, indexes_dict, index_number):
    """Shuffle the elements of the list according to an list containing the indexes

        Parameters:
          byte: Bits of the byte in string form
          indexes_dict: Dictionary containing the indexes
          index_number: Number to get the list of the dict (last digit of the number)

        Returns:
          Byte shuffled

    """
    # get the last digit of the number
    index = index_number % 10

    # get the list corresponding to that index
    indexes_list = indexes_dict[index]

    result = []

    # shuffle the values
    for value in indexes_list:
        result.append(byte[value])

    # convert to string again
    result = ''.join(map(str, result))

    return result


def generate_dictionary(num_lists, num_elements_list):
    """Generate a dictionary of lists containing random values

        Parameters:
          num_lists: Number of lists that the dictionary will contain
          num_elements_list: Number of elements that each list will contain

        Returns:
          Populated dictionary

    """
    dictionary = {}
    for i in range(num_lists):
        dictionary[i] = random.sample(range(num_elements_list), num_elements_list)

    return dictionary


def get_file_extension(file_name):
    """Get the extension of the file

        Parameters:
          file_name: File name to extract the extension

        Returns:
          Extension of the file as string

    """
    return os.path.splitext(file_name)[1][1:]


def replace_file_extension(file_name, extension):
    """Replace the extension of a file name

        Parameters:
          file_name: File name to change the extension
          extension: extension to change to

        Returns:
          Extension of the file as string

    """
    prefix, _, _ = file_name.rpartition('.')
    return prefix + '.' + extension


def invert_dictionary(dictionary):
    """Invert the lists of the dictionary, it swap the index with the value

        Parameters:
          dictionary: Dictionary with the list of indexes

        Returns:
          Flipped dictionary

    """
    dictionary_copy = dictionary.copy()

    for i in dictionary_copy:
        list_copy = dictionary_copy[i].copy()
        for j in range(8):
            list_copy[j] = dictionary_copy[i].index(j)
        dictionary_copy[i] = list_copy

    return dictionary_copy
