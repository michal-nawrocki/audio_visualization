"""
Client for audio_visualization.

This is to be run on the device that has the audio playback device
"""
import queue
import socket
import matplotlib.pyplot as plt
import numpy
import struct
from numpy import isnan
from datetime import datetime
from threading import (
    Thread,
    Lock
)

from main import (
    read_from_device,
)

HOST = "127.0.0.1"
PORT = 42069

lock = Lock()


def run_client(data_queue):
    address_port = (HOST, PORT)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Started client. Connecting to {address_port}")
        s.connect(address_port)
        print("Connected")

        file = open("test.txt", "w+")
        count = 0

        fig, ax = plt.subplots()
        x = numpy.arange(0, 2 * 1024, 2)
        line, = ax.plot(x, numpy.random.rand(1024))
        ax.set_ylim(0, 255)
        ax.set_xlim(0, 1024)
        while True:
            try:
                # data = input()

                with lock:
                    data = data_queue.get()
                    #print(f"Got data: {data}")

                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    file = open("test.txt", "a+")

                    data_int = numpy.array(struct.unpack(str(2 * 1024) + 'B', data), dtype='b')[::2] + 128
                    line.set_ydata(data_int)
                    fig.canvas.draw()
                    fig.canvas.flush_events()
                    print("_______")
                    print(len(data_int)) # array length
                    print(str(data_int))


                    '''
                    file.write(str(count))
                    file.write(" ")
                    file.write(current_time)
                    file.write(": \n")
                    file.write(str(data_int))
                    
                    decoded = numpy.fromstring(data, 'Float32')

                    
                    #replace NaN with 0
                    where_are_NaNs = isnan(decoded)
                    decoded[where_are_NaNs] = 0


                    #delete zeros
                    #decoded2 = numpy.delete(decoded, where_are_NaNs)
                    #print(len(decoded))

                    #print(len(decoded))

                    #write decoded bytes to file
                    file.write(str(decoded))
                    file.write("\n")

                    #plot decoded data
                    plt.plot(decoded)
                    plt.show()
                    '''

                    count +=1


                    #print(decoded)

                    #print("Current Time =", current_time)
                    #decoded = numpy.fromstring(data, numpy.int16)
                    #fig = plt.figure()
                    #s = fig.add_subplot(111)
                    #amplitude = numpy.fromstring(decoded, numpy.int16)
                    #s.specgram(amplitude)
                    #fig.savefig('t.png')

                if data == "":
                    break
                else:
                    # TODO: Provide the data from playback device
                    s.sendall(data)

            except Exception as error:
                print(f"EXCEPTION: {error}")

    print("Connection closed")


if __name__ == "__main__":
    data_queue = queue.Queue()

    thread_audio = Thread(target=read_from_device, args=(0, data_queue))
    thread_client = Thread(target=run_client, args=(data_queue,))

    with lock:
        thread_client.start()
        thread_audio.start()

    print("Started both threads")
