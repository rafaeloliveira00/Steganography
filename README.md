# Steganography

Project in python capable to hide any kind of file in a audio, image and video file. Providing multiple ways to hide the message.


**Hide methods**

One of the methods developed to this project is called Shuffle method, it consists in shuffling the bits in a random
order, generating a file (keys file) that will be necessary to retrieve the hidden message, making impossible to retrieve without it. The other is the simple method, it only saves the bytes in sequence order.

**Requirements:**
```
python3 -m pip install opencv-python numpy matplotlib scipy more-itertools
```

## Audio

To work on audio files rather than wav, it is necessary to have FFMPEG installed on the system. The input file may be any audio format but the output must be a lossless file type (e.g. wav, flac)

### How to execute

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

## Image
Only lossless image format can be used (e.g. PNG, TIFF), otherwise the hidden message can't be retrieved.

### How to execute

**Hide file using shuffle mode**
```
py main.py image -i image.png -o image_with_message.png -m somezip.zip -encode shuffle
```

**Retrieve the hidden file from the audio file**
```
py main.py image -i image_with_message.png -k keys -decode
```

## Video
Any video file may be used as the input but, the ourput must be avi, a container that supports raw video.

**Hide file using shuffle mode**
```
py main.py video -i original_video.mp4 -o video_with_message.avi -m somezip.zip -encode shuffle
```

**Retrieve the hidden file from the audio file**
```
py main.py video -i video_with_message.avi -k keys -decode
```

## All commands commands

| Arguments       |Reference                         |
|----------------|-------------------------------|
|audio\image\video|specifies which technique will be used (must be the first argument) 
|-i|input file, location of the original file to hide the message           |
|-o         |output file, location of the resulting file, may be optional           |
|-m          |message file, location of the file that will be hidden|
|-k |key file, location of the file containing the information to retrieve the file, may also be used when encoding a message to supply a pre-defined index lists.|
|-encode|operation to hide the message using the basic|shuffle method, if no method is supplied the default will be basic|
|-decode|operation to retrieve the hidden message|
|-help| help message|
|-info|prints some information regarding the input file|
|-generatekeys|randomly generates indexes lists and saves them in a file|
|-plot|show a spectrogram of the given audio file as input|
|-c|specifies which channel should be represent in the spectrogram|
