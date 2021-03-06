import socket
import pickle
#INTERN
import constant
import packetcode
from serverpacket import ServerPacket
from vector import Vector
from clientpacket import ClientPacket
from rectangle import Rectangle

def clamp(value, min, max):
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value


def launch_server(server_address : tuple):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(server_address)

    clients = []

    while True:
        data, addr = server.recvfrom(constant.PACKET_SIZE)
        client_packet : ClientPacket = pickle.loads(data)
        
        if client_packet.code == packetcode.CONNECT:
            #print(f"Connect! {addr}")
            clients.append(addr)  
            server.sendto(pickle.dumps(ServerPacket(client_packet.id, True, None)), addr)
        elif client_packet.code == packetcode.DISCONNECT:
            #print(f"Disconnect! {addr}")
            clients.remove(addr)
            server.sendto(pickle.dumps(ServerPacket(client_packet.id, True, None)), addr)
        elif client_packet.code == packetcode.POSITION_CHANGED:
            rectangle : Rectangle = client_packet.data
            server_packet = ServerPacket(client_packet.id, True, Vector(rectangle.x, rectangle.y))
            x_correct = 0 <= rectangle.x and rectangle.x <= (constant.RESOLUTION_WIDTH - rectangle.width)
            y_correct = 0 <= rectangle.y and rectangle.y <= (constant.RESOLUTION_HEIGHT - rectangle.height)

            if x_correct and y_correct:
                #print(f"Position changed: {rectangle}, on {addr}")
                pass
            else:
                correct_x = rectangle.x
                correct_y = rectangle.y
                if not x_correct:
                    correct_x = clamp(rectangle.x, 0, constant.RESOLUTION_WIDTH - rectangle.width)
                if not y_correct:
                    correct_y = clamp(rectangle.y, 0, constant.RESOLUTION_HEIGHT - rectangle.height)

                server_packet.validation = False
                server_packet.correction = Vector(correct_x, correct_y)
                #print(f"Position cant be changed {rectangle}, on {addr}")
            server.sendto(pickle.dumps(server_packet), addr)
        else:
            #print("Did not find")
            break

    server.close()

if __name__ == "__main__":
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    launch_server((ip_address, constant.SERVER_PORT))