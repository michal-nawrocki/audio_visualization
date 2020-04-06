"""
Client for audio_visualization.

This is to be run on the device that has the audio playback device
"""
import socket


HOST = "127.0.0.1"
PORT = 42069


def run_client():
    address_port = (HOST, PORT)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Started client. Connecting to {address_port}")
        s.connect(address_port)
        print("Connected")

        while True:
            try:
                data = input()

                if data is "":
                    break
                else:
                    # TODO: Provide the data from playback device
                    s.sendall(data.encode())

            except Exception as error:
                print(f"EXCEPTION: {error}")

    print("Connection closed")


if __name__ == "__main__":
    run_client()
