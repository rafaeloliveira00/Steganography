from audio import commands
import utils
import sys

help_message = '''
The first argument must be the type of steganography that you want (audio/image/video) only audio is working wight now.

-- Global arguments (for the 3 types of steganography) --
-i specify the input file (the one that the message will be hidden)
-o specify the output file (where to save the file, may be optional)
-m location of the file to hide

-- Audio --
-encode simple|shuffle define that the message will be hidden using one of the given methods (if no method is defined, 
    the simple method will be used)
-decode specify that the message will be decoded
-info will show information about the audio file
-plot will show a spectrogram of the given file. To specify the channel to show in the plot use -c otherwise the first
    channel will be displayed
           '''

# get the arguments
args = sys.argv

# audio / image / video
try:
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
    args_dictionary['input_file'] = args[args.index('-i') + 1]

# get output file
if '-o' in args:
    args_dictionary['output_file'] = args[args.index('-o') + 1]
else:
    if 'input_file' in args_dictionary:
        output_file = utils.replace_file_extension(args_dictionary['input_file'], 'wav')
        args_dictionary['output_file'] = 'hidden_' + output_file

# get message file
if '-m' in args:
    args_dictionary['message_file'] = args[args.index('-m') + 1]

# get key file
if '-k' in args:
    args_dictionary['key_file'] = args[args.index('-k') + 1]

# get the channel (for plot)
if '-c' in args:
    args_dictionary['channel'] = args[args.index('-c') + 1]

if steganography_type != 'audio':
    print('First argument must be audio!')
    sys.exit()
elif 'operation' not in args_dictionary:
    print('Missing operation!')
    sys.exit()

# redirect the information to the right script
if steganography_type == 'audio':
    commands.main(args_dictionary)
elif steganography_type == 'image':
    pass
