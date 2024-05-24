import socket
import threading

rooms = {}  # Dictionary to maintain rooms and their participants

def handle_client(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                handle_message(client_socket, message)
        except:
            remove_client(client_socket)
            break

def handle_message(client_socket, message):
    command, *params = message.split()
    if command == "CREATE":
        room_name = params[0]
        if room_name not in rooms:
            rooms[room_name] = []
        rooms[room_name].append(client_socket)
        client_socket.send(f"Room {room_name} created.".encode())
    elif command == "JOIN":
        room_name = params[0]
        if room_name in rooms:
            rooms[room_name].append(client_socket)
            client_socket.send(f"Joined room {room_name}.".encode())
        else:
            client_socket.send(f"Room {room_name} does not exist.".encode())
    elif command == "LIST":
        room_list = "Open rooms: " + ", ".join(rooms.keys())
        client_socket.send(room_list.encode())

def remove_client(client_socket):
    for room in rooms.values():
        if client_socket in room:
            room.remove(client_socket)
            break
    client_socket.close()

def start_server(ip_address):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_address, 8000))
    server.listen(5)
    print(f"Server started on {ip_address}:8000")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    with open("server_ip.txt", "r") as file:
        ip_address = file.read().strip()
    start_server(ip_address)
