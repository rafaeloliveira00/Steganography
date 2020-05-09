import matplotlib.pyplot as plot


def show_plot(data, rate):
    """Shows a spectrogram of the given data channel

        Parameters:
          data: Array containing the data channel
          rate: frequency rate
    """
    plot.subplot(2, 1, 1)
    plot.title('Spectrogram')
    plot.plot(data)
    plot.xlabel('Sample')
    plot.ylabel('Amplitude')

    plot.subplot(2, 1, 2)
    plot.specgram(data, Fs=rate)
    plot.xlabel('Time')
    plot.ylabel('Frequency')

    plot.show()
