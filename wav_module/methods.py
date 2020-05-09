import utils


def sequence_hide(channel_data, message_data):
    """Simple method to hide the message, it consists in hiding the message sequential along the bytes

        Parameters:
          channel_data: Data array of a channel
          message_data: Data array of the message

        Returns:
          Channel array data with the hidden message

    """
    assert utils.check_size(len(channel_data), len(message_data)), 'Not enough space to hide the message'

    return utils.hide_bytes(channel_data, message_data)


def sequence_retrieve(channel_data, number_bytes_hidden):
    """Retrieve the hidden message using the sequence method

           Parameters:
             channel_data: Data array of a channel containing the hidden message
             number_bytes_hidden: Number of bytes to retrieve

           Returns:
             Channel array data with the hidden message

       """
    assert utils.check_size(len(channel_data), number_bytes_hidden), 'This data can not have the amount of byte given'

    return utils.retrieve_bytes(channel_data, number_bytes_hidden)
