# write your code here
import argparse
import socket
import string
import itertools

ASCII_LOWERCASE = string.ascii_lowercase
DIGITS = string.digits
ALPHABET = ASCII_LOWERCASE + DIGITS

parser = argparse.ArgumentParser()
parser.add_argument("hostname", help="IP address")
parser.add_argument("port", help="port", type=int)
args = parser.parse_args()


def brute_force():
    attempt = 0
    for i in range(1, 1024):
        for comb in itertools.product(ALPHABET, repeat=i):
            password = ""
            for symbol in comb:
                password += symbol
            attempt += 1
            yield password, attempt


def brute_force_from_file():
    with open(r"passwords.txt",
              "r", encoding="utf8") as fout:
        for password in fout:
            password = password.strip()
            passwords = map(lambda x: ''.join(x),
                            itertools.product(*([letter.lower(), letter.upper()]
                                              for letter in password)))
            for password in passwords:
                yield password


def main():
    hostname = args.hostname
    port = args.port
    with socket.socket() as client_socket:
        client_socket.connect((hostname, port))
        buffer_size = 1024
        for password in brute_force_from_file():
            data = password.encode()
            client_socket.send(data)
            response = client_socket.recv(buffer_size).decode()
            if response == "Connection success!":
                response = password
                break
        print(response)


if __name__ == "__main__":
    main()
