from os import path
import subprocess
import utils
import cv2
import os


def frames_count(video):
    """Return the frames in the audio file

        Parameters:
          video: Video capture object

        Returns:
          Number of frames

    """
    return int(video.get(cv2.CAP_PROP_FRAME_COUNT))


def frames_per_second(video):
    """Return the frames rate

        Parameters:
          video: Video capture object

        Returns:
          Number of frames per second

    """

    return video.get(cv2.CAP_PROP_FPS)


def video_width(video):
    """Return the width of the video

        Parameters:
          video: Video capture object

        Returns:
          Width of the video

    """
    return int(video.get(cv2.CAP_PROP_FRAME_WIDTH))


def video_height(video):
    """Return the height of the video

        Parameters:
          video: Video capture object

        Returns:
          Height of the video

    """
    return int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))


def bytes_to_hide_count(video):
    """Return the number of bytes that can be hidden

        Parameters:
          video: Video capture object

        Returns:
          Number of bytes that can be hidden

    """

    # calculate space in one frame
    frame = (video_width(video) * video_height(video)) // 3
    # return the space that can hold a frame times the number of frames in the video
    return int(frame * frames_count(video))


def bytes_to_hide_frame_count(video):
    """Return the number of bytes that can be hidden in a single frame

        Parameters:
          video: Video capture object

        Returns:
          Number of bytes that can be hidden in a frame

    """
    return (video_width(video) * video_height(video)) // 3


def show_information(video):
    """Prints in console some information about the video

        Parameters:
          video: Video capture object

    """
    print(f'Resolution: {video_width(video)}x{video_height(video)}')
    print(f'Frames Per Second: {round(frames_per_second(video), 2)}')
    print(f'Total of frames: {frames_count(video)}')
    print(f'Total of bytes that can be hidden: {bytes_to_hide_count(video)}')
    print(f'Total of MegaBytes that can be hidden: {bytes_to_hide_count(video) // 1000000}')


def copy_audio(original_video, output_video):
    """Copies the audio from the original video file to the carrier

        Parameters:
          original_video: Original video file
          output_video: Carrier file

    """

    if utils.check_ffmpeg() is False:
        return

    # temporary audio stream file from the original video
    dir_path = os.path.dirname(original_video)
    if dir_path is not '':
        temp_file = dir_path + '/temp_audio_file.aac'
    else:
        temp_file = 'temp_audio_file.aac'

    try:
        # copy the audio file
        subprocess.call(['ffmpeg', '-i', original_video, '-y', '-vn', '-acodec', 'copy', temp_file],
                        stderr=subprocess.DEVNULL)

        # if the file do not exists then probably the original audio file do not have a audio stream
        if not path.exists(temp_file):
            return

        # rename the carrier file
        temp_carrier_name = os.path.basename(output_video)
        temp_carrier_name = '_temp_' + temp_carrier_name

        temp_carrier_name = utils.change_file_name(output_video, temp_carrier_name)

        # rename file name on the system (carrier file)
        try:
            os.rename(output_video, temp_carrier_name)
        except Exception:
            return

        print('Coping audio stream to the carrier')
        subprocess.call(
            ['ffmpeg', '-i', temp_carrier_name, '-y', '-i', temp_file, '-c:v', 'copy', '-map', '0:v:v', '-map',
             ' 1:a:0',
             output_video],
            stderr=subprocess.DEVNULL)

        # delete the temporary file
        os.remove(temp_file)
        os.remove(temp_carrier_name)

    except FileNotFoundError:
        pass
