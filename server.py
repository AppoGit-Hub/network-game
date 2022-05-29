import socket
import pygame
import pickle
#INTERN
import constant
import code
import extra
from serverpacket import ServerPacket
from vector import Vector
from clientpacket import ClientPacket

def clamp(value, min, max):
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(constant.SERVER_ADDRESS)

clients = []

while True:
    data, addr = server.recvfrom(constant.PACKET_SIZE)
    client_packet : ClientPacket = pickle.loads(data)
    
    match client_packet.code:
        case code.CONNECT:
            print(f"Connect! {addr}")
            clients.append(addr)  
            server.sendto(pickle.dumps(ServerPacket(client_packet.id, True, None)), addr)

        case code.DISCONNECT:
            print(f"Disconnect! {addr}")
            clients.remove(addr)
            server.sendto(pickle.dumps(ServerPacket(client_packet.id, True, None)), addr)

        case code.POSITION_CHANGED:
            rectangle : pygame.Rect = client_packet.data
            server_packet = ServerPacket(client_packet.id, True, Vector(rectangle.x, rectangle.y))
            x_correct = 0 <= rectangle.x and rectangle.x <= (constant.RESOLUTION_WIDTH - rectangle.width)
            y_correct = 0 <= rectangle.y and rectangle.y <= (constant.RESOLUTION_HEIGHT - rectangle.height)

            if x_correct and y_correct:
                print(f"Position changed: {rectangle}, on {addr}")
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
                print(f"Position cant be changed {rectangle}, on {addr}")
            server.sendto(pickle.dumps(server_packet), addr)

        case _:
            print("Did not find")
            break

server.close()