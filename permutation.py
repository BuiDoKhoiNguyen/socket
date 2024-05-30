import socket
import itertools

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
    packet_type = int.from_bytes(header[0:4], "little")
    packet_len = int.from_bytes(header[4:8], "little")
    while packet_type == PKT_HELLO:  
        header = sock.recv(8)
        packet_type = int.from_bytes(header[0:4], "little")
        packet_len = int.from_bytes(header[4:8], "little")
    data = sock.recv(packet_len)
    print("Received packet type:", packet_type, "packet len:", packet_len, data)
    return packet_type, data

def calculate_permutations(a):
    permutations = list(itertools.permutations(a))
    return len(permutations)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('112.137.129.129', 27012))

    student_id = "22021183"
    send_packet(client_socket, PKT_HELLO, student_id.encode('utf-8'))

    while True:
        packet_type, data = receive_packet(client_socket)
        
        if packet_type == PKT_BYE:
            break
        elif packet_type == PKT_HELLO:
            continue
        elif packet_type == PKT_CALC:
            m = int.from_bytes(data[0:4], "little")
            array = [int.from_bytes(data[i:i+4], "little") for i in range(4, len(data), 4)]
            
            print("Array:", array)
            permutations_count = calculate_permutations(array)
            print("Number of permutations:", permutations_count)
            
            res = permutations_count.to_bytes(4, "little")
            send_packet(client_socket, PKT_RESULT, res)
        elif packet_type == PKT_FLAG:
            flag = data.decode('utf-8')
            print(flag, f"Flag received: {flag}")
            break

    client_socket.close()

if __name__ == "__main__":
    main()
