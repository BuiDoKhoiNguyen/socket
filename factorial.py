import socket

 
PKT_HELLO = 0
PKT_CALC = 1
PKT_RESULT = 2
PKT_BYE = 3
PKT_FLAG = 4

def send_packet(sock, packet_type, data=b""):
    packet_type = packet_type.to_bytes(4, "little")
    packet_len = len(data).to_bytes(4, "little")
    print(packet_type + packet_len + data)
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

def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return "Nam nhuan"
    else:
        return "Nam khong nhuan"
    
def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('112.137.129.129', 27009))
    print("Connected")

   
    student_id = "22021183"
    send_packet(client_socket, PKT_HELLO, student_id.encode('utf-8'))

    while True:
        type, data = receive_packet(client_socket)
        if type == PKT_BYE:
            break
        if type == PKT_CALC:
            year = int.from_bytes(data, 'little')
            print(year)
            result = is_leap_year(year)
            send_packet(client_socket, PKT_RESULT, result.encode('utf-8'))
        elif type == PKT_FLAG:
            flag = data.decode('utf-8')
            print(flag, f"Flag received: {flag}")
            break
    client_socket.close()

if __name__ == "__main__":
    main()
