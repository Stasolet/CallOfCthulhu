import network
import gc
import socket
server = ("192.168.32.253", 9090)
def main(msg = "1;122"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server)
    s.write(msg)
    answ = s.read()
    s.close()
    print(answ)
    gc.collect()
    
# main()