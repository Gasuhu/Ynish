import wx
import socket
import threading

class RoomManager(wx.Panel):
    def __init__(self,parent, mode):
        super(RoomManager, self).__init__(parent)
        self.parent = parent

        self.server_ip = self.read_server_ip()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, 8000))

        self.create_widgets()

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def read_server_ip(self):
        with open("server_ip.txt", "r") as file:
            return file.read().strip()

    def create_widgets(self):
        self.create_btn = wx.Button(self, label="Create Room")
        self.join_btn = wx.Button(self, label="Join Room")
        self.list_btn = wx.Button(self, label="List Rooms")
        self.room_input = wx.TextCtrl(self)
        self.room_list = wx.ListBox(self)

        self.create_btn.Bind(wx.EVT_BUTTON, self.on_create_room)
        self.join_btn.Bind(wx.EVT_BUTTON, self.on_join_room)
        self.list_btn.Bind(wx.EVT_BUTTON, self.on_list_rooms)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.room_input, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.create_btn, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.join_btn, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.list_btn, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.room_list, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

    def on_create_room(self, event):
        room_name = self.room_input.GetValue()
        self.socket.send(f"CREATE {room_name}".encode())

    def on_join_room(self, event):
        room_name = self.room_input.GetValue()
        self.socket.send(f"JOIN {room_name}".encode())

    def on_list_rooms(self, event):
        self.socket.send("LIST".encode())

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode()
                if message:
                    wx.CallAfter(self.display_message, message)
            except:
                break

    def display_message(self, message):
        if message.startswith("Open rooms:"):
            rooms = message[len("Open rooms: "):].split(", ")
            self.room_list.Set(rooms)
        else:
            wx.MessageBox(message, "Server Message")


