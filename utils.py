from os import path
import subprocess
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
          file_name: Location of the file to hide
          indexes_dictionary: Dictionary with the list of indexes
          message_length: Length of the file hidden

    """

    # get the name of the file
    message_file_name = os.path.basename(file_name)

    # location to save the key file
    file_directory = path.dirname(file_name)

    if file_directory != '':
        final_name = file_directory + '/' + 'keys'
    else:
        final_name = 'keys'

    dictionary = {
        "file_name": message_file_name,
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

    with open(final_name, 'w') as fp:
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


def read_key_index(location):
    """Read the file and return only the inverted indexes list

           Parameters:
             location: Location of file

           Returns:
             Dictionary containing the index lists

       """
    try:
        with open(location) as json_file:
            data = json.load(json_file)

        dict_index_lists = data['indexes_dictionary']

        # convert the indexes dictionary keys to int
        dict_index_lists = {int(k): v for k, v in dict_index_lists.items()}

        # invert the dictionary to write
        dict_index_lists = invert_dictionary(dict_index_lists)

    except FileNotFoundError:
        print("The key file doesn't exist or no read permissions")
        sys.exit()
    except KeyError:
        print("Key file is invalid")
        sys.exit()

    return dict_index_lists


def generate_file_only_index_lists(location):
    """Creates a file with randomly generated indexes lists

           Parameters:
             location: Location of file

       """

    index_lists = generate_dictionary(10)

    dictionary = {
        "indexes_dictionary": index_lists
    }

    with open(location, 'w') as fp:
        json.dump(dictionary, fp)


def check_ffmpeg():
    """Check if FFMPEG is installed on the system

         Returns:
          True if is installed otherwise False

    """
    try:
        subprocess.call(['ffmpeg'], stderr=subprocess.DEVNULL)

    except FileNotFoundError:
        return False

    return True


def change_file_name(name, name_to_change):
    """Changes a string representing a file name, including directory locations. To note that his function only changes
    the string and not the actual file

           Parameters:
             name: File name
             name_to_change: Name to change to

           Returns:
             Changed file name

       """

    # get the file name from the given directory
    name_to_change = os.path.basename(name_to_change)

    # get the directory
    dir_path = os.path.dirname(name)

    result = name_to_change
    if dir_path is not '':
        result = dir_path + '/' + name_to_change

    return result
