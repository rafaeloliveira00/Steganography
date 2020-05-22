from audio import bytes_manipulation as bm
from audio import wav
from os import path
import message
import utils
import sys
import os


def hide(audio_file_input, audio_file_output, message_file, will_shuffle=False, dict_index=None):
    """Method responsible to manage the files, it will convert the audio formats if necessary before starting the
    coding of the data

        Parameters:
          audio_file_input: Location of the audio file
          audio_file_output: Location to save the modified audio file
          message_file: Location of the file to hide
          will_shuffle: if true then the shuffle method will be used
          dict_index: dictionary containing the index lists

    """
    input_input_extension = utils.get_file_extension(audio_file_input)
    # if the file extension is not wav then convert it to wav extension
    if input_input_extension != 'wav':

        if utils.check_ffmpeg() is False:
            print('FFmpeg must be installed on the system to use a different format then wav')
            sys.exit()

        new_file = utils.replace_file_extension(audio_file_input, 'wav')
        wav.convert_audio_file(audio_file_input, new_file)
        audio_file_input = new_file

    # get the extension of the output file
    output_input_extension = utils.get_file_extension(audio_file_output)
    # if is flac file, convert to flac
    if output_input_extension == 'flac':
        if utils.check_ffmpeg() is False:
            print('FFmpeg must be installed on the system to use a different format then wav')
            sys.exit()
        # first save with wav extension and after the file was been save, convert the file to flac
        audio_file_output = utils.replace_file_extension(audio_file_output, 'wav')
    # if is wav file, do nothing
    elif output_input_extension == 'wav':
        pass
    # if not, then it was given an incorrect extension of a file
    else:
        print('The output file can only be .wav or .flac format')
        sys.exit()

    # begin the encoding
    sequence_hide(audio_file_input, audio_file_output, message_file, will_shuffle, dict_index)

    # if the user wanted an flac file, lets convert it
    if output_input_extension == 'flac':
        new_file = utils.replace_file_extension(audio_file_output, 'flac')
        wav.convert_audio_file(audio_file_output, new_file, True)

    # check if the original file was a wav file, if note remove it as is a temporary file
    if input_input_extension != 'wav':
        os.remove(audio_file_input)


def retrieve(audio_file_input, key_file):
    """Method responsible to manage the files, it will convert the audio formats if necessary before starting the
    decoding of the data

        Parameters:
          audio_file_input: Location of the audio file
          key_file: Location of the key file

    """
    # get the extension of the file, to check if conversion is necessary
    output_input_extension = utils.get_file_extension(audio_file_input)
    # if is flac file, convert to wav to perform the operations
    if output_input_extension == 'flac':
        # first save with wav extension and after the file was been save, convert the file to flac
        new_file = utils.replace_file_extension(audio_file_input, 'wav')
        wav.convert_audio_file(audio_file_input, new_file)
        audio_file_input = new_file
    # if is wav file, do nothing
    elif output_input_extension == 'wav':
        pass
    # if not, then it was given an incorrect extension of a file
    else:
        assert 'The output file can only be .wav or .flac types'

    sequence_retrieve(audio_file_input, key_file)

    # if the input was a flac file, then delete the temporary file
    if output_input_extension == 'flac':
        os.remove(audio_file_input)


def sequence_hide(audio_file, result_audio_file, message_file, shuffle=False, dict_index=None):
    """Method to hide the message, it consists in hiding the message sequential along the channels,
    if shuffle mode is activated then, every bit of every byte will be shuffled with a generated dictionary.
    After the message is hidden a file is created to retrieve the original message

        Parameters:
          audio_file: Location of the audio file
          result_audio_file: Location to save the modified audio file
          message_file: Location of the file to hide
          shuffle: if true then the shuffle method will be used
          dict_index: dictionary containing the index lists

    """
    # open the audio file
    original_song, rate = wav.read_wav_file(audio_file)

    # open the file to hide
    message_bytes = message.read_file(message_file)

    # get number of channels
    channel_count = wav.channel_count(original_song)

    # get the number of bytes that can be hidden
    max_data = wav.bytes_to_hide_count(original_song)

    if max_data < len(message_bytes):
        print('Not enough space to hide the message')
        sys.exit()

    # equals to dict_index, if the user did not input no dict_index then it is None and one will be generated
    index_dict = dict_index

    # check if it is necessary to generate dictionary of indexes
    if shuffle and index_dict is None:
        # generate the dictionary of indexes
        index_dict = utils.generate_dictionary(10)

    # loop every channel
    for i in range(channel_count):
        # get the bytes of the channel
        channel_bytes = wav.channel_bytes(original_song, i)

        # if there isn't more bytes to hide, break the loop
        if (len(channel_bytes) // 8) * i > len(message_bytes):
            break

        # calculate the start and stop position
        start = (len(channel_bytes) * i) // 8
        stop = (len(channel_bytes) * i + len(channel_bytes)) // 8

        # get the sub-array of the message to hide
        message_bytes_sub_array = message_bytes[start:stop]

        # hide the bytes in the channel
        modified_channel_bytes = bm.hide_bytes(channel_bytes, message_bytes_sub_array, index_dict)

        # replace the data channel
        original_song = wav.replace_data_channel(original_song, modified_channel_bytes, i)

    # create the file
    wav.write_wav_file(result_audio_file, original_song, rate)

    # generate the file to retrieve the message
    utils.generate_key_file(message_file, len(message_bytes), index_dict)

    print('File created successfully')


def sequence_retrieve(audio_file, key_file):
    """Retrieve the hidden message using the sequence method

        Parameters:
          audio_file: Location of the audio file
          key_file: Location of the file containing the keys

    """
    # open the audio file
    original_song, rate = wav.read_wav_file(audio_file)

    assert original_song is not None, 'Error opening the input file!'

    # get number of channels
    channel_count = wav.channel_count(original_song)

    # get the number of bytes that can be hidden
    max_data = wav.bytes_to_hide_count(original_song)

    # read the keys file
    dictionary = None

    # retrieve from the file the data
    keys_data = utils.read_key_file(key_file)

    bytes_length = keys_data['length']

    assert max_data > bytes_length, 'This data can not have the amount of bytes given'

    # check if method is shuffle
    if keys_data['method'] == 'shuffle':
        dictionary = keys_data['indexes_dictionary']

    result_file = keys_data['file_name']

    # array with the bytes extracted
    extracted_bytes_array = []

    bytes_left = bytes_length

    # loop every channel
    for i in range(channel_count):
        # check if there is more bytes to extract
        if bytes_left <= 0:
            break
        # get the bytes of the channel
        channel_bytes = wav.channel_bytes(original_song, i)

        # calculate the number of bytes to get
        if bytes_left >= len(channel_bytes) // 8:
            bytes_left -= len(channel_bytes) // 8
            bytes_to_get = len(channel_bytes) // 8
        else:
            bytes_to_get = bytes_left
            bytes_left = 0

        extracted_bytes = bm.retrieve_bytes(channel_bytes, bytes_to_get, dictionary)

        # add the extracted bytes to the final result
        extracted_bytes_array.extend(extracted_bytes)

    # calculate the output file location
    file_directory = path.dirname(audio_file)
    if file_directory != '':
        final_name = file_directory + '/' + result_file
    else:
        final_name = result_file

    result = message.write_file(final_name, extracted_bytes_array)

    if result:
        print('Message extracted successful')
    else:
        print('Error creating the final file')
