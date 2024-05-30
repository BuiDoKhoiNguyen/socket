import socket

PKT_HELLO = 0
PKT_CALC = 1
PKT_RESULT = 2
PKT_BYE = 3
PKT_FLAG = 4

def send_packet(sock, packet_type, res):
    packet_len = len(res)
    
    packet_type = packet_type.to_bytes(4, 'little')
    packet_len = packet_len.to_bytes(4, 'little')
    
    sock.sendall(packet_type + packet_len + res)

def receive_packet(sock):
    header = sock.recv(8)
    packet_type = int.from_bytes(header[0:4], 'little')
    packet_len = int.from_bytes(header[4:8], 'little')

    # while packet_type == PKT_HELLO:  
    #     header = sock.recv(8)
    #     packet_type = int.from_bytes(header[0:4], "little")
    #     packet_len = int.from_bytes(header[4:8], "little")

    print(packet_type, packet_len)
    data = sock.recv(packet_len)
    return packet_type, data

def find_position(arr, x):
    for i, row in enumerate(arr):
        for j, val in enumerate(row):
            if val == x:
                return i, j
    return -1, -1

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('112.137.129.129', 27006))
    print("Connected")

    student_id = "22021183"
    send_packet(client_socket, PKT_HELLO, student_id.encode('utf-8'))

    while True:
        packet_type, data = receive_packet(client_socket)

        if packet_type == PKT_BYE:
            break
        elif packet_type == PKT_CALC:
            x = int.from_bytes(data[0:4], 'little', signed=True)
            N = int.from_bytes(data[4:8], 'little', signed=True)
            M = int.from_bytes(data[8:12], 'little', signed=True)
            
            print(x,N,M)
            posX = -1
            posY = -1
            for index in range(M*N):
                element = int.from_bytes(data[4 * (index + 3) : 4 * (index + 4)], 'little')
                # print(index, ' element: ', element)
                if element == x:
                    posX = index // M 
                    posY = index % M
                    break
            if posX != -1:
                posY += posX * M
                posX = 0
            print("posX: ",posX,"posY: ", posY)
            res = (posX).to_bytes(4, 'little', signed=True) + (posY).to_bytes(4, 'little', signed=True)
            send_packet(client_socket, PKT_RESULT, res)

        elif packet_type == PKT_FLAG:
            flag = data.decode('utf-8')
            print(flag, f"Flag received: {flag}")
            break

    client_socket.close()

if __name__ == "__main__":
    main()
