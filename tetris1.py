#global variables (lists) representing each row of the board
from graphics import *
from random import randint


class Block(Rectangle):
    def __init__(self, p, color):
        self.p=p
        self.p1=Point(self.p.getX()*30, self.p.getY()*30)
        self.p2=Point(self.p1.getX()+30, self.p1.getY()+30)
        Rectangle.__init__(self, self.p1, self.p2)
        self.setFill(color)

    def can_move(self,board,dx,dy):
        if board.can_move(self.p.x+dx,self.p.y+dy)==True:
            return True
        else:
            return False
        #check borders
        #returns true of false depending on whether the block can move dx or dy squares
        
    def move(self,dx,dy):
        self.dx=dx*30
        self.dy=dy*30
        Rectangle.move(self,self.dx,self.dy)
        self.p.x += dx
        self.p.y += dy

class Shape(object):
    def __init__(self, points, color):
        self.blocks=[Block(points[0],color),Block(points[1],color),Block(points[2],color),Block(points[3],color)]
        self.rotation_dir = 1
        #boolean to indicate whether or not the shape has rotated
             
    def draw(self, win):
        self.blocks[0].draw(win)
        self.blocks[1].draw(win)
        self.blocks[2].draw(win)
        self.blocks[3].draw(win)

    def move(self,dx,dy):
        self.blocks[0].move(dx,dy)
        self.blocks[1].move(dx,dy)
        self.blocks[2].move(dx,dy)
        self.blocks[3].move(dx,dy)

    def get_blocks(self):
        return self.blocks

    def can_move(self,board,dx,dy):
        for block in self.blocks:
            if block.can_move(board,dx,dy)==True:
                continue
            else:
                return False
        return True
        #return a boolean for if the shape can move

    def can_rotate(self,board):
        #check if the shape can be rotated... return true or false
        for block in self.blocks:
            x = self.center_block.p.x - self.rotation_dir*self.center_block.p.y + self.rotation_dir*block.p.y
            y = self.center_block.p.y + self.rotation_dir*self.center_block.p.x- self.rotation_dir*block.p.x
            if board.can_move(x,y) == False:
                return False
            else:
                continue
        return True
        

    def rotate(self,board):
        if self.can_rotate(board) == True:
            for block in self.blocks:
                dx = (self.center_block.p.x - self.rotation_dir*self.center_block.p.y + self.rotation_dir*block.p.y) - (block.p.x)
                dy = (self.center_block.p.y + self.rotation_dir*self.center_block.p.x - self.rotation_dir*block.p.x) - (block.p.y)
                block.move(dx,dy)
        if self.shift_rotation_dir== True:
            self.rotation_dir = (-1)*(self.rotation_dir)

class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x +1   , center.y),
                  Point(center.x + 2, center.y)]
        Shape.__init__(self, coords, "lavender blush")
        self.center_block = self.blocks[1]
        self.rotation_dir = -1
        self.shift_rotation_dir = True

class L_shape(Shape):
    def __init__(self,center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x +1, center.y),
                  Point(center.x + 1, center.y+1)]
        Shape.__init__(self, coords, "purple")
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = False

class J_shape(Shape):
    def __init__(self,center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x -1, center.y+1),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, "pale violet red")
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = False

class O_shape(Shape):
    def __init__(self,center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x -1, center.y+1),
                  Point(center.x, center.y+1)]
        Shape.__init__(self, coords, "maroon")
        self.center_block = self.blocks[1]
    def rotate(self,board):
        return

class Z_shape(Shape):
    def __init__(self,center):
        coords = [Point(center.x - 1, center.y+1),
                  Point(center.x, center.y),
                  Point(center.x , center.y+1),
                  Point(center.x+1, center.y)]
        Shape.__init__(self, coords, "dark sea green")
        self.center_block = self.blocks[2]
        self.shift_rotation_dir = True

class T_shape(Shape):
    def __init__(self,center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x , center.y+1),
                  Point(center.x+1, center.y)]
        Shape.__init__(self, coords, "dark olive green")
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = False

class S_shape(Shape):
    def __init__(self,center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x , center.y+1),
                  Point(center.x+1, center.y+1)]
        Shape.__init__(self, coords, "cadetblue")
        self.center_block = self.blocks[2]
        self.shift_rotation_dir = True

class Board (object):
    def __init__(self,win,width,height):
        self.width = width
        self.height = height
        #create a canvas to draw the shapes on
        self.canvas = CanvasFrame(win,self.width *30, self.height*30)
        self.canvas.setBackground('midnight blue')
        self.grid = {}

        self.f=Text(Point(150,150),"Paused. \nPress p to unpause.")
        self.f.setTextColor("white")
        self.f.setFace("times roman")
        self.f.setSize(12)
        self.f.setStyle("bold")
        self.g=Rectangle(Point(50,100),Point(250,200))
        self.g.setFill("gray14")

    def draw_shape(self,shape):
        #draws the shape on the board if there is room for it
        #returns true of false whether or not the shape can be drawn
        if shape.can_move(self,0,0) == True:
            shape.draw(self.canvas)
            return True
        elif shape.can_move(self,0,0)== False:
            return False
        
    def can_move(self,x,y):
        if not (0<=x<=9 and 0<=y<=19):
            return False
        elif(x,y) in self.grid:
            return False
        else:
            return True 
        #check if it is okay to move a square
        #Already a block in that position or off the board?
    
    def add_shape(self,shape):
        #add a shape to the grid using the coordinates in the dictionary key
        #use get_blocks method on Shape
        x=shape.get_blocks()
        for block in x:
            self.grid[(block.p.x,block.p.y)]=block

    def delete_row(self,y):
        x=0
        while x<=9:
            self.grid[(x,y)].undraw()
            del self.grid[(x,y)]
            x+=1
        #delete all of the blocks in row y from the grid and them erase them 

    def is_row_complete(self,y):
        #check if the squares in row y are occupied, return either true or false
        x=0
        while x<=9:
            if (x,y) in self.grid.keys():
                x+=1
            else:
                return False
        return True

    def move_down_rows(self,y_start):
        x=0
        y=0
        for x in range(0,10):
            for y in range(y_start,0,-1):
                if (x,y) in self.grid.keys():
                    block=self.grid[(x,y)]
                    block.move(0,1)
                    del self.grid[(x,y)]
                    self.grid[(block.p.x,block.p.y)]=block

    def remove_complete_rows(self):
        y=0
        num_complete = 0
        while y<=19:
            if self.is_row_complete(y) == True:
                self.delete_row(y)
                self.move_down_rows(y)
                y+=1
                num_complete +=1
            else:
                y+=1
        return num_complete
        #removes all ofthe complete rows and all rows above down

    def game_over(self):
            x=Text(Point(75,75),"Game over!")
            x.setTextColor("white")
            x.setFace("times roman")
            x.setSize(12)
            x.setStyle("bold")
            x.draw(self.canvas)
        #display Game Over! if the game is done

    def pause(self):
        #draws pause message on board
        self.g.draw(self.canvas)
        self.f.draw(self.canvas)

    def unpause(self):
        self.f.undraw()
        self.g.undraw()

class ScoreBoard(object):
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        #create a canvas to keep score on
        self.canvas = CanvasFrame(win, self.width*30, self.height*30)
        self.canvas.setBackground('midnight blue')
        self.old = Rectangle(Point(70,40), Point(140,60))
        self.score = 0
        self.show_new_score(0)

    def get_new_score(self, num_complete):
        #calculate new score
        if num_complete < 4:
            self.score += num_complete * 100
        else:
            self.score += num_complete * 200

    def show_new_score(self, num_complete):
        #get new score, then display it
        self.old.undraw()
        self.get_new_score(num_complete)
        x=Text(Point(75,50), str(self.score))
        x.setTextColor("white")
        x.setFace("times roman")
        x.setSize(50)
        x.setStyle("bold")
        x.draw(self.canvas)
        self.old = x

    def new_time(self, curr_delay):
        #determines new speed of drop and returns
        if curr_delay > 50:
            x = self.score%500
            if x == 0:
                x = self.score/500
                new_time = 1000 - x*50
                return new_time
        else:
            return 50
        return curr_delay
        

            
class WTPTetris(object):
    SHAPES = [I_shape, J_shape,L_shape,O_shape,S_shape,T_shape,Z_shape]
    DIRECTION = {"Left" :(-1,0), "Right":(1,0),"Down":(0,1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    ''' introduce toggle boolean for pause, might want to wrap the other keys in that boolean thing
        (maybe not, just chck within p), then check for 'p' in key part, make new moethod that pauses (add message,
        stop moving, stop rotation), make new unpause method for starting animation and stuff '''

    def __init__(self,win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.scoreboard = ScoreBoard(win, self.BOARD_WIDTH, 4)
        self.win = win
        self.pausebool = False
        self.delay = 1000
        self.win.bind_all("<Key>", self.key_pressed)
        self.current_shape = self.create_new_shape()
        self.board.draw_shape(self.current_shape)
        self.animate_shape()
        #draw the current shape on the board and animate the shape

    def animate_shape(self):
        if self.pausebool == False:
            self.do_move("Down")
            win.after(self.delay,self.animate_shape)
        else:
            win.after(self.delay, self.animate_shape)
            #move the shape down at equal intervals, specified by the instance variable

    def create_new_shape(self):
        new_shape_class = self.SHAPES[randint(0,6)]
        new_shape = new_shape_class(Point(5,0))
        return new_shape                       
        #create new shape that is centered at the top of the board
        #Return value = shape

    def do_move(self,direction):
##        direction= string
        #use other function to check if it can move
        #then move it &return true
        #if not
        #add current shape, remove completed rows, create new shape and set current shape
        #check game over
        x= direction
        if self.pausebool == False:
            if x == "Down" or x=="Right" or x == "Left":
                dx= (self.DIRECTION[x])[0]
                dy=(self.DIRECTION[x])[1]
                if self.current_shape.can_move(self.board,dx,dy)==True:
                    self.current_shape.move(dx,dy)
                    return True
                elif (x == "Down") and (self.current_shape.can_move(self.board,dx,dy) == False):
                    self.board.add_shape(self.current_shape)
                    num_complete = self.board.remove_complete_rows()
                    self.scoreboard.show_new_score(num_complete)
                    self.delay = self.scoreboard.new_time(self.delay)
                    self.current_shape=self.create_new_shape()
                    h=self.board.draw_shape(self.current_shape)
                    if h==False:
                        self.board.game_over()
                        return "game over"
                    return False

    def do_rotate(self):
        #check if current shape can rotate and does if can
        if self.current_shape.can_rotate(self.board) & self.pausebool==False:
            self.current_shape.rotate(self.board)
            return True
        else:
            return False

    def key_pressed(self,event):
        #space bar moves it down till it cant move anymore
        #up key rotates
        key=event.keysym
        if key == "space":
            while self.do_move("Down")==True:
                continue
        elif key == "Down" or key=="Right" or key == "Left":
            self.do_move(key)
        elif key == 'Up':
            self.do_rotate()
        elif key == 'p' or 'P':
            if self.pausebool == False:
                self.do_pause()
            else:
                self.do_unpause()

    def do_pause(self):
        self.pausebool= True
        self.board.pause()
        
    def do_unpause(self):
        self.pausebool= False
        self.board.unpause()
        
win= Window("WTP Tetris")
game= WTPTetris(win)
win.mainloop()
            
