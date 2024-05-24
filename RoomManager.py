import wx
import socket
import threading
import ast
from GameSceneServer import GameScene


class RoomManager(wx.Panel):
    def __init__(self, parent, mode="normal"):
        super(RoomManager, self).__init__(parent)
        self.parent = parent
        self.mode = mode

        self.server_ip = self.read_server_ip()

        self.parent.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.parent.socket.connect((self.server_ip, 8000))

        self.create_widgets()

        threading.Thread(target=self.receive_messages, daemon=True).start()


        self.refresh_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_list_rooms, self.refresh_timer)
        self.refresh_timer.Start(3000)  # Refresh every 3 seconds
        # Check room list as soon as the window is opened
        self.on_list_rooms(None)

    def read_server_ip(self):
        with open("server_ip.txt", "r") as file:
            return file.read().strip()

    def create_widgets(self):
        self.create_btn = wx.Button(self, label="Ajouter une partie")
        self.join_btn = wx.Button(self, label="Rejoindre une partie")
        self.room_input = wx.TextCtrl(self)
        self.room_list = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.room_list.InsertColumn(0, "Nom de la partie")
        self.room_list.SetColumnWidth(0, 400)
        self.room_list.InsertColumn(1, "Mode")

        self.room_list.SetColumnWidth(1, 150)

        self.mode_label = wx.StaticText(self, label=f"Mode: {self.mode}")

        self.create_btn.Bind(wx.EVT_BUTTON, self.on_create_room)
        self.join_btn.Bind(wx.EVT_BUTTON, self.on_join_room)
        self.retour_menu = wx.Button(self, label='Retour au menu principal', size=(150, 40), pos=(490, 790))
        self.retour_menu.Bind(wx.EVT_BUTTON, self.CloseGame)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.mode_label, 0, wx.CENTER | wx.ALL, 5)
        sizer.Add(self.room_input, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.create_btn, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.join_btn, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.room_list, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.retour_menu, 0, wx.ALIGN_RIGHT  | wx.TOP | wx.BOTTOM  | wx.RIGHT ,20)
        
        self.SetSizer(sizer)
      

    def on_create_room(self, event):
        room_name = self.room_input.GetValue()
        self.parent.socket.send(f"CREATE {room_name} {self.mode}".encode())

    def on_join_room(self, event):
        room_name = self.room_input.GetValue()
        print('nano',room_name)
        self.parent.socket.send(f"JOIN {room_name}".encode())
        #self.parent.panel.Destroy()  # Remove the panel with the buttons
        self.parent.ShowMainMenu(True,self.parent.socket)

    def on_list_rooms(self, event):
        self.parent.socket.send("LIST".encode())

    def receive_messages(self):
        while True:
            try:
                message = self.parent.socket.recv(1024).decode()
                if message:
                    print("message sent from server :\n",message)
                    wx.CallAfter(self.display_message, message)
            except:
                break

    def display_message(self, message):
        if message.startswith("Open rooms:"):
            rooms = message[len("Open rooms: "):]
            rooms = ast.literal_eval(rooms)
            self.room_list.DeleteAllItems()
            for key in rooms:
                index = self.room_list.InsertItem(self.room_list.GetItemCount(), key)

                self.room_list.SetItem(index, 1, rooms[key]['mode'])

        else:
            wx.MessageBox(message, "Server Message")

    def join_specific_room(self, event, room_name):
        self.parent.socket.send(f"JOIN {room_name}".encode())

    def CloseGame(self,event):
        self.parent.socket.send("CLOSE".encode())
        self.parent.ShowMainMenu()



