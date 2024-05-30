import socket

PKT_HELLO = 0
PKT_CALC = 1
PKT_RESULT = 2
PKT_BYE = 3
PKT_FLAG = 4


def send_packet(sock, packet_type, data=b""):
    packet_type = packet_type.to_bytes(4, "little")
    packet_len = len(data).to_bytes(4, "little")
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


factorials = [1]
for i in range(1, 21):
    factorials.append(factorials[-1] * i)

def calculate_factorial_sum(low, high):  
    index1 = next(i for i, f in enumerate(factorials) if f >= low)
    
    index2 = next(i for i, f in reversed(list(enumerate(factorials))) if f <= high)
    
    total = sum(factorials[index1:index2+1])
    
    return total


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("112.137.129.129", 27010))
    print("Connected")

    student_id = "22021183"
    send_packet(client_socket, PKT_HELLO, student_id.encode("utf-8"))
    while True:
        type, data = receive_packet(client_socket)
        if type == PKT_BYE:
            break
        if type == PKT_CALC:
            low = int.from_bytes(data[0:4], "little")
            high = int.from_bytes(data[4:8], "little")
            print(low, "to", high)
            print(factorials)
            result = calculate_factorial_sum(low, high)
            print(result)
            result_bytes = result.to_bytes(8, "little")
            send_packet(client_socket, PKT_RESULT, result_bytes)
        elif type == PKT_FLAG:
            flag = data.decode("utf-8")
            print(flag, f"Flag received: {flag}")
            break

    client_socket.close()


if __name__ == "__main__":
    main()
