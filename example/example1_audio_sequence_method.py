from wav_module import wav
from wav_module import methods
import utils
import os


def hide():
    original_song = 'original_song.mp3'
    original_message_to_hide = 'original_somezip.zip'

    modified_song = 'modified_song.flac'

    input_input_extension = utils.get_file_extension(original_song)
    # if the file extension is not wav then convert it to wav extension
    if input_input_extension != 'wav':
        new_file = utils.replace_file_extension(original_song, 'wav')
        wav.convert_audio_file(original_song, new_file)
        original_song = new_file

    # get the extension of the output file
    output_input_extension = utils.get_file_extension(modified_song)
    # if is flac file, convert to flac
    if output_input_extension == 'flac':
        # first save with wav extension and after the file was been save, convert the file to flac
        modified_song = utils.replace_file_extension(modified_song, 'wav')
    # if is wav file, do nothing
    elif output_input_extension == 'wav':
        pass
    # if not, then it was given an incorrect extension of a file
    else:
        assert 'The output file can only be .wav or .flac types'

    data, rate = wav.read_wav_file(original_song)
    wav.show_information(data)

    methods.sequence_hide(original_song, modified_song, original_message_to_hide, True)

    # if the user wanted an flac file, lets convert it
    if output_input_extension == 'flac':
        new_file = utils.replace_file_extension(modified_song, 'flac')
        wav.convert_audio_file(modified_song, new_file, True)

    # check if the original file was a wav file, if note remove it as is a temporary file
    if input_input_extension != 'wav':
        os.remove(original_song)


def retrieve():
    modified_song_retrieve = 'modified_song.flac'

    output_input_extension = utils.get_file_extension(modified_song_retrieve)
    # if is flac file, convert to flac
    if output_input_extension == 'flac':
        # first save with wav extension and after the file was been save, convert the file to flac
        new_file = utils.replace_file_extension(modified_song_retrieve, 'wav')
        wav.convert_audio_file(modified_song_retrieve, new_file)
        modified_song_retrieve = new_file
    # if is wav file, do nothing
    elif output_input_extension == 'wav':
        pass
    # if not, then it was given an incorrect extension of a file
    else:
        assert 'The output file can only be .wav or .flac types'

    methods.sequence_retrieve(modified_song_retrieve, 'keys')

    # if the input was a flac file, then delete the temporary file
    if output_input_extension == 'flac':
        os.remove(modified_song_retrieve)


hide()
# retrieve()
