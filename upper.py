import socket

 
PKT_HELLO = 0
PKT_STRING = 1
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
    packet_type = int.from_bytes(header[0:4], "little")
    packet_len = int.from_bytes(header[4:8], "little")

    data = sock.recv(packet_len)

    print("Receive: ")
    print(packet_type, packet_len, data)
    return packet_type, data

def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('112.137.129.129', 27017))
    print("Connected")

   
    student_id = "22021183"
    send_packet(client_socket, PKT_HELLO, student_id.encode('utf-8'))
    print("done")
    while True:
        type, data = receive_packet(client_socket)
        if type == PKT_BYE:
            break
        if type == PKT_STRING:
            res = data.encode('utf-8')
            print(res)
            res = res.upper()

            res = res.decode('utf-8')
            send_packet(client_socket, PKT_RESULT, res)
        elif type == PKT_FLAG:
            flag = data.decode('utf-8')
            print(flag, f"Flag received: {flag}")
            break
    client_socket.close()

if __name__ == "__main__":
    main()
