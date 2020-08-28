# write your code here
import argparse
import socket


parser = argparse.ArgumentParser()
parser.add_argument("hostname", help="IP address")
parser.add_argument("port", help="port", type=int)
parser.add_argument("message", help="message for sending")
args = parser.parse_args()


def main():
    hostname = args.hostname
    port = args.port
    message = args.message
    with socket.socket() as client_socket:
        client_socket.connect((hostname, port))
        data = message.encode()
        client_socket.send(data)
        buffer_size = 1024
        response = client_socket.recv(buffer_size).decode()
        print(response)


if __name__ == "__main__":
    main()
