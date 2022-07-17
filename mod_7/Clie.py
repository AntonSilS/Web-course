import socket
import threading
import time
import sys



class Client:
    def __init__(self, ip="localhost", port=5001):
        self.ip = ip
        self.port = int(port)
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.state = True
        
    def recieve_msg(self):
        while self.state:
            msg = self.sock.recv(1024).decode()
            if not msg:
                break
            print(msg)

    def send_msg(self):
        while True:
            msg = input()
            if msg == "exit":
                msg = "Out chat!"
                self.sock.sendall(msg.encode())
                self.state = False
                break
            self.sock.sendall(msg.encode())

    def start_talk(self):
        try:
            self.sock.connect((self.ip, self.port))
            threading.Thread(target=self.send_msg, daemon=True).start()
            print('<<<Start chat (enter "exit" for quit)>>>')
            self.recieve_msg()
        except ConnectionRefusedError:
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("Out chat by KeyboardInterrupt!")
        except OSError:
            print("Such server doesn't run")
        finally:
            self.sock.close()


def main(argv=''):

    if argv:
        new_client = Client(argv[0], argv[1])
        print('YEs_1')

    else:
        new_client = Client()
        print('YEs_2')

    new_client.start_talk()


if __name__ == "__main__":
    try:
        if sys.argv[1:]:
            main(sys.argv[1:])
        else:
            main()
    except IndexError:
        print('Please enter: IP and PORT (example: 192.0.0.1 5000)!')

        

        
