from image_module import commands as image_commands
from audio import commands as audio_commands
from video import commands as video_commands
from os import path
import utils
import sys


def check_file(file, name):
    """Check if the file exists

        Parameters:
           file: file location
           name: type of the file

    """
    if not path.exists(file):
        print(f'{name} not found or no read permissions')
        sys.exit()


def generate_key_file():
    """Generates a file containing index lists randomly generated

    """
    utils.generate_file_only_index_lists('keys')
    print('File created successfully')
    sys.exit()


help_message = '''
The first argument must be the type of steganography that you want (audio/image/video) only audio is working wight now.

-- Global arguments (for the 3 types of steganography) --
-i specify the input file (the one that the message will be hidden)
-o specify the output file (where to save the file, may be optional)
-m location of the file to hide
-generatekeys creates a file containing a randomly generated index lists (must be the only argument)

-- Audio --
-encode simple|shuffle define that the message will be hidden using one of the given methods (if no method is defined, 
    the simple method will be used), -k argument may be used to specify a pre-defined index lists
-decode specify that the message will be decoded
-info will show information about the audio file
-plot will show a spectrogram of the given file. To specify the channel to show in the plot use -c otherwise the first
    channel will be displayed

-- Image --
-encode simple|shuffle define that the message will be hidden using one of the given methods (if no method is defined, 
    the simple method will be used), -k argument may be used to specify a pre-defined index lists
-decode specify that the message will be decoded
-info will show information about the image file

-- Video --
-encode simple|shuffle define that the message will be hidden using one of the given methods (if no method is defined, 
    the simple method will be used), -k argument may be used to specify a pre-defined index lists
-decode specify that the message will be decoded
-info will show information about the video file
           '''

# get the arguments
args = sys.argv

# audio / image / video
try:
    if args[1] == '-generatekeys':
        generate_key_file()
    steganography_type = args[1]
except IndexError:
    print(help_message)
    sys.exit()

# dictionary containing the user arguments
args_dictionary = {}

# if true then the user wants to hide the message otherwise it wants to retrieve a message
will_encode = None
method = None

# get operation
if '-help' in args:
    print(help_message)
    sys.exit()

elif '-encode' in args:
    try:
        args_dictionary['operation_method'] = args[args.index('-encode') + 1]
    except IndexError:
        pass
    args_dictionary['operation'] = 'encode'
elif '-decode' in args:
    args_dictionary['operation'] = 'decode'
elif '-plot' in args:
    args_dictionary['operation'] = 'plot'
elif '-info' in args:
    args_dictionary['operation'] = 'info'
elif '-help' in args:
    args_dictionary['operation'] = 'help'

# get input file
if '-i' in args:
    input_file = args[args.index('-i') + 1]
    check_file(input_file, 'Input file')
    args_dictionary['input_file'] = input_file

# get output file
if '-o' in args:
    args_dictionary['output_file'] = args[args.index('-o') + 1]

# get message file
if '-m' in args:
    message_file = args[args.index('-m') + 1]
    check_file(message_file, 'Message file')
    args_dictionary['message_file'] = message_file

# get key file
if '-k' in args:
    key_file = args[args.index('-k') + 1]
    check_file(key_file, 'Key file')
    args_dictionary['key_file'] = key_file

# get the channel (for plot)
if '-c' in args:
    args_dictionary['channel'] = args[args.index('-c') + 1]

if steganography_type != 'audio' and steganography_type != 'image' and steganography_type != 'video':
    print("First argument must be 'audio', 'image' or 'video'!")
    sys.exit()
elif 'operation' not in args_dictionary:
    print('Missing operation!')
    sys.exit()

# redirect the information to the right script
if steganography_type == 'audio':
    audio_commands.main(args_dictionary)
elif steganography_type == 'image':
    image_commands.main(args_dictionary)
elif steganography_type == 'video':
    video_commands.main(args_dictionary)
