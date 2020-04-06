"""
Client for audio_visualization.

This is to be run on the device that has the audio playback device
"""
import queue
import socket
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

        while True:
            try:
                # data = input()

                with lock:
                    data = data_queue.get()
                    print(f"Got data: {data}")

                if data is "":
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
