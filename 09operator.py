import socket
import struct
 
PKT_HELLO = 0
PKT_CALC = 1
PKT_RESULT = 2
PKT_BYE = 3
PKT_FLAG = 4

def send_packet(sock, packet_type, data=b''):
    
    packet_type = packet_type.to_bytes(4, 'little')
    pakcet_len = len(data).to_bytes(4, 'little')
    sock.sendall(packet_type + pakcet_len + data)


def receive_packet(sock):
    header = sock.recv(8)

    packet_type = int.from_bytes(header[0:4], "little")
    packet_len = int.from_bytes(header[4:8], "little")


    while packet_type == PKT_HELLO:  
        header = sock.recv(8)
        packet_type = int.from_bytes(header[0:4], "little")
        packet_len = int.from_bytes(header[4:8], "little")

    data = sock.recv(packet_len)

    print("Receive: ")
    print(packet_type, packet_len)
    return packet_type, data

def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('112.137.129.129', 27004))
    print("Connected")

   
    student_id = "22021183"
    send_packet(client_socket, PKT_HELLO, student_id.encode('utf-8'))

    while True:
        type, data = receive_packet(client_socket)
        if type == PKT_BYE:
            break
        if type == PKT_CALC:
            a = int.from_bytes(data[0:4], "little", signed=True)
            b = int.from_bytes(data[4:8], "little", signed=True)
            q = int.from_bytes(data[8:12], "big")

            print(a,b,q)
            if q == 1:
                res = a + b
            elif q == 2:
                res = a - b
            elif q == 3:
                res = a * b
            elif q == 4 and b != 0:
                res = round(a / b, 2)
            print(res)

            if b == 0:
                res_type = 3
                res_data = res_type.to_bytes(4, 'big') + b.to_bytes(4, 'big')
            else:
                if isinstance(res, int):
                    if res >= -2147483648 and res <= 2147483647:
                        res_type = 1
                        res_data = res_type.to_bytes(4, 'big') + res.to_bytes(4, 'big', signed=True)
                    elif res >= -9223372036854775808 and res <= 9223372036854775807:  
                        res_type = 2
                        res_data = res_type.to_bytes(4, 'big') + res.to_bytes(4, 'big', signed=True)
                elif isinstance(res, float):
                    res_type = 2
                    res_data = res_type.to_bytes(4, 'big') + struct.pack('>f', res)  

          
            send_packet(client_socket, PKT_RESULT, res_data)
            
        elif type == PKT_FLAG:
            flag = data.decode('utf-8')
            print(flag, f"Flag received: {flag}")
            break
    client_socket.close()

if __name__ == "__main__":
    main()
