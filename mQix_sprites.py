import pygame as pg
import random
import math

class Board(pg.sprite.Sprite):
    def __init__(self, size, colour, position):

        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((size,size))
        self.image = self.image.convert()
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.rect.left = position[0]
        self.rect.top = position[1]

        self.left = position[0]
        self.top = position[1]
        self.size = size

        self.fillPercent = 0
    
    # Returns the (x,y) position based on a given logical position
    def getVisualPosition(self, position):
        return (position[0]+self.rect.left, position[1]+self.rect.top)
    
    # Returns the (x,y) logical position based on an actual position
    def getLogicPosition(self, position):
        return (position[0]-self.rect.left, position[1]-self.rect.top)

class Qix(pg.sprite.Sprite):
    def __init__(self, board, radius, speed=0.7):
        pg.sprite.Sprite.__init__(self)

        self.board = board
        # boundaries
        self.lb = board.rect.left
        self.rb = board.rect.right
        self.tb = board.rect.top
        self.bb = board.rect.bottom

        #self.image = pg.Surface((100,100))
        #self.image = self.image.convert()
        #self.image.fill((255,0,255))

        self.radius = radius
        self.image = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        pg.draw.circle(self.image, (255,0,255), (radius, radius), radius)
        #self.image = self.image.convert()

        self.rect = self.image.get_rect()
        self.rect.center = board.rect.center

        self.speed = speed
        self.dir = self.getRandomDir((-90,90), (-90,90))

    
    def getRandomDir(self, xDegs, yDegs):
        randX = random.randint(xDegs[0], xDegs[1])
        randY = random.randint(yDegs[0], yDegs[1])

        theta = math.atan2(randY, randX)
        #print(theta)
        #print(self.speed*math.cos(theta), self.speed*math.sin(theta))
        
        return (self.speed*math.cos(theta), self.speed*math.sin(theta))
    
    def update(self):
        self.rect.centerx+=self.dir[0]
        self.rect.centery+=self.dir[1]

        if self.rect.left < self.lb:
            self.rect.left = self.lb + 5
            self.dir = self.getRandomDir((0, 90), (-90, 90))
        elif self.rect.right > self.rb:
            self.rect.right = self.rb - 5
            self.dir = self.getRandomDir((-90, 0), (-90, 90))
        if self.rect.top < self.tb:
            self.rect.top = self.tb + 5
            self.dir = self.getRandomDir((-90, 90), (0, 90))
        elif self.rect.bottom > self.bb:
            self.rect.bottom = self.bb - 5
            self.dir = self.getRandomDir((-90,90), (-90,0))


class Sparc(pg.sprite.Sprite):
    def __init__(self, player, board, logic, position, prev, colour):
        pg.sprite.Sprite.__init__(self)

        self.board = board
        self.logic = logic
        self.player = player

        self.image = pg.Surface((5,5))
        self.image = self.image.convert()
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.setPos(position)

        self.prev = prev
        self.curr = logic[position[1]][position[0]]

    def update(self):
        if self.curr.state != 1:
            if self.player.push is False:
                border = self.buildBorder(self.logic[self.player.getLogicPosition()[1]][self.player.getLogicPosition()[0]])
            else:
                # don't think this ever happens but it's fine to just leave ig
                border = self.buildBorder(self.player.push[0])
            
            self.curr = border[random.randint(0, len(border)-1)]
            for space in map(lambda x: x[0], self.curr.adjacents):
                if space.state == 1:
                    self.prev = space
                    break
            self.setPos(self.curr.position)
            
            return


        for space in map(lambda x: x[0], self.curr.adjacents):
            if (space.state == 1 or space.state == 2) and space != self.prev:
                self.setPos(space.position)
                self.prev = self.curr
                self.curr = space
                break
    
    def buildBorder(self, start):
        prev = start
        for space in map(lambda x: x[0], prev.adjacents):
            if space.state == 1:
                curr = space
                break
        path = [start, curr]

        while True:
            for space in map(lambda x: x[0], curr.adjacents):
                if space == start:
                    return path
                elif space.state == 1 and space != prev:
                    path.append(space)
                    prev = curr
                    curr = space
                    break
    
    def getLogicPosition(self):
        return self.board.getLogicPosition((self.rect.centerx, self.rect.centery))
    
    def setPos(self, position):
        self.rect.centerx, self.rect.centery = self.board.getVisualPosition(position)

class Player(pg.sprite.Sprite):
    def __init__(self, board, position, logic):
        pg.sprite.Sprite.__init__(self)

        self.board = board
        self.logic = logic

        self.image = pg.Surface((5,5))
        self.image = self.image.convert()
        self.image.fill((255,0,0))

        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

        self.dir = (0,1)
        self.bleft = position[0]
        self.btop = position[1]

        self.push = False # either false or a list containing spaces travelled upon while in a push

    def update(self):
        dx = self.dir[0]
        dy = self.dir[1]
        if dy == 0:
            # if movement is occuring in the x-axis
            if not ((self.rect.centerx == self.bleft and dx < 0) or (self.rect.centerx == (self.bleft+self.board.size-1) and dx > 0)):
                if self.push or self.nextPosValid(dx, dy):
                    self.rect.centerx += dx
                    if self.push:
                        x, y = self.getLogicPosition()
                        self.push.append(self.logic[y][x])
        else:
            # if movement is occuring in the y=axis
            if not ((self.rect.centery == self.btop and dy < 0) or (self.rect.centery == (self.btop+self.board.size-1) and dy > 0)):
                if self.push or self.nextPosValid(dx, dy):
                    self.rect.centery += dy
                    if self.push:
                        x, y = self.getLogicPosition()
                        self.push.append(self.logic[y][x])
    
    def nextPosValid(self, dx, dy):
        xPos, yPos = self.getLogicPosition()
        return self.logic[yPos+dy][xPos+dx].state == 1 or self.logic[yPos+dy][xPos+dx].state == 2

    def getLogicPosition(self):
        return (self.rect.centerx-self.bleft, self.rect.centery-self.btop)
        #return [[y, x] for x in range(self.rect.left-self.bleft, self.rect.right-self.bleft) for y in range(self.rect.top-self.btop, self.rect.bottom-self.btop)]
    def setLogicPosition(self, position):
        self.rect.centerx = position[0]+self.bleft
        self.rect.centery = position[1]+self.btop

class PlayerVisual(pg.sprite.Sprite):
    def __init__(self, player, size, colour):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((size,size))
        self.image = self.image.convert()
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery

        self.player = player

    def update(self):
        self.rect.centerx = self.player.rect.centerx
        self.rect.centery = self.player.rect.centery

class Button(pg.sprite.Sprite):
    def __init__(self, position, size, defaultColour, activeColour, clickVal):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((size[0], size[1]))
        self.image = self.image.convert()
        self.image.fill(defaultColour)

        self.rect = self.image.get_rect()
        self.rect.left = position[0]
        self.rect.top = position[1]

        self.defaultColour = defaultColour
        self.activeColour = activeColour
        self.clickVal = clickVal

        self.hovered = False
    
    def update(self):
        if self.hovered:
            self.image.fill(self.activeColour)
        else:
            self.image.fill(self.defaultColour)

class Cursor(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((1,1))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pg.mouse.get_pos()

class BoardSpace():
    def __init__(self, position):
        self.position = position    # (x,y) position on the board

        self.adjacents = []         # a list containing all the spaces that it's adjacent to
                                    # each element is of the form [Space, (dir of space: x, y)]
        self.state = 0              # current space state
                                    # states: 0=empty space, 1=border, 2=active border, 3=filled, 4=old border (not implemented cause I'm bad)
    
    def initSides(self, adjacents):
        self.adjacents = adjacents
    
    def print(self):
        return f"Position: {self.position},\tAdjacent List: {self.adjacents}"
    
    def __eq__(self, other):
        return isinstance(other, BoardSpace) and self.position == other.position
    
    def __str__(self):
        return "x: {}, y: {}".format(self.position[0], self.position[1])

    """def copy(self):
        copy = type(self)(self.position)
        copy.adjacents = self.adjacents
        copy.state = self.state
        return copy"""

class TextDisplay(pg.sprite.Sprite):
    # position is a tuple ("left" or "center", (x,y))
    def __init__(self, position, font, fontSize, colour, text = ""):
        pg.sprite.Sprite.__init__(self)

        if position[0] == "center":
            self.center = position[1]
            self.mode = "center"
        elif position[0] == "left":
            self.left = position[1][0]
            self.top = position[1][1]
            self.mode = "left"
        else:
            print("Error. Invalid position mode.")
        
        self.font = pg.font.SysFont(font, fontSize)
        self.text = text
        self.colour = colour
    
    def setText(self, text):
        self.text = text
    
    def update(self):
        self.image = self.font.render(self.text, True, self.colour)
        self.rect = self.image.get_rect()

        if self.mode == "center":
            self.rect.center = self.center
        elif self.mode == "left":
            self.rect.left = self.left
            self.rect.top = self.top

class TitleDisplay(pg.sprite.Sprite):
    # position is a tuple ("left" or "center", (x,y))
    def __init__(self, screen, diff):
        pg.sprite.Sprite.__init__(self)
        
        self.screen = screen

        font = pg.font.SysFont("Arial", 120)
        self.image = font.render("mQix", True, (255,0,0))

        self.rect = self.image.get_rect()
        self.rect.centery = 250
        self.rect.right = 0

        self.maxVal = screen.get_width()
        self.spawnDiff = diff

        self.spawnNew = False
    
    def update(self):
        self.rect.centerx+=1
        if self.rect.left > self.spawnDiff:
            self.spawnNew = True
        if self.rect.left > self.maxVal:
            self.kill()


