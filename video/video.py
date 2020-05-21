import cv2


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
