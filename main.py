import wx
from GameScene import GameScene


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
        mode_choices = ["Normal","Blitz"]
        self.mode_choice = wx.Choice(self.panel, choices=mode_choices)
        choice_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.mode_choice.SetFont(choice_font)
        self.mode_choice.SetSelection(0)  # Default to the first choice
        self.vbox.Add(self.mode_choice, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        # Define button size
        button_size = (200, 60)

        # Add buttons with gaps in between
        play2player = wx.Button(self.panel, label='Jouer à 2 Joueurs', size=button_size)
        playAi = wx.Button(self.panel, label='Jouer vs AI', size=button_size)
        playLan = wx.Button(self.panel, label='Jouer en réseau', size=button_size)

        self.vbox.Add(play2player, 0, wx.ALIGN_CENTER | wx.TOP, 20)  # Add top gap for the first button
        self.vbox.Add(playAi, 0, wx.ALIGN_CENTER | wx.TOP, 20)  # Add top gap for the second button
        self.vbox.Add(playLan, 0, wx.ALIGN_CENTER | wx.TOP, 20)  # Add top gap for the third button

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(self.vbox, 1, wx.ALIGN_CENTER)

        self.panel.SetSizer(self.hbox)

        self.SetSize((600, 800))
        self.SetTitle('Game Menu')
        self.Centre()

        play2player.Bind(wx.EVT_BUTTON, self.OnPlay2player)
        playAi.Bind(wx.EVT_BUTTON, self.OnPlayAi)
        playLan.Bind(wx.EVT_BUTTON, self.OnPlayLan)

    def OnPlay2player(self, event):
        selected_mode = self.mode_choice.GetStringSelection()
        self.ShowGame(selected_mode,'2player')
        
    def OnPlayAi(self, event):
        selected_mode = self.mode_choice.GetStringSelection()
        self.ShowGame(selected_mode,'ai')
    def OnPlayLan(self, event):
        selected_mode = self.mode_choice.GetStringSelection()
        self.ShowRoomMangement(selected_mode)

    def ShowGame(self, mode,game_type):
        self.panel.Destroy()  # Remove the panel with the buttons
        GameScene(self, mode=mode,game_type=game_type)  # Pass the selected mode
        self.SetTitle('Game Scene YNISH')
        self.SetSize((700, 900))
        self.Centre()
        self.Layout()
    


    def ShowMainMenu(self,server=False,socket=None):
        self.DestroyChildren()  # Remove all children components
        self.InitUI()  # Reinitialize the main menu UI
        if(server):
            self.ShowGameServer("Normal",socket)


def main():
    app = wx.App()
    frm = MainFrame(None)
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
