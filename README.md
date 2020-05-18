# Steganography

Project in development in python capable to hide any kind of file in a audio, image and video file. Providing multiple ways to hide the message.

For now only audio and image steganography is developed.

**Hide methods**

One of the methods developed to this project is called Shuffle method, it consists in shuffling the bits in a random
order, generating a file that will be necessary to retrieve the hidden message, making impossible to retrieve without it. The other is the simple method, it only saves the bytes in sequence order.

**Requirements:**
```
python -m pip install numpy matplotlib scipy more-itertools
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
Only lossless image format can be used (e.g. PNG), otherwise the hidden message can't be retrieved.

### How to execute

**Help:**
```
py main.py -help
```

**Hide file using shuffle mode**
```
py main.py image -i image.png -o image_with_message.png -m somezip.zip -encode shuffle
```

**Retrieve the hidden file from the audio file**
```
py main.py image -i image_with_message.png -k keys -decode
```
