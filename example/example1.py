import plot
from wav_module import wav
from wav_module import methods
import message

ORIGINAL_SONG = 'original_song.wav'
ORIGINAL_MESSAGE_TO_HIDE = 'original_somezip.zip'

MODIFIED_SONG = 'modified_song.wav'
RETRIEVED_HIDDEN_MESSAGE = 'retrieved_somezip.zip'

### HIDE THE MESSAGE ###

# read the data of the original song
original_song, rate = wav.read_wav_file(ORIGINAL_SONG)

# read the message
message_to_hide = message.read_file(ORIGINAL_MESSAGE_TO_HIDE)

# get the length of the message
length_message = len(message_to_hide)

# get the first channel of the audio file
channel0 = wav.channel_bytes(original_song, 0)

# hide the message in the first channel
channel0_with_hidden_message = methods.sequence_hide(channel0, message_to_hide)

# show the spectogram of the original data channel
plot.show_plot(channel0, rate)

# show the spectogram of the channel with the original message
plot.show_plot(channel0_with_hidden_message, rate)

# replace the data channel in the song
modified_song = wav.replace_data_channel(original_song, channel0_with_hidden_message, 0)

# create audio file with the hidden message
wav.write_wav_file(MODIFIED_SONG, modified_song, rate)

### RETRIEVE THE MESSAGE ###
# read the audio file with the hidden message
modified_song, rate = wav.read_wav_file(MODIFIED_SONG)

# get the channel with the hidden message (first channel)
channel0 = wav.channel_bytes(modified_song, 0)

# retrieve the hidden message from the channel, to note that the 'length_message' is the length of the message hidden
# and this variable is previously created when the message is being hidden
hidden_message = methods.sequence_retrieve(channel0, length_message)

# create the file with the retrieve message
message.write_file(RETRIEVED_HIDDEN_MESSAGE, hidden_message)
