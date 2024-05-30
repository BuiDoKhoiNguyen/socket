import socket
import struct

PKT_HELLO = 0
PKT_CALC = 1
PKT_RESULT = 2
PKT_BYE = 3
PKT_FLAG = 4

def send_packet(sock, packet_type, data=b''):
    packet_len = len(data)
    packet_type = packet_type.to_bytes(4, 'little')
    packet_len = packet_len.to_bytes(4, 'little')
    print(packet_type + packet_len + data)
    sock.sendall(packet_type + packet_len + data)

def receive_packet(sock):
    header = sock.recv(8)
    print(header)
    packet_type = int.from_bytes(header[0:4], "little")
    packet_len = int.from_bytes(header[4:8], "little")

    # while packet_type == PKT_HELLO:
    #     header = sock.recv(8)
    #     packet_type = int.from_bytes(header[0:4], "little")
    #     packet_len = int.from_bytes(header[4:8], "little")
    print(packet_type, packet_len)
    data = sock.recv(packet_len)
    return packet_type, data

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('112.137.129.129', 27011))
    print("Connected")

    student_id = "22021183"
    send_packet(client_socket, PKT_HELLO, student_id.encode('utf-8'))

    while True:
        type, data = receive_packet(client_socket)
        if type == PKT_BYE:
            break
        if type == PKT_CALC:
            n = int.from_bytes(data[0:4], "little")
            print(n)
            res = fibonacci(n)
            res = res.to_bytes(4, "little")
            send_packet(client_socket, PKT_RESULT, res)
        elif type == PKT_FLAG:
            flag = data.decode('utf-8')
            print(flag, f"Flag received: {flag}")
            break

    client_socket.close()

if __name__ == "__main__":
    main()
