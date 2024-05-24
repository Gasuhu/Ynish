import socket
import threading

rooms = {}  # Dictionary to maintain rooms and their participants
roomCreators = {} # Dictionary to maintain
roomsInGame = {} # Dictionary to maintain in game state

def handle_client(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                handle_message(client_socket, message,address)
        except:
            remove_client(client_socket)
            break

def handle_message(client_socket, message,address):
    command, *params = message.split()
    print("message : ",message)
    if command == "CREATE":
        room_name = params[0]
        if room_name not in rooms:
            rooms[room_name] = {'mode':params[1] }
            roomCreators[room_name] ={'creator':client_socket }
        client_socket.send(f"Room {room_name} created. Mode : {params[1]}".encode())
        room_list = "Open rooms: " + f"{rooms}"
        client_socket.send(room_list.encode())
    elif command == "JOIN":
        room_name = params[0]
        if room_name in rooms:
            del rooms[room_name]
            client_socket.send(f"Joined room {room_name}.".encode())
            roomCreators[room_name].creator.send(f'GameStarted Player2')
            roomCreators[room_name].creator.send(f'GameStarted Player1')
            del roomCreators[room_name]
        if room_name not in roomsInGame:
            roomsInGame[room_name]={'gameState':{},'player1':"",'player2':""}
        else:
            client_socket.send(f"Room {room_name} does not exist.".encode())
    elif command == "LIST":
        room_list = "Open rooms: " + f"{rooms}"
        client_socket.send(room_list.encode())
    elif command == "START":
        room_name = params[0]
        player = params[1]
        roomsInGame[room_name][player]= client_socket
        roomsInGame[room_name]['game_state'] = {
                    'activePlayer': '1',
                    'isJump': False,
                    'CellsClickByPlayer1': [],
                    'CellsClickByPlayer2': [],
                    'CellsClickBySmallPlayer1': [],
                    'CellsClickBySmallPlayer2': [],
                    'activeRing': (),
                    'BlackPoints': [],
                    'smallRingsToFlip': [],
                    'directions': [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, -1), (-1, 1)],
                    'directionDiagonal': [(1, 1), (1, -1), (-1, -1), (-1, 1)],
                    'directionVertical': [(1, 0), (-1, 0)],
                    'ringsValidated': [],
                    'ringPlayer1Validated': 0,
                    'ringPlayer2Validated': 0,
                    'hovered_cell': None,
                    'active_hovered': None,
                    'board': [
                        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
                        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
                    ],
                    'selectRingPlayer1': False,
                    'selectRingPlayer2': False,
                    'turn': 1
                }

 


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
    # with open("server_ip.txt", "r") as file:
    #     ip_address = file.read().strip()
    start_server("localhost")
