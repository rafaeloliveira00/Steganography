import os
import scipy.io.wavfile as sci_wav


def bytes_count(data):
    """Return the number of bytes

        Parameters:
          data: Data from the wav file

        Returns:
          Number of bytes

    """
    return data.shape[0]


def channel_count(data):
    """Return the number of channels of the wav file

        Parameters:
          data: Data from the wav file

        Returns:
          Number of channels

    """
    return data.shape[1]


def channel_bytes(data, channel):
    """Return an array containing the bytes of the given channel

        Parameters:
          data: Data from the wav file
          channel: Number of the channel

        Returns:
          Number of channels

    """
    assert channel_count(data) > channel, 'This data do not have the given channel'
    return [s[channel] for s in data]


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
