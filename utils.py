import random
import json
import sys
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


def generate_dictionary(num_lists):
    """Generate a dictionary of lists containing random values

        Parameters:
          num_lists: Number of lists that the dictionary will contain

        Returns:
          Populated dictionary

    """
    dictionary = {}
    for i in range(num_lists):
        dictionary[i] = random.sample(range(8), 8)

    return dictionary


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


def generate_key_file(file_name, message_length, indexes_dictionary=None):
    """Generates the file necessary to retrieve the message

        Parameters:
          file_name: Name of the file hidden
          indexes_dictionary: Dictionary with the list of indexes
          message_length: Length of the file hidden

    """
    dictionary = {
        "file_name": file_name,
        "length": message_length
    }

    # if the indexes_dictionary is None then the shuffle method was not applied
    if indexes_dictionary is not None:
        # invert the dictionary
        indexes_dictionary_inverted = invert_dictionary(indexes_dictionary)
        dictionary["method"] = "shuffle"
        dictionary["indexes_dictionary"] = indexes_dictionary_inverted
    else:
        dictionary["method"] = "simple"

    with open('keys', 'w') as fp:
        json.dump(dictionary, fp)


def read_key_file(location):
    """Read the file to retrieve the indexes list

           Parameters:
             location: Location of file

           Returns:
             Dictionary containing the information

       """

    try:
        with open(location) as json_file:
            data = json.load(json_file)

        # check if the method is shuffle
        if data['method'] == 'shuffle':
            # convert the indexes dictionary keys to int
            data['indexes_dictionary'] = {int(k): v for k, v in data['indexes_dictionary'].items()}
    except FileNotFoundError:
        print("The key file doesn't exist or no read permissions")
        sys.exit()
    except KeyError:
        print("Key file is invalid")
        sys.exit()

    return data
