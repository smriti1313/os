import socket


def send_file_to_server(filename):
	print("Attempting to connect to server...")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(("localhost", 9999))
		print("Connected to server.")

		with open(filename, 'r', encoding = 'utf-8', errors = 'replace') as file:
			print(f"Sending file: {filename}")
			for line in file:
				s.sendall(line.encode())
		print("File sent. Closing connection.")
		s.close()


send_file_to_server("Books to read/famousMenOfTheMiddleAges.txt")