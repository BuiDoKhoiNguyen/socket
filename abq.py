import socket
import struct
 
PKT_HELLO = 0
PKT_CALC = 1
PKT_RESULT = 2
PKT_BYE = 3
PKT_FLAG = 4

def send_packet(sock, packet_type, data=b''):
    packet_type = packet_type.to_bytes(4, 'little')
    packet_len = len(data).to_bytes(4, 'little')
    
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

    print("Receive: ")
    print(packet_type, packet_len)
    return packet_type, data

def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('112.137.129.129', 27007))
    print("Connected")

   
    student_id = "22021183"
    send_packet(client_socket, PKT_HELLO, student_id.encode('utf-8'))

    while True:
        type, data = receive_packet(client_socket)
        if type == PKT_BYE:
            break
        if type == PKT_CALC:
            a = int.from_bytes(data[0:4], "little", signed=True)
            b = int.from_bytes(data[4:8], "little",signed=True)
            q = int.from_bytes(data[8:12], "big")

            print(a,b,q)
            if q == 1:
                res = a + b
            elif q == 2:
                res = a - b
            elif q == 3:
                res = a * b
            elif q == 4:
                res = a ** b
            
            
            # print(res)
            # if res > (2**32 - 1):
            #     res = res % (2**32)
            # elif res < -(2**31):
            #     res = res % -(2**32)
            print(res)
            res = res.to_bytes(4, 'little', signed=True)
            
            send_packet(client_socket, PKT_RESULT, res)
            
        elif type == PKT_FLAG:
            flag = data.decode('utf-8')
            print(flag, f"Flag received: {flag}")
            break
    client_socket.close()

if __name__ == "__main__":
    main()
