import numpy
import pyaudio
import time
import matplotlib.pyplot as plt

""" Globals for params """
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024


def get_all_devises():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    # for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range(0, numdevices):
        if p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

        if p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels') > 0:
            print("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    devinfo = p.get_device_info_by_index(2)
    print("Selected device is ", devinfo.get('name'))
    if p.is_format_supported(
            44100.0,  # Sample rate
            input_device=devinfo["index"],
            input_channels=devinfo['maxInputChannels'],
            input_format=pyaudio.paInt16):
        print("Yay")

    p.terminate()


def get_miks_stereo_device_index():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        device_name = p.get_device_info_by_host_api_device_index(0, i).get('name')

        if "Miks stere" in device_name:
            print(f"Miks stereo device id is: {i}")
            return i


def read_from_device(device_index):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=CHUNK
    )

    while True:
        # Get raw bytes
        bit = stream.read(CHUNK)

        # Decode
        decoded = numpy.fromstring(bit, 'Int16')

        print(decoded)
        time.sleep(1)
        plt.plot(decoded)
        plt.show()


if __name__ == "__main__":
    # get_all_devises()
    miks_stereo_index = get_miks_stereo_device_index()
    read_from_device(device_index=miks_stereo_index)
