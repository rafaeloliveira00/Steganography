import scipy.io.wavfile as sci_wav
import numpy as np
import subprocess
import utils
import os


def bytes_count(data):
    """Return the number of bytes per channel

        Parameters:
          data: Data from the wav file

        Returns:
          Number of bytes per channel

    """
    return data.shape[0]


def channel_count(data):
    """Return the number of channels of the wav file

        Parameters:
          data: Data from the wav file

        Returns:
          Number of channels

    """
    # if the tuple have only one element then there is no columns on the data
    if len(data.shape) == 1:
        return 1

    return data.shape[1]


def bytes_to_hide_count(data):
    """Return the number of bytes that can be hidden

        Parameters:
          data: Data from the wav file

        Returns:
          Number of bytes that can be hidden

    """
    return (bytes_count(data) * channel_count(data)) / 8


def channel_bytes(data, channel):
    """Return an array containing the bytes of the given channel

        Parameters:
          data: Data from the wav file
          channel: Number of the channel

        Returns:
          Number of channels

    """
    assert channel_count(data) > channel, 'This data do not have the given channel'

    # check if there is only 1 channel
    if channel_count(data) == 1:
        return list(data)

    return [s[channel] for s in data]


def replace_data_channel(data, data_channel, channel):
    """Replace the data channel

        Parameters:
          data: Data from the wav file
          data_channel: The data channel
          channel: The number of the channel to replace the data

        Returns:
          Data of the wav file

    """
    assert channel_count(data) > channel, 'This data do not have the given channel'

    data_copy = data.copy()

    # check if there is only 1 channel
    if channel_count(data) == 1:
        return np.asarray(data_channel)

    data_copy[:, channel] = data_channel[:]

    return data_copy


def read_wav_file(location):
    """Open a wav file and return the data as an array

        Parameters:
          location: Location of the file

        Returns:
          A tuple, first element the data, the second the sample rate

    """
    data, rate = None, None

    try:
        rate, data = sci_wav.read(location)
    except FileNotFoundError:
        print('File not found')
    except PermissionError:
        print('Insufficient permissions to open the file')

    return data, rate


def write_wav_file(location, data, rate):
    """Create a new wav file and write the data

        Parameters:
          location: Location of the file
          data: Data of the file
          rate: Sample rate

        Returns:
          True if it succeeds otherwise False

    """
    assert data is not None, 'Data can not be None'
    assert rate and type(rate) is int, 'Invalid sample rate'

    try:
        # check if a directory was provided
        if os.path.dirname(location) is not '':
            # create directory if don't exist
            os.makedirs(os.path.dirname(location), exist_ok=True)
        # write to the file
        sci_wav.write(location, rate, data)
    except PermissionError:
        print('No permissions to write in the given directory')
        return False

    return True


def show_information(file_data, rate):
    """Prints in console some information about the file

        Parameters:
          file_data: Data of the file
          rate: rate of the audio file

    """
    print(f"Number of channels: {channel_count(file_data)}")
    print(f"Rate: {rate} Hz")
    print(f"Number of samples per channel: {bytes_count(file_data)}")
    print(f"Number of total bytes that can be hidden: {bytes_to_hide_count(file_data)}")


def convert_audio_file(input_file, output_file, delete=False):
    """Convert the format of an audio file to another, the output file will be overwritten

        Parameters:
          input_file: File to be converted
          output_file: Destination of the file
          delete: True to delete the original file after the conversion

        Returns:
          True if it succeeds otherwise False

    """
    assert utils.check_ffmpeg(), 'FFMPEG must be installed on the system'
    try:
        subprocess.call(['ffmpeg', '-i', input_file, '-y', output_file], stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        return False

    if delete:
        os.remove(input_file)

    return True
