import plot
from wav_module import wav
from wav_module import methods
import message
import utils

'''
Hide the message in sequence order
'''

ORIGINAL_SONG = 'original_song.wav'
ORIGINAL_MESSAGE_TO_HIDE = 'original_somezip.zip'

MODIFIED_SONG = 'modified_song.wav'
RETRIEVED_HIDDEN_MESSAGE = 'retrieved_original_somezip.zip'

### HIDE THE MESSAGE ###
data, rate = wav.read_wav_file(ORIGINAL_SONG)
wav.show_information(data)

length_message = methods.sequence_hide(ORIGINAL_SONG, MODIFIED_SONG, ORIGINAL_MESSAGE_TO_HIDE, True)

# generate a new dic ( for now its the same seed so it will generate the same dict as before)
dict = utils.generate_dictionary(10, 8)

# invert the dict
d = utils.invert_dictionary(dict)

### RETRIEVE THE MESSAGE ###
methods.sequence_retrieve(MODIFIED_SONG, length_message, RETRIEVED_HIDDEN_MESSAGE, d)
