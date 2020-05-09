import utils
from wav_module import wav
import message


def sequence_hide(audio_file, result_audio_file, message_file):
    """Simple method to hide the message, it consists in hiding the message sequential along the channels

        Parameters:
          audio_file: Location of the audio file
          result_audio_file: Location to save the modified audio file
          message_file: Location of the file to hide

        Returns:
          Number of bytes hidden

    """
    # open the audio file
    original_song, rate = wav.read_wav_file(audio_file)

    # open the file to hide
    message_bytes = message.read_file(message_file)

    # get number of channels
    channel_count = wav.channel_count(original_song)

    # get the number of bytes that can be hidden
    max_data = wav.bytes_to_hide_count(original_song)

    assert max_data > len(message_bytes), 'Not enough space to hide the message'

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
        modified_channel_bytes = utils.hide_bytes(channel_bytes, message_bytes_sub_array)

        # replace the data channel
        original_song = wav.replace_data_channel(original_song, modified_channel_bytes, i)

    # create the file
    wav.write_wav_file(result_audio_file, original_song, rate)

    print('File created successfully')

    # return the number of bytes hidden
    return len(message_bytes)


def sequence_retrieve(audio_file, bytes_length, result_file):
    """Retrieve the hidden message using the sequence method

        Parameters:
          audio_file: Location of the audio file
          bytes_length: Number of bytes hidden
          result_file: Location of the obtained file

        Returns:
          Number of bytes hidden

    """
    # open the audio file
    original_song, rate = wav.read_wav_file(audio_file)

    # get number of channels
    channel_count = wav.channel_count(original_song)

    # get the number of bytes that can be hidden
    max_data = wav.bytes_to_hide_count(original_song)

    assert max_data > bytes_length, 'This data can not have the amount of bytes given'

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

        extracted_bytes = utils.retrieve_bytes(channel_bytes, bytes_to_get)

        # add the extracted bytes to the final result
        extracted_bytes_array.extend(extracted_bytes)

    result = message.write_file(result_file, extracted_bytes_array)

    if result:
        print('Message extracted successful')
    else:
        print('Error creating the final file')
