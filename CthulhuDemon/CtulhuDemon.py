""""
Модуль, осуществляющий связ с устройствами в фоне
"""

import mysql.connector
import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    Обработчик данных с устройств
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    mysql.connector.connect(host="localhost",
                            user="cthulhudemon",
                            passwd="1122",
                            database="cthulhudb",
                            use_pure=True)


    HOST, PORT = "", 9090

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()

