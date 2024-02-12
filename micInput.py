#!/usr/bin/env python
import numpy as np
import aubio

sample_rate = 44100  # Set your desired sample rate
x = np.zeros(44100)  # Create an array to hold audio samples (e.g., a sine wave)

for i in range(44100):
    x[i] = np.sin(2. * np.pi * i * 225. / sample_rate)  # Generate a sine wave

# Create a pitch object (using the 'yin' algorithm)
p = aubio.pitch("yin", samplerate=sample_rate)

# Pad the input vector with zeros to match hop size
pad_length = p.hop_size - x.shape[0] % p.hop_size
x_padded = np.pad(x, (0, pad_length), 'constant', constant_values=0)
x_padded = x_padded.reshape(-1, p.hop_size)  # Reshape it into blocks of hop_size
x_padded = x_padded.astype(aubio.float_type)  # Convert to aubio.float_type

# Process each frame and print the time and pitch
for frame, i in zip(x_padded, range(len(x_padded))):
    time_str = "%.3f" % (i * p.hop_size / float(sample_rate))
    pitch_candidate = p(frame)
    print(time_str, "%.3f" % pitch_candidate)



"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
'''
import argparse
import queue
import sys

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=10, metavar='N',
    help='display every Nth sample (default: %(default)s)')
args = parser.parse_args(remaining)
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1
q = queue.Queue()


def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::args.downsample, mapping])


def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines


try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']

    length = int(args.window * args.samplerate / (1000 * args.downsample))
    plotdata = np.zeros((length, len(args.channels)))

    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    if len(args.channels) > 1:
        ax.legend([f'channel {c}' for c in args.channels],
                  loc='lower left', ncol=len(args.channels))
    ax.axis((0, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)

    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)
    with stream:
        plt.show()
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))


import pyaudio
import numpy as np

# Choose your microphone and set the chunk size and rate
mic = 1
chunk_size = 1024
rate = 44100

# Create a PyAudio instance
p = pyaudio.PyAudio()

# Open the stream
stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=chunk_size, input_device_index=mic)

# Read the data from the stream
data = stream.read(chunk_size)

# Convert the data to an array
data = np.fromstring(data, dtype=np.int16)

# Perform a Fourier transform on the data
freqs = np.fft.fftfreq(len(data))

print("freqs ", freqs)

# Close the stream
stream.stop_stream()
stream.close()
p.terminate()
'''