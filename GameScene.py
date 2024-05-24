import wx

class GameScene(wx.Panel):
    def __init__(self, parent,mode):
        super(GameScene, self).__init__(parent)
        self.parent = parent
        #Blitz
        if( mode=="Blitz" ):
            self.finish =1 
        #Mode normal
        else:
            self.finish= 3
        # Paramètres du jeu
        self.gameType = '2player'
        self.activePlayer = '1'
        self.isJump = False
        self.turn = 1

        # État du jeu
        self.CellsClickByPlayer1 = []
        self.CellsClickByPlayer2 = []
        self.CellsClickBySmallPlayer1 = []
        self.CellsClickBySmallPlayer2 = []
        self.BlackPoints = []
        self.smallRingsToFlip = []
        self.ringsValidated = []
        self.ringPlayer1Validated = 0
        self.ringPlayer2Validated = 0

        # Directions pour la logique du jeu
        self.directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, -1), (-1, 1)]
        self.directionDiagonal = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        self.directionVertical = [(1, 0), (-1, 0)]

        # Plateau et paramètres UI
        self.board = [
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
        ]
        
        self.cell_size_x = 50
        self.cell_size_y = 30
        self.start_x = 70
        self.start_y = 130
        
        self.selectRingPlayer1 = False
        self.selectRingPlayer2 = False

        # Stocker les indices des cellules survolées et actives
        self.hovered_cell = None
        self.active_hovered = None

        # Création des labels de tour et de joueur
        wx.StaticText(self, label="PLAYER 1", pos=(70, 30))
        self.player1Pos = (50, 60)
        wx.StaticText(self, label="PLAYER 2", pos=(565, 30))
        self.player2Pos = (545, 60)


        # Boutons pour retourner au menu principal et redémarrer le jeu
        retour_menu = wx.Button(self, label='Retour au menu principal', size=(150, 40), pos=(490, 790))
        retour_menu.Bind(wx.EVT_BUTTON, self.CloseGame)
        self.retourner = False  
        self.retournerButton = wx.Button(self, label="Annuler",size=(150, 40), pos=(50, 750))
        self.retournerButton.Hide()  # Initially hide the button
        self.retournerButton.Bind(wx.EVT_BUTTON, self.unselectRing)

        redemarrer = wx.Button(self, label='Redémarrer la partie', size=(150, 40), pos=(50, 790))
        redemarrer.Bind(wx.EVT_BUTTON, self.RestartGame)

        # Création des labels de tour et de joueur actif
        self.turn_label = wx.StaticText(self, label="Turn: 1", pos=(330, 10))
        self.player_label = wx.StaticText(self, label="Player 1 turn play !", pos=(300, 750))

        # Liaison des événements
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)

    def OnPaint(self, event):
        # Créer le contexte de dessin
        dc = wx.PaintDC(self)
        dc.Clear()  # Effacer l'écran

        # Dessiner les différents éléments du jeu
        self.drawBorder(dc)  # Dessiner les bordures
        self.drawPlayerCircle(dc, "1")  # Dessiner le cercle du joueur 1
        self.drawPlayerCircle(dc, "2")  # Dessiner le cercle du joueur 2
        self.drawHoverCircle(dc)  # Dessiner le cercle survolé
        self.drawBoard(dc)  # Dessiner le plateau de jeu
        self.drawValidationsRings(dc)  # Dessiner les anneaux validés

        # Vérifier si la partie est terminée
        self.checkEndGame()



            
    def OnMotion(self, event):
        x, y = event.GetPosition()
        col = (x - self.start_x) // self.cell_size_x
        row = (y - self.start_y) // self.cell_size_y
        if 0 <= row < len(self.board) and 0 <= col < len(self.board[0]):
            if self.board[row][col] != 0:
               
                if(self.active_hovered==(row, col)):
                    return
                # delete old circle
                if self.active_hovered is not None :
                    x = self.start_x + self.active_hovered[1] * self.cell_size_x 
                    y = self.start_y + self.active_hovered[0] * self.cell_size_y 
                    self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2-50, self.cell_size_x,2*self.cell_size_y+50])
                self.hovered_cell = (row, col)
                self.active_hovered=(row, col)
                # new circle
                x = self.start_x + col * self.cell_size_x 
                y = self.start_y + row * self.cell_size_y 
                self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2-50, self.cell_size_x,2*self.cell_size_y+50])




    def OnLeftClick(self, event):
        x, y = event.GetPosition()
        col = (x - self.start_x) // self.cell_size_x
        row = (y - self.start_y) // self.cell_size_y
        if(self.turn<=10):
            if 0 <= row < len(self.board) and 0 <= col < len(self.board[0]):
                if self.board[row][col] != 0 and not self.isClicked((row, col)) :

                    x = self.start_x + col * self.cell_size_x 
                    y = self.start_y + row* self.cell_size_y 
                    self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])
                    if(self.activePlayer=='1'):
                        self.CellsClickByPlayer1.append((row, col))
                        self.player_label = wx.StaticText(self, label="Player 2 turn play !                  ", pos=(300, 750))
                        self.board[row][col]=2
                        self.activePlayer='2'
                    else :
                        self.board[row][col]=-2
                        self.CellsClickByPlayer2.append((row, col))
                        self.activePlayer='1'
                        self.player_label = wx.StaticText(self, label="Player 1 turn play !                   ", pos=(300, 750))
                    self.turn+=1
                    self.turn_label = wx.StaticText(self, label="Turn: {0}".format(self.turn), pos=(330, 10))


                else:
                    self.hovered_cell = None
        else :
            if not self.isJump and not(self.selectRingPlayer1 or self.selectRingPlayer2):
                if 0 <= row < len(self.board) and 0 <= col < len(self.board[0]):
                    if self.board[row][col] != 0 and self.isHoverPlayer() :
                        x = self.start_x + col * self.cell_size_x 
                        y = self.start_y + row* self.cell_size_y 
                        self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])
                        if(self.activePlayer=='1'):
                            self.CellsClickBySmallPlayer1.append((row, col))
                            self.board[row][col]=3
                        else :
                            self.board[row][col]=-3
                            self.CellsClickBySmallPlayer2.append((row, col))
                        self.isJump=True
                        self.activeRing=(row,col)
                        self.addBlackPoints([row,col])
                        self.RefreshBlackDots()
                        self.retourner=True
                        self.update_button_visibility()

            else:
                if 0 <= row < len(self.board) and 0 <= col < len(self.board[0]) :
                    if self.board[row][col] != 0 and self.hovered_cell in self.BlackPoints and not(self.selectRingPlayer1 or self.selectRingPlayer2):
                        x = self.start_x + col * self.cell_size_x 
                        y = self.start_y + row* self.cell_size_y 
                        self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])
                        if(self.activePlayer=='1'):
                            self.CellsClickByPlayer1.append((row, col))
                            self.CellsClickByPlayer1.remove(self.activeRing)
                            self.activePlayer='2'
                            self.board[row][col]=2
                            self.player_label = wx.StaticText(self, label="Player 2 turn play !                ", pos=(300, 750))

                        else :
                            self.activePlayer='1'                            
                            self.board[row][col]=-2
                            self.CellsClickByPlayer2.append((row, col))
                            self.CellsClickByPlayer2.remove(self.activeRing)
                            self.player_label = wx.StaticText(self, label="Player 1 turn play !                 ", pos=(300, 750))

                        _row=self.activeRing[0]
                        _col=self.activeRing[1]
                        x = self.start_x + _col * self.cell_size_x 
                        y = self.start_y + _row* self.cell_size_y 
                        self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])
                        self.flip((row, col))

                        self.isJump=False
                        self.RefreshBlackDots(True)
                        self.retourner=False
                        self.update_button_visibility()
                        self.turn+=1
                        self.turn_label = wx.StaticText(self, label="Turn: {0}".format(self.turn), pos=(330, 10))
                        # chech for player 1
                        if(self.process_ring_validation(3, self.CellsClickBySmallPlayer1)):
                            self.activePlayer='1'
                            self.player_label = wx.StaticText(self, label="Player {0} turn play ! Choisie un anneaux a enlever".format(self.activePlayer), pos=(300, 750))

                            self.turn-=1
                        if(self.process_ring_validation(-3, self.CellsClickBySmallPlayer2)):
                            self.activePlayer='2'
                            self.player_label = wx.StaticText(self, label="Player {0} turn play ! Choisie un anneaux a enlever".format(self.activePlayer), pos=(300, 750))
                            self.turn-=1
                        self.turn_label = wx.StaticText(self, label="Turn: {0}".format(self.turn), pos=(330, 10))

                    else :
                        if self.selectRingPlayer1 or self.selectRingPlayer2:
                            if self.isHoverPlayer():
                                self.selectRingPlayer1=False
                                self.selectRingPlayer2=False
                                
                                if(self.activePlayer=='1'):
                                    self.activePlayer='2'
                                    self.ringPlayer1Validated +=1
                                    self.CellsClickByPlayer1.remove((row,col))
                                else:
                                    self.activePlayer='1'
                                    self.ringPlayer2Validated +=1
                                    self.CellsClickByPlayer2.remove((row,col))
                                self.board[row][col]= 1
                                self.turn+=1
                                self.Refresh(eraseBackground=False,rect=(50,50,200,200) if self.activePlayer!='1' else (545,50,200,200) )
                        
                    


    def drawValidationsRings(self,dc):
        for i in range(self.ringPlayer1Validated):
            self.draw_validattion_ring(dc,'1',i)
        for i in range(self.ringPlayer2Validated):
            self.draw_validattion_ring(dc,'2',i)
    def draw_validattion_ring(self,dc,player,i):
        row, col = self.player1Pos if player=="1" else self.player2Pos
        x =row + i*15
        y = col
        outer_radius = self.cell_size_x // 2 - 2
        inner_radius = outer_radius - 5
        dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
        dc.SetBrush(wx.Brush(wx.YELLOW if player =="1" else wx.BLUE ))  # Set brush color to red
        dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, outer_radius)
        dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
        dc.SetBrush(wx.Brush(wx.Colour(240, 240, 240)))  # Set brush color to red
        dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, inner_radius)
    def process_ring_validation(self, check_value, cells_click_list):
        if self.check_five_in_a_line(check_value):
            if  check_value == 3 :
                 self.selectRingPlayer1=True
                 #self.ringPlayer1Validated +=1
            else :
                self.selectRingPlayer2=True
                #self.ringPlayer2Validated +=1 
            for ring in self.ringsValidated:
                cells_click_list.remove(ring)
                self.board[ring[0]][ring[1]] = 1
                x = self.start_x + ring[1] * self.cell_size_x 
                y = self.start_y + ring[0] * self.cell_size_y 
                self.Refresh(eraseBackground=False, rect=[x, y - self.cell_size_y // 2, self.cell_size_x, 2 * self.cell_size_y])
            

            return True
        return False
    def check_five_in_a_line(self,player):
            
        def in_bounds(x, y):
            return 0 <= x < rows and 0 <= y < cols
    
        def check_direction_diagonal(x, y, dx, dy):
            self.ringsValidated=[]
            for i in range(5):
                if not in_bounds(x + i * dx, y + i * dy) or self.board[x + i * dx][y + i * dy] != player:
                    return False
                self.ringsValidated.append((x + i * dx,y + i * dy))
            return True 
            
        def check_direction_vertical(x, y, dx, dy):
            self.ringsValidated=[]
            for i in range(10):
                if not in_bounds(x + i * dx, y + i * dy) or self.board[x + i * dx][y + i * dy] not in [player,0]:
                    return False
                if self.board[x + i * dx][y + i * dy] == player :
                    self.ringsValidated.append((x + i * dx,y + i * dy))
            return True 


        rows = len(self.board)
        cols = len(self.board[0])

        
        for x in range(rows):
            for y in range(cols):
                if self.board[x][y] == player:
                    for dx, dy in self.directionDiagonal:
                        if check_direction_diagonal(x, y, dx, dy):
                            return True
                    for dx, dy in self.directionVertical:
                        if check_direction_vertical(x, y, dx, dy):
                            return True
        return False  
                    
    def flip(self,pos):
        direction,iteration =self.getDirection(pos)
        pos = list(pos)
        for i in range(1,iteration):
            pos[0]-=direction[0]
            pos[1]-=direction[1]

            if(self.board[pos[0]][pos[1]] == 3):
                self.board[pos[0]][pos[1]]= -3
                self.CellsClickBySmallPlayer1.remove(tuple(pos))
                self.CellsClickBySmallPlayer2.append(tuple(pos))

            else :
                if(self.board[pos[0]][pos[1]] == -3):
                    self.board[pos[0]][pos[1]]= 3
                    self.CellsClickBySmallPlayer2.remove(tuple(pos))
                    self.CellsClickBySmallPlayer1.append(tuple(pos))
            x = self.start_x + pos[1] * self.cell_size_x 
            y = self.start_y + pos[0]* self.cell_size_y 

            self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])

        
    def getDirection(self,pos):
        row = pos[0]-self.activeRing[0]
        col = pos[1]-self.activeRing[1]
        iteration=max(abs(row),abs(col))
        return (row//iteration,col//iteration) , iteration
            



    
    def RefreshBlackDots(self,erase=False):
        for pos in self.BlackPoints:
            x = self.start_x + pos[1] * self.cell_size_x 
            y = self.start_y + pos[0] * self.cell_size_y 
            self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])
        if(erase):
            self.BlackPoints=[]
    def addBlackPoints(self,pos):

        for direction in self.directions:
            start = pos.copy()
            self.addPointsTillEnd(direction,start)


    def addPointsTillEnd(self,direction,pos,last=False):
        # 11 column and 19 rows 
        pos[0] +=  direction[0]
        pos[1] +=  direction[1]
        if(pos[0]>=0 and pos[0]<=18 and pos[1]>=0 and pos[1]<=10):
            if(self.board[pos[0]][pos[1]] == 1):
                self.BlackPoints.append((pos[0],pos[1]))
                if(not last):
                    self.addPointsTillEnd(direction,pos,last)
                else :
                    return False 
            else:
                if(self.board[pos[0]][pos[1]] in [3,-3]):   
                    self.addPointsTillEnd(direction,pos,True)
                else :
                    if(self.board[pos[0]][pos[1]] in [2,-2]):
                        return False
                    self.addPointsTillEnd(direction,pos,last)
    
  
        
            
    def isClicked(self,pos):
        return pos in self.CellsClickByPlayer1 or pos in self.CellsClickByPlayer2
    
    def drawBorder(self,dc):
        rect = wx.Rect(self.start_x-20, self.start_y-20, self.cell_size_x*11+40 , self.cell_size_y*19+40)
        dc.DrawRoundedRectangle(rect, 15)
    def drawBoard(self,dc):

        dc.SetPen(wx.Pen(wx.BLACK, 1)) 
        for row_index, row in enumerate(self.board):
            for col_index, cell in enumerate(row):
                if cell != 0:
                    x = self.start_x + col_index * self.cell_size_x
                    y = self.start_y + row_index * self.cell_size_y
                    dc.DrawLine(x, y, x + self.cell_size_x, y + self.cell_size_y)
                    dc.DrawLine(x + self.cell_size_x, y, x, y + self.cell_size_y)
                    dc.DrawLine(x + int(self.cell_size_x/2), y-int(self.cell_size_y/2), x+int(self.cell_size_x/2), y+self.cell_size_y+int(self.cell_size_y/2))

    def drawHoverCircle(self,dc):
        # 5 start 
        if(self.turn<=10):
            if self.hovered_cell is not None and not self.isClicked(self.hovered_cell):
                row, col = self.hovered_cell
                x = self.start_x + col * self.cell_size_x
                y = self.start_y + row * self.cell_size_y
                # Draw empty circle with 4 pixel width
                outer_radius = self.cell_size_x // 2 - 2
                inner_radius = outer_radius - 5
                dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
                if(self.activePlayer=='1'):
                    dc.SetBrush(wx.Brush(wx.Colour(255, 255, 175)))  # Set brush color to red
                else:
                    dc.SetBrush(wx.Brush(wx.Colour(130, 130, 255)))  # Set brush color to red
                dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, outer_radius)
                dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
                dc.SetBrush(wx.Brush(wx.WHITE))  # Set brush color to red
                dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, inner_radius)

        else :
            if  not self.isJump and not(self.selectRingPlayer1 or self.selectRingPlayer2) :
                if self.isHoverPlayer():
                    row, col = self.hovered_cell
                    x = self.start_x + col * self.cell_size_x
                    y = self.start_y + row * self.cell_size_y
                    # Draw empty circle with 4 pixel width
                    outer_radius = self.cell_size_x // 2 - 10
                    dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
                    if(self.activePlayer=='1'):
                        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 175)))  # Set brush color to red
                    else:
                        dc.SetBrush(wx.Brush(wx.Colour(130, 130, 255)))  # Set brush color to red
                    dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, outer_radius)
            else :
                if self.hovered_cell in self.BlackPoints and not(self.selectRingPlayer1 or self.selectRingPlayer2):
                    row, col = self.hovered_cell
                    x = self.start_x + col * self.cell_size_x
                    y = self.start_y + row * self.cell_size_y
                    # Draw empty circle with 4 pixel width
                    outer_radius = self.cell_size_x // 2 - 2
                    inner_radius = outer_radius - 5
                    dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
                    if(self.activePlayer=='1'):
                        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 175)))  # Set brush color to red
                    else:
                        dc.SetBrush(wx.Brush(wx.Colour(130, 130, 255)))  # Set brush color to red
                    dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, outer_radius)
                    dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
                    dc.SetBrush(wx.Brush(wx.WHITE))  # Set brush color to red
                    dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, inner_radius)
    
            if(self.selectRingPlayer1 or self.selectRingPlayer2):
                if self.isHoverPlayer():
                    row, col = self.hovered_cell
                    x = self.start_x + col * self.cell_size_x
                    y = self.start_y + row * self.cell_size_y
                    cells=self.CellsClickByPlayer1  if self.selectRingPlayer1 else self.CellsClickByPlayer2
                    if self.hovered_cell in cells:
                        if(self.activePlayer=='1'):
                            dc.SetBrush(wx.Brush(wx.YELLOW))  
                        else:
                            dc.SetBrush(wx.Brush(wx.BLUE))  
                        
                        self.drawTriangle(x,y,dc)


    def drawTriangle(self,x,y,dc):
        points = [(x + self.cell_size_x // 2, y +  self.cell_size_y // 2 -30 ), (x+self.cell_size_x // 2 - 12, y+  self.cell_size_y // 2 -50), (x + self.cell_size_x // 2+12, y+ self.cell_size_y // 2+-50)]

        # Draw the filled triangle
        dc.DrawPolygon(points)


    def isHoverPlayer(self):
        return self.hovered_cell is not None and (self.hovered_cell in self.CellsClickByPlayer1 and self.activePlayer=='1'
                        or  self.hovered_cell in self.CellsClickByPlayer2 and self.activePlayer=='2')
    def drawPlayerCircle(self,dc,player):
        cells = self.CellsClickByPlayer1 if player == "1" else self.CellsClickByPlayer2
        cellsSmall = self.CellsClickBySmallPlayer1 if player == "1" else self.CellsClickBySmallPlayer2
        for pos in cells :
            row, col = pos
            x = self.start_x + col * self.cell_size_x
            y = self.start_y + row * self.cell_size_y
            # Draw empty circle with 4 pixel width
            outer_radius = self.cell_size_x // 2 - 2
            inner_radius = outer_radius - 5
            dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
            dc.SetBrush(wx.Brush(wx.YELLOW if player =="1" else wx.BLUE ))  # Set brush color to red
            dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, outer_radius)
            dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
            dc.SetBrush(wx.Brush(wx.WHITE))  # Set brush color to red
            dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, inner_radius)
        for pos in cellsSmall :
            row, col = pos
            x = self.start_x + col * self.cell_size_x
            y = self.start_y + row * self.cell_size_y
            # Draw empty circle with 4 pixel width
            outer_radius = self.cell_size_x // 2 - 10
            inner_radius = outer_radius - 5
            dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
            dc.SetBrush(wx.Brush(wx.YELLOW if player =="1" else wx.BLUE ))  # Set brush color to red
            dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, outer_radius)
        for pos in self.BlackPoints:
            row, col = pos
            x = self.start_x + col * self.cell_size_x
            y = self.start_y + row * self.cell_size_y
            # Draw empty circle with 4 pixel width
            outer_radius = 4

            dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
            dc.SetBrush(wx.Brush(wx.BLACK ))  # Set brush color to red
            dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, outer_radius)
    
    def checkEndGame(self):
        if(self.ringPlayer1Validated == self.ringPlayer2Validated and self.ringPlayer1Validated==self.finish):
            self.ShowEndGameDialog("0")

        if(self.ringPlayer1Validated==self.finish):
            self.ShowEndGameDialog("1")
        else:
            if(self.ringPlayer2Validated==self.finish):
                self.ShowEndGameDialog("2")

            
    def ShowEndGameDialog(self,player):
        if(player != "0"):
            dlg = wx.MessageDialog(self, 
                "Le joueur {0} a gagnée la partie ! Voulez vous rejouer ?".format(player), 
                "Fin", 
                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
        else:
            dlg = wx.MessageDialog(self, 
                "La partie est fini en égalité ! Voulez vous rejouer ?".format(player), 
                "Fin", 
                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)

        dlg.SetYesNoLabels("Rejouer", "Retourner")

        result = dlg.ShowModal()
        if result == wx.ID_YES:
            self.RestartGame(None)
        elif result == wx.ID_NO:
            self.CloseGame(None)
        dlg.Destroy()

    def RestartGame(self,event):
        self.activePlayer ='1'
        self.isJump=False
        self.CellsClickByPlayer1=[]
        self.CellsClickByPlayer2=[]
        self.CellsClickBySmallPlayer1=[]
        self.CellsClickBySmallPlayer2=[]
        self.activeRing=()
        self.BlackPoints=[]
        self.smallRingsToFlip=[]
        self.directions=[ (1,0), (1, 1), (1, -1),(-1, 0), (-1, -1), (-1, 1)]
        self.directionDiagonal=[(1, 1), (1, -1),(-1, -1), (-1, 1)]
        self.directionVertical=[(1,0),(-1,0)]
        self.ringsValidated=[]
        self.ringPlayer1Validated=0
        self.ringPlayer2Validated=0
        self.hovered_cell = None  # Store the index of the hovered cell
        self.active_hovered=None # Store the index of the active
        self.board = [
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
        ]
        self.selectRingPlayer1 = False
        self.selectRingPlayer2 = False
        self.turn = 1
        self.turn_label = wx.StaticText(self, label="Turn: 1    ", pos=(330, 10))
        # Create player label
        self.player_label = wx.StaticText(self, label="Player 1 turn play !\t\t\t\t ", pos=(300, 750))
        self.Refresh()


    def CloseGame(self,event):
        confirmation_dialog = wx.MessageDialog(
            self, 
            "Voulez vous vraimment quiter la partie actuelle", 
            "Confiramation", 
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        )

        if confirmation_dialog.ShowModal() == wx.ID_YES:
            self.parent.ShowMainMenu()
        
        confirmation_dialog.Destroy()
    def update_button_visibility(self):
        if self.retourner:
            self.retournerButton.Show()
        else:
            self.retournerButton.Hide()

        # Update the layout to reflect the changes
        self.Layout()
    def unselectRing(self,event):
        self.retourner=False
        self.update_button_visibility()
        self.RefreshBlackDots(True)
        self.CellsClickBySmallPlayer1.pop()
        self.isJump=False
