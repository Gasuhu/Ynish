import wx
import math

class GameScene(wx.Panel):
    def __init__(self, parent):
        super(GameScene, self).__init__(parent)
        self.activePLayer ='1'
        self.gameType='2player'
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
        self.isJump=False
        self.CellsClickByPLayer1=[]
        self.CellsClickByPLayer2=[]
        self.CellsClickBySmallPLayer1=[]
        self.CellsClickBySmallPLayer2=[]
        self.activeRing=()
        self.BlackPoints=[]
        self.smallRingsToFlip=[]
        self.directions=[ (1,0), (1, 1), (1, -1),(-1, -0), (-1, -1), (-1, 1)]
        self.ringsValidated=[]
        self.ringPlayer1Valided=0
        self.ringPlayer2Valided=0
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
        self.cell_size_x = 50
        self.cell_size_y = 30
        self.start_x = 70
        self.start_y = 120

         # Create turn label
        self.turn = 1
        self.turn_label = wx.StaticText(self, label="Turn: 1", pos=(330, 10))
        self.turn_label = wx.StaticText(self, label="PLAYER 1", pos=(70, 30))
        self.turn_label = wx.StaticText(self, label="PLAYER 2", pos=(565, 30))

        # Create player label
        self.player_label = wx.StaticText(self, label="Player 1 turn play !", pos=(300, 750))

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        self.drawBorder(dc)
        self.drawPlayerCircle(dc,"1")
        self.drawPlayerCircle(dc,"2")
        self.drawHoverCircle(dc)
        self.drawBoard(dc)



            
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
                    self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])
                self.hovered_cell = (row, col)
                self.active_hovered=(row, col)
            else:
                self.hovered_cell = None
        else:
            self.hovered_cell = None
        if(self.hovered_cell is not None):

            # new circle
            x = self.start_x + col * self.cell_size_x 
            y = self.start_y + row * self.cell_size_y 
            self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])

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
                    if(self.activePLayer=='1'):
                        self.CellsClickByPLayer1.append((row, col))
                        self.player_label = wx.StaticText(self, label="Player 2 turn play !", pos=(300, 750))
                        self.board[row][col]=2
                        self.activePLayer='2'
                    else :
                        self.board[row][col]=-2
                        self.CellsClickByPLayer2.append((row, col))
                        self.activePLayer='1'
                        self.player_label = wx.StaticText(self, label="Player 1 turn play !", pos=(300, 750))
                    self.turn+=1
                    self.turn_label = wx.StaticText(self, label="Turn: {0}".format(self.turn), pos=(330, 10))


                else:
                    self.hovered_cell = None
        else :
            if not self.isJump:
                if 0 <= row < len(self.board) and 0 <= col < len(self.board[0]):
                    if self.board[row][col] != 0 and self.isHoverPlayer() :
                        x = self.start_x + col * self.cell_size_x 
                        y = self.start_y + row* self.cell_size_y 
                        self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])
                        if(self.activePLayer=='1'):
                            self.CellsClickBySmallPLayer1.append((row, col))
                            self.board[row][col]=3
                        else :
                            self.board[row][col]=-3
                            self.CellsClickBySmallPLayer2.append((row, col))
                        self.isJump=True
                        self.activeRing=(row,col)
                        self.addBlackPoints([row,col])
                        self.RefreshBlackDots()

            else:
                if 0 <= row < len(self.board) and 0 <= col < len(self.board[0]):
                    if self.board[row][col] != 0 and self.hovered_cell in self.BlackPoints:
                        x = self.start_x + col * self.cell_size_x 
                        y = self.start_y + row* self.cell_size_y 
                        self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])
                        if(self.activePLayer=='1'):
                            self.CellsClickByPLayer1.append((row, col))
                            self.CellsClickByPLayer1.remove(self.activeRing)
                            self.activePLayer='2'
                            self.board[row][col]=2
                            self.player_label = wx.StaticText(self, label="Player 2 turn play !", pos=(300, 750))

                        else :
                            self.activePLayer='1'                            
                            self.board[row][col]=-2
                            self.CellsClickByPLayer2.append((row, col))
                            self.CellsClickByPLayer2.remove(self.activeRing)
                            self.player_label = wx.StaticText(self, label="Player 1 turn play !", pos=(300, 750))

                        _row=self.activeRing[0]
                        _col=self.activeRing[1]
                        x = self.start_x + _col * self.cell_size_x 
                        y = self.start_y + _row* self.cell_size_y 
                        self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])
                        self.flip((row, col))

                        self.isJump=False
                        self.RefreshBlackDots(True)
                        self.turn+=1
                        self.turn_label = wx.StaticText(self, label="Turn: {0}".format(self.turn), pos=(330, 10))
                        # chech for player 1
                        if(self.check_five_in_a_line(3)):
                            self.ringPlayer1Valided+=1
                            for ring in self.ringsValidated:
                                self.CellsClickBySmallPLayer1.remove(ring)
                                x = self.start_x + ring[1] * self.cell_size_x 
                                y = self.start_y + ring[0]* self.cell_size_y 
                                self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])

                        if(self.check_five_in_a_line(-3)):
                            self.ringPlayer2Valided+=1
                            for ring in self.ringsValidated:
                                self.CellsClickBySmallPLayer2.remove(ring)
                                x = self.start_x + ring[1] * self.cell_size_x 
                                y = self.start_y + ring[0]* self.cell_size_y 
                                self.Refresh(eraseBackground=False,rect=[x, y-self.cell_size_y //2, self.cell_size_x,2*self.cell_size_y])



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


        rows = len(self.board)
        cols = len(self.board[0])

        
        for x in range(rows):
            for y in range(cols):
                if self.board[x][y] == player:
                    for dx, dy in self.directions:
                        if check_direction_diagonal(x, y, dx, dy):
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
                self.CellsClickBySmallPLayer1.remove(tuple(pos))
                self.CellsClickBySmallPLayer2.append(tuple(pos))

            else :
                if(self.board[pos[0]][pos[1]] == -3):
                    self.board[pos[0]][pos[1]]= 3
                    self.CellsClickBySmallPLayer2.remove(tuple(pos))
                    self.CellsClickBySmallPLayer1.append(tuple(pos))
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
        return pos in self.CellsClickByPLayer1 or pos in self.CellsClickByPLayer2
    
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
                if(self.activePLayer=='1'):
                    dc.SetBrush(wx.Brush(wx.Colour(255, 255, 175)))  # Set brush color to red
                else:
                    dc.SetBrush(wx.Brush(wx.Colour(130, 130, 255)))  # Set brush color to red
                dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, outer_radius)
                dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
                dc.SetBrush(wx.Brush(wx.WHITE))  # Set brush color to red
                dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, inner_radius)
        else :
            if  not self.isJump :
                if self.isHoverPlayer():
                    row, col = self.hovered_cell
                    x = self.start_x + col * self.cell_size_x
                    y = self.start_y + row * self.cell_size_y
                    # Draw empty circle with 4 pixel width
                    outer_radius = self.cell_size_x // 2 - 10
                    dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
                    if(self.activePLayer=='1'):
                        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 175)))  # Set brush color to red
                    else:
                        dc.SetBrush(wx.Brush(wx.Colour(130, 130, 255)))  # Set brush color to red
                    dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, outer_radius)
            else :
                if self.hovered_cell in self.BlackPoints:
                    row, col = self.hovered_cell
                    x = self.start_x + col * self.cell_size_x
                    y = self.start_y + row * self.cell_size_y
                    # Draw empty circle with 4 pixel width
                    outer_radius = self.cell_size_x // 2 - 2
                    inner_radius = outer_radius - 5
                    dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
                    if(self.activePLayer=='1'):
                        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 175)))  # Set brush color to red
                    else:
                        dc.SetBrush(wx.Brush(wx.Colour(130, 130, 255)))  # Set brush color to red
                    dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, outer_radius)
                    dc.SetPen(wx.Pen(wx.BLACK, 1))  # Set pen color to blue with a width of 4 pixels
                    dc.SetBrush(wx.Brush(wx.WHITE))  # Set brush color to red
                    dc.DrawCircle(x + self.cell_size_x // 2, y + self.cell_size_y // 2, inner_radius)


    def isHoverPlayer(self):
        return self.hovered_cell is not None and (self.hovered_cell in self.CellsClickByPLayer1 and self.activePLayer=='1'
                        or  self.hovered_cell in self.CellsClickByPLayer2 and self.activePLayer=='2')
    def drawPlayerCircle(self,dc,player):
        cells = self.CellsClickByPLayer1 if player == "1" else self.CellsClickByPLayer2
        cellsSmall = self.CellsClickBySmallPLayer1 if player == "1" else self.CellsClickBySmallPLayer2
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
            
