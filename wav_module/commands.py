from wav_module import methods
from wav_module import wav
from wav_module import plot
import utils
import sys


def main(args_dictionary):
    """Method that will invoke the functions according to the user input

        Parameters:
          args_dictionary: Dictionary containing the user arguments

    """
    try:

        if 'input_file' not in args_dictionary:
            print('Missing input file destination!')
            sys.exit()

        # encode option
        if args_dictionary['operation'] == 'encode':

            # validate the arguments
            if 'message_file' not in args_dictionary:
                print('Missing message file destination!')
                sys.exit()

            # if no method specified then use the basic method
            elif 'operation_method' not in args_dictionary:
                print('No operation method defined, using basic method!')
                args_dictionary['operation_method'] = 'basic'

            will_shuffle = True if args_dictionary['operation_method'] == 'shuffle' else False
            input_file = args_dictionary['input_file']
            output_file = args_dictionary['output_file']
            message_file = args_dictionary['message_file']

            methods.hide(input_file, output_file, message_file, will_shuffle)

        # decode option
        elif args_dictionary['operation'] == 'decode':

            # validate the arguments
            if 'key_file' not in args_dictionary:
                print('Missing key file destination!')
                sys.exit()

            input_file = args_dictionary['input_file']
            key_file = args_dictionary['key_file']

            methods.retrieve(input_file, key_file)

        # information option
        elif args_dictionary['operation'] == 'info':
            data, _ = wav.read_wav_file(args_dictionary['input_file'])
            wav.show_information(data)

        # show spectrogram
        elif args_dictionary['operation'] == 'plot':

            input_file = args_dictionary['input_file']

            if utils.get_file_extension(input_file) != 'wav':
                print('The spectrogram can only be shown to wav files')
                return

            data, rate = wav.read_wav_file(input_file)

            channel = 0

            if 'channel' not in args_dictionary:
                print('Channel not specified. Will be used the channel 1 as default')
            else:
                channel = args_dictionary['channel'] + 1

            # get channel data
            channel_data = wav.channel_bytes(data, channel)

            # represent the plot
            plot.show_plot(channel_data, rate)

    except KeyError:
        print('Bad arguments, use -help.')
