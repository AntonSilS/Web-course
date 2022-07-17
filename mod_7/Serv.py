import socket
import threading
import time



class ServerChat:
    def __init__(self, port=5001, ip=""):
        self.port = port
        self.ip = ip
        self.sock = socket.socket()
        self.clients_dict = {self.sock: self.port}

    def start_server(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))
        self.sock.listen()
        print("<<<Server's been run>>>")

    def recieve_msg(self, conn, addr):
        msg = conn.recv(1024).decode()
        msg_with_name = f"Client({addr[1]}): {msg}"
        return msg_with_name, msg

    def trannsmiter(self, msg_with_name, addr, msg=''):
        for client, address in self.clients_dict.items():
            if addr[1] == address:
                if msg == 'have been joined to chat':
                    client.sendto(f"You {msg}".encode(), addr)
                else:
                    client.sendto(f"You: {msg}".encode(), addr)
            else:
                client.sendall(msg_with_name.encode())

    def handler(self, conn, addr):
        try:
            while True:
                from_client_msg_name, msg = self.recieve_msg(conn, addr)
                if from_client_msg_name == f"Client({addr[1]}): Out chat!":
                    break
                print(from_client_msg_name)
                self.trannsmiter(from_client_msg_name, addr, msg)
        except:
            pass
        finally:
            self.clients_dict.pop(conn)
            msg_with_name = f"Client:({addr[1]}) has been diconnected"
            print(msg_with_name)
            self.trannsmiter(msg_with_name, addr)
            conn.close()

    def loop_thread_conn(self):
        try:
            while True:
                conn, addr = self.sock.accept()
                self.clients_dict[conn] = addr[1]
                if self.sock in self.clients_dict:
                    self.clients_dict.pop(self.sock)
                connect_msg_with_name = f"Client({addr[1]}) has been joined"
                connect_msg = 'have been joined to chat'
                print(connect_msg_with_name)
                self.trannsmiter(connect_msg_with_name, addr, connect_msg)
                threading.Thread(target=self.handler, args=(conn, addr), daemon=True).start()
        except ConnectionAbortedError:
            print("Server has been closed!")

    def run_and_check(self):
        try:
            threading.Thread(target=self.loop_thread_conn, daemon=True).start()
            while True:
                if not self.clients_dict:
                    time.sleep(1)
                    data = input(f"Chat is empty. Do you want to shut down the server(y/n)?\n")
                    if data == "y":
                        self.sock.close()
                        break
                    time.sleep(5)
        except KeyboardInterrupt:
            print("Shut down server by KeyboardInterrupt!")

def main():
    new_serv = ServerChat()

    new_serv.start_server()

    new_serv.run_and_check()

if __name__ == "__main__":
    main()