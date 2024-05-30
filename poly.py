import socket

 
PKT_HELLO = 0
PKT_CALC = 1
PKT_RESULT = 2
PKT_BYE = 3
PKT_FLAG = 4

def send_packet(sock, packet_type, data=b''):
    packet_len = len(data)
    print("packet_len",packet_len)
    packet_type = packet_type.to_bytes(4, 'little')
    packet_len = packet_len.to_bytes(4, 'little')
    print(packet_len)  
    sock.sendall(packet_type + packet_len + data)


def receive_packet(sock):
    header = sock.recv(8)

    packet_type = int.from_bytes(header[0:4], "little")
    packet_len = int.from_bytes(header[4:8], "little")

    while packet_type == PKT_HELLO:  
        header = sock.recv(8)
        packet_type = int.from_bytes(header[0:4], "little")
        packet_len = int.from_bytes(header[4:8], "little")

    data = sock.recv(packet_len)

    return packet_type, data

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('112.137.129.129', 27002))

    student_id = "22021183"
    send_packet(client_socket, PKT_HELLO, student_id.encode('utf-8'))

    while True:
        type, data = receive_packet(client_socket)
        
        if type == PKT_BYE:
            break
        elif type == PKT_HELLO:
            continue
        elif type == PKT_CALC:
            N = int.from_bytes(data[0:4], "little")
            M = int.from_bytes(data[4:8], "little")
            x = int.from_bytes(data[8:12], "little")
            print(N, M, x)
    
            t = [int.from_bytes(data[i:i+4], "little") for i in range(12, len(data), 4)]

            res = sum(t[i] * (x ** i) for i in range(N + 1)) % M
            res = res.to_bytes(4, "little")
            send_packet(client_socket, PKT_RESULT, res)
        elif type == PKT_FLAG:
            flag = data.decode('utf-8')
            print(flag, f"Flag received: {flag}")
            break
    client_socket.close()

if __name__ == "__main__":
    main()
