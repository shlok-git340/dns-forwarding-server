import socket
import struct

def main():
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    test_bytes = b'\xbb\xaf\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x0ccodecrafters\x02io\x00\x00\x01\x00\x01'
    print("client sent: ",end=' ')
    print(test_bytes.hex())
    udp_socket.sendto(test_bytes,("127.0.0.1",2053))
    res,source = udp_socket.recvfrom(512)
    print("client received : ",end = ' ')
    print(res.hex())

if __name__ == "__main__":
    main()