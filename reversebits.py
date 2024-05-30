import socket

 
PKT_HELLO = 0
PKT_CALC = 1
PKT_RESULT = 2
PKT_BYE = 3
PKT_FLAG = 4

def send_packet(sock, packet_type, data=b''):
    packet_len = len(data)
    packet_type = packet_type.to_bytes(4, 'little')
    packet_len = packet_len.to_bytes(4, 'little')  
    sock.sendall(packet_type + packet_len + data)


def receive_packet(sock):
    header = sock.recv(8)
    print(header)
    print("Receive: ")
    packet_type = int.from_bytes(header[0:4], "little")
    packet_len = int.from_bytes(header[4:8], "little")

    while packet_type == PKT_HELLO:  
        header = sock.recv(8)
        packet_type = int.from_bytes(header[4:8], "little")
        packet_len = int.from_bytes(header[0:4], "little")

    data = sock.recv(packet_len)

    print("packet type",packet_type,"packet len", packet_len, "data", data)
    return packet_type, data

def reverse_bits(a):
    return a ^ ((1 << 32) - 1)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('112.137.129.129', 27015))

    student_id = "22021183"
    send_packet(client_socket, PKT_HELLO, student_id.encode('utf-8'))

    while True:
        type, data = receive_packet(client_socket)
        type = data
        if type == PKT_BYE:
            break
        elif type == PKT_HELLO:
            continue
        elif type == PKT_CALC:
            a = int.from_bytes(data[0:4], "little")
            print(a)
            res = reverse_bits(a)
            res_bytes = res.to_bytes(8, 'little')  
            send_packet(client_socket, PKT_RESULT, res_bytes)
        elif type == PKT_FLAG:
            flag = data.decode('utf-8')
            print(flag, f"Flag received: {flag}")
            break
    client_socket.close()

if __name__ == "__main__":
    main()
