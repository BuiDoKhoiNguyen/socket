import socket

 
PKT_HELLO = 0
PKT_CALC = 1
PKT_RESULT = 2
PKT_BYE = 3
PKT_FLAG = 4

def send_packet(sock, packet_type ,data=b''):
    packet_len = len(data).to_bytes(4, 'little')
    packet_type = packet_type.to_bytes(4, 'little')
   
    sock.sendall(packet_type + packet_len + data)


def receive_packet(sock):
    header = sock.recv(8)

    packet_type = int.from_bytes(header[0:4], "little")
    packet_len = int.from_bytes(header[4:8], "little")

    data = sock.recv(packet_len)

    print("Receive: ")
    print("packet type",packet_type,"packet len", packet_len)
    return packet_type, data

def find_element(arr, m):
    total_sum = sum(arr)
    left_sum = 0
    right_sum = total_sum - arr[0]
    for i in range(1, len(arr)):
        left_sum += arr[i-1]
        right_sum -= arr[i]
        if left_sum == right_sum:
            return i
    return -1

def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('112.137.129.129', 27016))
    print("Connected")

   
    student_id = "22021183"
    send_packet(client_socket, PKT_HELLO, student_id.encode('utf-8'))

    while True:
        type, data = receive_packet(client_socket)
        if type == PKT_BYE:
            break
        if type == PKT_CALC:
            m = int.from_bytes(data[0:4], "little")
            checksum = int.from_bytes(data[4:8], "little")
            array = [int.from_bytes(data[i:i+4], "little") for i in range(8, len(data), 4)]
            print( "m:", m,"checksum:" ,checksum)

            print("Array:", array)
            position = find_element(array, m)
            print("Position of the element:", position)
            
            calculated_checksum = 1
            for num in array:
                calculated_checksum *= num
                calculated_checksum %= m
            
            if calculated_checksum == checksum:
                t = 1
                data = t.to_bytes(4, 'little') + position.to_bytes(4, 'little')
                send_packet(client_socket, PKT_RESULT, data)
            else:
                t=0
                send_packet(client_socket, PKT_RESULT, t.to_bytes(4, 'little'))
        elif type == PKT_FLAG:
            flag = data.decode('utf-8')
            print(flag, f"Flag received: {flag}")
            break
    client_socket.close()

if __name__ == "__main__":
    main()
