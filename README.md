# Steganography

Project in development in python capable to hide any kind of file in a audio, image and video file. Providing multiple ways to hide the message.

For now only audio steganography is developed.

##Hide methods
One of the methods developed to this project is called Shuffle method, it consists in shuffling the bits in a random
order, generating a file that will be necessary to retrieve the hidden message, making impossible to retrieve without it
as the number of possible combinations is 146 313 216 000. The other is the simple method, it only saves the bytes in sequence order.

**Requirements:**
```
python -m pip install numpy matplotlib scipy more-itertools
```

To work on audio files rather than wav, it is necessary to have FFMPEG installed on the system.

###How to execute

**Help:**
```
py main.py -help
```

**Hide file using shuffle mode**
```
py main.py audio -i original_song.mp3 -o song_with_message.flac -m somezip.zip -encode shuffle
```

**Retrieve the hidden file from the audio file**
```
py main.py audio -i song_with_message.flac -k keys -decode
```
