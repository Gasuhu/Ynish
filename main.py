import wx
from GameScene import GameScene
from GameSceneVSai import GameScene as gamesceneao
from RoomManager import RoomManager

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # Add a large label at the top center
        title = wx.StaticText(self.panel, label="Ynish")
        font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        self.vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, -130)  # Move the label a bit higher

        # Add a choice control for selecting game mode
        mode_choices = ["Normal", "Blitz"]
        self.mode_choice = wx.Choice(self.panel, choices=mode_choices, style=wx.CB_SORT)
        choice_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.mode_choice.SetFont(choice_font)
        self.mode_choice.SetSelection(0)  # Default to the first choice
        self.vbox.Add(self.mode_choice, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        # Define button size
        button_size = (200, 60)

        # Add buttons with gaps in between
        button1 = wx.Button(self.panel, label='Jouer à 2 Joueurs', size=button_size)
        button2 = wx.Button(self.panel, label='Jouer vs AI', size=button_size)
        button3 = wx.Button(self.panel, label='Jouer en réseau', size=button_size)

        self.vbox.Add(button1, 0, wx.ALIGN_CENTER | wx.TOP, 20)  # Add top gap for the first button
        self.vbox.Add(button2, 0, wx.ALIGN_CENTER | wx.TOP, 20)  # Add top gap for the second button
        self.vbox.Add(button3, 0, wx.ALIGN_CENTER | wx.TOP, 20)  # Add top gap for the third button

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(self.vbox, 1, wx.ALIGN_CENTER)

        self.panel.SetSizer(self.hbox)

        self.SetSize((600, 800))
        self.SetTitle('Game Menu')
        self.Centre()

        button1.Bind(wx.EVT_BUTTON, self.OnButton1Click)
        button2.Bind(wx.EVT_BUTTON, self.OnButton2Click)
        button3.Bind(wx.EVT_BUTTON, self.OnButton3Click)

    def OnButton1Click(self, event):
        selected_mode = self.mode_choice.GetStringSelection()
        self.ShowGame(selected_mode)
        
    def OnButton2Click(self, event):
        selected_mode = self.mode_choice.GetStringSelection()
        self.ShowGameAI(selected_mode)
    def OnButton3Click(self, event):
        selected_mode = self.mode_choice.GetStringSelection()
        self.ShowRoomMangement(selected_mode)

    def ShowGame(self, mode):
        self.panel.Destroy()  # Remove the panel with the buttons
        game_panel = GameScene(self, mode=mode)  # Pass the selected mode
        self.SetTitle('Game Scene YNISH')
        self.SetSize((700, 900))
        self.Centre()
        self.Layout()
    
    def ShowGameAI(self, mode):
        self.panel.Destroy()  # Remove the panel with the buttons
        game_panel = gamesceneao(self, mode=mode)  # Pass the selected mode
        self.SetTitle('Game Scene YNISH')
        self.SetSize((700, 900))
        self.Centre()
        self.Layout()
    def ShowRoomMangement(self, mode):
        self.panel.Destroy()  # Remove the panel with the buttons
        game_panel = RoomManager(self,mode=mode)  # Pass the selected mode
        self.SetTitle('Room Mangement')
        self.SetSize((600, 800))
        self.Centre()
        self.Layout()

    def ShowMainMenu(self):
        self.DestroyChildren()  # Remove all children components
        self.InitUI()  # Reinitialize the main menu UI

def main():
    app = wx.App()
    frm = MainFrame(None)
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
