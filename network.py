import constant
import pickle
from socket import socket


def send_to_server_packet(socket : socket, packet, address : tuple):
    socket.sendto(pickle.dumps(packet), address)
    respond_server, address_server = socket.recvfrom(constant.PACKET_SIZE)
    return pickle.loads(respond_server)