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
    packet_len = packet_len.to_bytes(4, 'little')  # Fixed typo: to_bytes instead of to_bypes
    sock.sendall(packet_type + packet_len + data)


def receive_packet(sock):
    header = sock.recv(8)
    packet_type = int.from_bytes(header[0:4], 'little')
    packet_len = int.from_bytes(header[4:8], 'little')

    data = sock.recv(packet_len)

    print("Receive: ")
    print(packet_type, packet_len)
    return packet_type, data


def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def next_prime(n):
    if n <= 1:
        return 2
    prime = n + 1
    while True:
        if is_prime(prime):
            return prime
        prime += 1


def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('112.137.129.129', 27014))
    print("Connected")

   
    student_id = "22021183"
    send_packet(client_socket, PKT_HELLO, student_id.encode('utf-8'))

    while True:
        type, data = receive_packet(client_socket)
        if type == PKT_BYE:
            break
        if type == PKT_CALC:
            a = int.from_bytes(data[0:4], "little")

            print(a)

            res = next_prime(a)
            print(res)
            res = res.to_bytes(4, "little")
            send_packet(client_socket, PKT_RESULT, res)
        elif type == PKT_FLAG:
            flag = data.decode('utf-8')
            print(flag, f"Flag received: {flag}")
            break
    client_socket.close()

if __name__ == "__main__":
    main()
