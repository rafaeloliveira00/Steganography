from image_module import methods
from image_module import image
import cv2 as cv
import sys


def main(args_dictionary):
    """Method that will invoke the functions according to the user input

        Parameters:
          args_dictionary: Dictionary containing the user arguments

    """
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
            args_dictionary['output_file'] = 'hidden_' + args_dictionary['input_file']

        will_shuffle = True if args_dictionary['operation_method'] == 'shuffle' else False
        input_file = args_dictionary['input_file']
        output_file = args_dictionary['output_file']
        message_file = args_dictionary['message_file']

        methods.sequence_hide(input_file, output_file, message_file, will_shuffle)

    # decode option
    elif args_dictionary['operation'] == 'decode':
        # validate the arguments
        if 'key_file' not in args_dictionary:
            print('Missing key file destination!')
            sys.exit()

        input_file = args_dictionary['input_file']
        key_file = args_dictionary['key_file']

        methods.sequence_retrieve(input_file, key_file)

    # information option
    elif args_dictionary['operation'] == 'info':
        frame = cv.imread(args_dictionary['input_file'])
        image.show_information(frame)
