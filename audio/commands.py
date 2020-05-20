from audio import methods
from audio import wav
from audio import plot
from os import path
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
            if 'operation_method' not in args_dictionary:
                print('No operation method defined, using basic method!')
                args_dictionary['operation_method'] = 'basic'

            if 'output_file' not in args_dictionary:
                output_file = utils.replace_file_extension(args_dictionary['input_file'], 'wav')
                file_directory = path.dirname(output_file)
                file_name = path.basename(output_file)

                if file_directory != '':
                    final_name = file_directory + '/hidden_' + file_name
                else:
                    final_name = 'hidden_' + file_name

                args_dictionary['output_file'] = final_name

            # dictionary containing the indexes list
            dict_index = None

            # if the user input a key file then he wants to use a defined index lists
            if 'key_file' in args_dictionary:
                dict_index = utils.read_key_index(args_dictionary['key_file'])

            will_shuffle = True if args_dictionary['operation_method'] == 'shuffle' else False
            input_file = args_dictionary['input_file']
            output_file = args_dictionary['output_file']
            message_file = args_dictionary['message_file']

            methods.hide(input_file, output_file, message_file, will_shuffle, dict_index)

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
            data, rate = wav.read_wav_file(args_dictionary['input_file'])
            wav.show_information(data, rate)

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
                channel = int(args_dictionary['channel']) - 1

            # get channel data
            channel_data = wav.channel_bytes(data, channel)

            # represent the plot
            plot.show_plot(channel_data, rate)

    except KeyError:
        print('Bad arguments, use -help.')
