import copy
import socket
import sys
import constant
import pickle
import pygame
import network
import _thread
import server
import select
import packetcode
from serverpacket import ServerPacket
from vector import Vector
from clientpacket import ClientPacket
from rectangle import Rectangle

class Client:
    def __init__(self, socket : socket, server_address : tuple):
        self.packet_id = 0
        self.socket = socket
        self.server_address = server_address
        self.display = pygame.display.set_mode(constant.RESOLUTION)
        self.clock = pygame.time.Clock()
        self.speed = 5

        try:
            server_respond = self.send_packet(packetcode.CONNECT, None)
        except ConnectionError:
            print("Connection Error Occured")
            self.close_client()

        self.next_position = Vector(0, 0)
        self.last_position = self.next_position

    def send_packet(self, packet_code, packet_data):
        packet = ClientPacket(self.packet_id, packet_code, packet_data)
        self.socket.sendto(pickle.dumps(packet), self.server_address)
        respond_server, address_server = self.socket.recvfrom(constant.PACKET_SIZE)
        self.packet_id += 1
        return pickle.loads(respond_server)
    
    def close_connection(self):
        self.send_packet(packetcode.DISCONNECT, None)
        self.socket.close()
        self.close_client()
    
    def close_client(self):
        pygame.quit()
        sys.exit()

    def main_loop(self):
        play = True
        while play:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
            
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_UP]:
                self.next_position.y += -1 * self.speed
            if key_pressed[pygame.K_DOWN]:
                self.next_position.y += 1 * self.speed
            if key_pressed[pygame.K_LEFT]:
                self.next_position.x += -1 * self.speed
            if key_pressed[pygame.K_RIGHT]:
                self.next_position.x += 1 * self.speed
            
            rectangle_width = 50
            rectangle_height = 50

            rectangle : Rectangle = Rectangle(self.next_position.x, self.next_position.y, rectangle_width, rectangle_height)
            
            if self.next_position != self.last_position:
                server_respond : ServerPacket = self.send_packet(packetcode.POSITION_CHANGED, rectangle)
                if server_respond.validation and server_respond.packet_id + 1 == self.packet_id:
                    #print(f"Position {self.next_position}")
                    pass
                else:
                    #print(f"Position correct {server_respond.correction}")
                    correct_position : Vector = server_respond.correction
                    self.next_position = correct_position
                    rectangle.x = correct_position.x
                    rectangle.y = correct_position.y

            pygame.draw.rect(self.display, pygame.Color("red"), pygame.Rect(rectangle.x, rectangle.y, rectangle.width, rectangle.height))

            self.last_position = copy.copy(self.next_position)

            pygame.display.flip()
            self.display.fill((0, 0, 0))
        self.close_connection()

def launch_local_server():
    local_server = server.launch_server(constant.DEFAULT_SERVER_ADDRESS)

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5)
    client_connect_packet = ClientPacket(0, packetcode.CONNECT, None)
    client_server_adress = constant.SERVER_ADDRESS
    
    print("Finding server")
    try:
        print("Connection to server...")
        server_respond  = network.send_to_server_packet(client_socket, client_connect_packet, client_server_adress)
    except:
        print("Connection error. Launching local server")
        _thread.start_new_thread(launch_local_server, ())
        client_server_adress = constant.DEFAULT_SERVER_ADDRESS

    print("Lauching client")
    client = Client(client_socket, client_server_adress)
    client.main_loop()