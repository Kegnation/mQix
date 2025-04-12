import pygame as pg
import numpy as np
import random
import time
import mQix_sprites as sprites

pg.init()
pg.mixer.init()

# Global vars
FRAME_RATE = 90
BOARD_SIZE = 400
STARTING_HP = 5

DECIMAL_C_L = {
    "BLACK": 0,
    "WHITE": 16777215,
    "GREEN": 65280,
    "RED": 16711680,
    "DARK RED": 13123648,
    "DARK GREEN": 26112
}
STATE_C_L = {
    0: DECIMAL_C_L["BLACK"],
    1: DECIMAL_C_L["GREEN"],
    2: DECIMAL_C_L["RED"],
    3: DECIMAL_C_L["DARK RED"],
    4: DECIMAL_C_L["DARK GREEN"]
}
RGB_C_L = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREY":  (125, 125, 125),
    "RED":   (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE":  (0, 0, 255),
    "DARK PURPLE": (153, 51, 255),
    "HAZY PINK": (255, 102, 255),
    "HAZY BLUE": (0, 128, 255),
    "HAZY LIGHT BLUE": (51, 153, 255),
    "HAZY ORANGE": (255, 128, 0),
    "HAZY LIGHT ORANGE": (255, 153, 51),
    "LIGHT GREY": (192, 192, 192),
    "HAZY LIGHT GREY": (244, 244, 244),
    "LIGHT GREEN": (178, 255, 102),
    "HAZY LIGHT GREEN": (204, 255, 153),
    "LIGHT RED": (255, 102, 102),
    "HAZY LIGHT RED": (255, 153, 153)
}

def menuScreen(screen, clock, sounds):
    
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(RGB_C_L["BLACK"])

    # mQix is hard-coded a y level of 250
    pg.draw.line(background, RGB_C_L["WHITE"], (0, 170), (screen.get_width(), 170), 5)
    pg.draw.line(background, RGB_C_L["WHITE"], (0, 330), (screen.get_width(), 330), 5)

    spawnDiff = 25
    # has an x-length of 275
    mQix = [sprites.TitleDisplay(screen, spawnDiff)]

    midpoint = screen.get_width()//2
    playButton = sprites.Button((midpoint-250/2, 360), (250, 90), RGB_C_L["LIGHT GREEN"], RGB_C_L["HAZY LIGHT GREEN"], "play")
    playLabel = sprites.TextDisplay(("center", playButton.rect.center), "Arial", 50, RGB_C_L["BLACK"], "Play!")
    settingsButton = sprites.Button((midpoint-250/2, 465), (250, 90), RGB_C_L["LIGHT GREY"], RGB_C_L["HAZY LIGHT GREY"], "settings")
    settingsLabel = sprites.TextDisplay(("center", settingsButton.rect.center), "Arial", 50, RGB_C_L["BLACK"], "Settings")
    quitButton = sprites.Button((midpoint-250/2, 570), (250, 90), RGB_C_L["LIGHT RED"], RGB_C_L["HAZY LIGHT RED"], "quit")
    quitLabel = sprites.TextDisplay(("center", quitButton.rect.center), "Arial", 50, RGB_C_L["BLACK"], "Quit")

    buttons = [playButton, settingsButton, quitButton]
    labels = [playLabel, settingsLabel, quitLabel]

    cursor = sprites.Cursor()

    allSprites = pg.sprite.OrderedUpdates(mQix, buttons, labels, cursor)

    while True:
        clock.tick(FRAME_RATE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return "quit"
            elif event.type == pg.MOUSEBUTTONDOWN:
                for button in buttons:
                    if cursor.rect.colliderect(button.rect):
                        sounds["clickButton"].play()
                        return button.clickVal
                sounds["click"].play()

        if mQix[-1].spawnNew == True:
            mQix.append(sprites.TitleDisplay(screen, spawnDiff))
            allSprites = pg.sprite.OrderedUpdates(mQix, buttons, labels, cursor)

        for button in buttons:
            if cursor.rect.colliderect(button):
                button.hovered = True
            else:
                button.hovered = False

        allSprites.clear(screen, background)
        screen.blit(background, (0,0))
        allSprites.update()
        allSprites.draw(screen)

        pg.display.flip()

def settingScreen(screen, clock, sounds):
    global BOARD_SIZE
    global FRAME_RATE

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(RGB_C_L["BLACK"])

    backButton = sprites.Button((20, 20), (140, 70), RGB_C_L["LIGHT RED"], RGB_C_L["HAZY LIGHT RED"], "menu")
    backLabel = sprites.TextDisplay(("center", backButton.rect.center), "Arial", 40, RGB_C_L["BLACK"], "Back")

    buttonSize = 40
    leftOffset = 45
    topOffset = 50
    buttonDiff = 20

    offset = 180
    boardSizeLabel = sprites.TextDisplay(("left", (20, offset)), "Arial", 45, RGB_C_L["WHITE"], "Board Size: {}".format(BOARD_SIZE))
    boardSizeDec = sprites.Button((20+leftOffset, offset+topOffset), (buttonSize, buttonSize), \
                                  RGB_C_L["LIGHT RED"], RGB_C_L["HAZY LIGHT RED"], -50)
    boardSizeInc = sprites.Button((boardSizeDec.rect.right+buttonDiff, offset+topOffset), (buttonSize, buttonSize), \
                                  RGB_C_L["LIGHT GREEN"], RGB_C_L["HAZY LIGHT GREEN"], 50)
    boardSizeButtons = [boardSizeInc, boardSizeDec]
    bsDecLabel = sprites.TextDisplay(("center", boardSizeDec.rect.center), "Arial", 30, RGB_C_L["BLACK"], "-")
    bsIncLabel = sprites.TextDisplay(("center", boardSizeInc.rect.center), "Arial", 30, RGB_C_L["BLACK"], "+")

    offset = 300
    gameSpeedLabel = sprites.TextDisplay(("left", (20, offset)), "Arial", 45, RGB_C_L["WHITE"], "Game Speed (fps): {}".format(FRAME_RATE))
    gameSpeedDec = sprites.Button((20+leftOffset, offset+topOffset), (buttonSize, buttonSize), \
                                  RGB_C_L["LIGHT RED"], RGB_C_L["HAZY LIGHT RED"], -10)
    gameSpeedInc = sprites.Button((gameSpeedDec.rect.right+buttonDiff, offset+topOffset), (buttonSize, buttonSize), \
                                  RGB_C_L["LIGHT GREEN"], RGB_C_L["HAZY LIGHT GREEN"], 10)
    gameSpeedButtons = [gameSpeedInc, gameSpeedDec]
    gsDecLabel = sprites.TextDisplay(("center", gameSpeedDec.rect.center), "Arial", 30, RGB_C_L["BLACK"], "-")
    gsIncLabel = sprites.TextDisplay(("center", gameSpeedInc.rect.center), "Arial", 30, RGB_C_L["BLACK"], "+")

    buttons = [backButton, *boardSizeButtons, *gameSpeedButtons]
    labels = [backLabel, boardSizeLabel, bsDecLabel, bsIncLabel, gameSpeedLabel, gsDecLabel, gsIncLabel]

    cursor = sprites.Cursor()

    allSprites = pg.sprite.OrderedUpdates(buttons, labels, cursor)

    while True:
        clock.tick(FRAME_RATE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "menu"
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return "menu"
            elif event.type == pg.MOUSEBUTTONDOWN:
                for button in buttons:
                    if not cursor.rect.colliderect(button.rect):
                        sounds["click"].play()
                        continue

                    sounds["clickButton"].play()
                    if button == backButton:
                        return button.clickVal
                    elif button in boardSizeButtons:
                        if BOARD_SIZE+button.clickVal > 0 and BOARD_SIZE+button.clickVal <= 450:
                            BOARD_SIZE+=button.clickVal
                            boardSizeLabel.setText("Board Size: {}".format(BOARD_SIZE))
                    elif button in gameSpeedButtons:
                        if FRAME_RATE+button.clickVal > 0:
                            FRAME_RATE+=button.clickVal
                            gameSpeedLabel.setText("Game Speed (fps): {}".format(FRAME_RATE))
        
        for button in buttons:
            if cursor.rect.colliderect(button):
                button.hovered = True
            else:
                button.hovered = False
        
        allSprites.clear(screen, background)
        screen.blit(background, (0,0))
        allSprites.update()
        allSprites.draw(screen)

        pg.display.flip()

def createBackground(screen):
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(RGB_C_L["BLACK"])

    #                                           800x700
    pg.draw.rect(background, RGB_C_L["BLUE"], ((150, 250), (500, 260)), 3, 10)

    return background

def resultScreen(screen, clock, sounds, level, qixSpeed, sparxNum):
    
    background = createBackground(screen)
    screen.blit(background, (0,0))

    midpoint = screen.get_width()//2
    yOffset = 315
    yDiff = 60
    titleLabel = sprites.TextDisplay(("center", (midpoint, 190)), "Arial", 70, RGB_C_L["RED"], "Game Over")
    levelLabel = sprites.TextDisplay(("center", (midpoint, yOffset+yDiff*0)), "Arial", 40, RGB_C_L["GREEN"], "Level: {}".format(level))
    qixSpeedLabel = sprites.TextDisplay(("center", (midpoint, yOffset+yDiff*1)), "Arial", 40, RGB_C_L["GREEN"], "Qix Speed: {}".format(qixSpeed))
    sparxNumLabel = sprites.TextDisplay(("center", (midpoint, yOffset+yDiff*2)), "Arial", 40, RGB_C_L["GREEN"], "Number of Sparx: {}".format(sparxNum))

    menuButton = sprites.Button((15, 620), (180, 60), RGB_C_L["HAZY BLUE"], RGB_C_L["HAZY LIGHT BLUE"], "menu")
    menuLabel = sprites.TextDisplay(("center", menuButton.rect.center), "Arial", 30, RGB_C_L["BLACK"], "Menu")
    playAgainButton = sprites.Button((605, 620), (180, 60), RGB_C_L["HAZY ORANGE"], RGB_C_L["HAZY LIGHT ORANGE"], "play")
    playAgainLabel = sprites.TextDisplay(("center", playAgainButton.rect.center), "Arial", 30, RGB_C_L["BLACK"], "Play Again")

    buttons = [menuButton, playAgainButton]
    buttonGroup = pg.sprite.OrderedUpdates(menuButton, playAgainButton)

    cursor = sprites.Cursor()

    textGroup = pg.sprite.OrderedUpdates(titleLabel, levelLabel, qixSpeedLabel, sparxNumLabel, menuLabel, playAgainLabel)
    allSprites = pg.sprite.OrderedUpdates(buttonGroup, textGroup, cursor)

    while True:
        clock.tick(FRAME_RATE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "menu"
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return "menu"
            elif event.type == pg.MOUSEBUTTONDOWN:
                for button in buttons:
                    if cursor.rect.colliderect(button.rect):
                        sounds["clickButton"].play()
                        return button.clickVal
                sounds["click"].play()
        
        for button in buttons:
            if cursor.rect.colliderect(button):
                button.hovered = True
            else:
                button.hovered = False
        

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pg.display.flip()

def initSpaces(logic):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            space = logic[y][x]
            space.position = [x,y]

            # top check
            if y>0:
                space.adjacents.append([logic[y-1][x], (0,-1)])
            # left check
            if x>0:
                space.adjacents.append([logic[y][x-1], (-1,0)])
            # bottom check
            if y<BOARD_SIZE-1:
                space.adjacents.append([logic[y+1][x], (0,1)])
            if x<BOARD_SIZE-1:
                space.adjacents.append([logic[y][x+1], (1,0)])
            
            # set initial border
            if x == 0 or x == BOARD_SIZE-1 or y == 0 or y == BOARD_SIZE-1:
                space.state = 1
            
            """if (y == 100 and x in myRange) or (x == 100 and y in myRange) \
                or (y == 200 and x in myRange) or (x == 200 and y in myRange):
                space.state = 2"""

def pushStart(player, logic):
    x, y = player.getLogicPosition()
    adjs = map(lambda x: x[0], logic[y][x].adjacents)
    for pos, space in enumerate(adjs):
        if space.state == 0:
            player.dir = logic[y][x].adjacents[pos][1]
            player.push = [logic[y][x]]
            logic[y][x].state = 2
            return True
    
    return False

def pushEnd(visual, logic, player, board, success, label, sounds):
    if success:
        validEnd(player, logic, board, label, sounds)
    else:
        invalidEnd(player)

    updateVisual(visual, logic)

def invalidEnd(player):
    pushPath = player.push

    for space in pushPath:
        space.state = 0
    
    pushPath[0].state = 1
    player.setLogicPosition(pushPath[0].position)

    player.push = False

def buildBorder(prev, curr):
    path = [curr]

    valid = True
    while valid:
        for space in map(lambda x: x[0], curr.adjacents):
            if space.state == 1 and space != prev:
                path.append(space)
                prev = curr
                curr = space
                break
            elif space.state == 2:
                valid = False
    
    return path

def swapAlongPath(path, newState):
    for space in path:
        space.state = newState

def validEnd(player, logic, board, label, sounds):
    pushPath = player.push

    paths = []
    for space in map(lambda x: x[0], pushPath[-1].adjacents):
        if space.state == 1:
            paths.append(buildBorder(pushPath[-1], space))
    
    swapAlongPath(paths[0], 2)
    path1Count = scanlineFill(logic, "COUNT")
    swapAlongPath(paths[0], 1)

    swapAlongPath(paths[1], 2)
    path2Count = scanlineFill(logic, "COUNT")
    swapAlongPath(paths[1], 1)

    if path1Count < path2Count:
        swapAlongPath(paths[0], 2)
        scanlineFill(logic, "FILL")
        swapAlongPath(paths[0], 3)
        swapAlongPath(pushPath, 1)
    else:
        swapAlongPath(paths[1], 2)
        scanlineFill(logic, "FILL")
        swapAlongPath(paths[1], 3)
        swapAlongPath(pushPath, 1)

    scanlineFill(logic, "FILL")
    swapPushStates(pushPath, logic)

    board.fillPercent = getFillPercent(logic)

    label.setText(str(round(board.fillPercent, 2))+"%")
    sounds["fill"].play()

    player.push = False

def scanlineFill(logic, mode):
    fillSpaces = []

    for row in logic:
        toggle = row[0].state == 2
        lineFlag = False
        tmp = []
        prev = row[0]
        for space in row[1:]:
            if space.state == 2 and prev.state != 2:
                toggle = not toggle
                fillSpaces.extend(tmp)
                tmp = []
            elif space.state == 2 and prev.state == 2:
                lineFlag = True
            elif space.state == 0 and lineFlag:
                for tmpSpace in map(lambda x: x[0], space.adjacents):
                    if tmpSpace in fillSpaces:
                        toggle = True
                        tmp.append(space)
                        break
                    else:
                        toggle = False
                lineFlag = False
            elif toggle and space.state == 0:
                tmp.append(space)
            prev = space
    
    if mode == "FILL":
        for space in fillSpaces:
            space.state = 2
    elif mode == "COUNT":
        count = 0
        for space in fillSpaces:
            count+=1
        return count
    else:
        print("Bad ScanlineFill Mode")

def swapPushStates(pushPath, logic):
    for row in logic:
        for space in row:
            if space.state == 2:
                space.state = 3
    
    for space in pushPath:
        space.state = 1

def updateVisual(visual, logic):
    for y, row in enumerate(logic):
        for x, space in enumerate(row):
            visual[y][x] =  STATE_C_L[space.state]

def getFillPercent(logic):
    count = 0
    for row in logic:
        for space in row:
            if space.state == 3:
                count+=1
    
    return count/(BOARD_SIZE**2)*100

def gameScreen(screen, clock, sounds, level, qixSpeed, numSparx):
    gameVisual = None
    gameLogic = [[sprites.BoardSpace((x,y)) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
    initSpaces(gameLogic)

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(RGB_C_L["GREY"])
    screen.blit(background, (0,0))
    
    board = sprites.Board(BOARD_SIZE, RGB_C_L["GREY"], ((screen.get_width()-BOARD_SIZE)//2, (screen.get_height()-BOARD_SIZE)//2))
    gameVisual = [[STATE_C_L[space.state] for space in row] for row in gameLogic]
    
    player = sprites.Player(board, ((screen.get_width()-BOARD_SIZE)//2, (screen.get_height()-BOARD_SIZE)//2), gameLogic)
    playerVisual = sprites.PlayerVisual(player, 5, RGB_C_L["RED"])
    hp = STARTING_HP

    sparx = []
    for i in range(numSparx):
        rand = random.randint(0,BOARD_SIZE-1)
        if i % 2 == 0:
            position = (rand, BOARD_SIZE-1)
        else:
            position = (BOARD_SIZE-1, rand)
        
        for space in map(lambda x: x[0], gameLogic[position[1]][position[0]].adjacents):
            if space.state == 1:
                prev = space
                break
    
        sparx.append(sprites.Sparc(player, board, gameLogic, position, prev, RGB_C_L["HAZY PINK"]))
    
    sparxGroup = pg.sprite.OrderedUpdates(sparx)
    qix = sprites.Qix(board, 25, qixSpeed)
    qixGroup = pg.sprite.OrderedUpdates(qix)
    qixHitFlag = True
    sparxHitFlag = True

    textOffset = 150
    textSpacing = 40
    leftOffset = 10
    percentLabel = sprites.TextDisplay(("center", (screen.get_width()//2, 70)), "Arial", 30, RGB_C_L["BLACK"], "0.00%")
    hpLabel = sprites.TextDisplay(("left", (leftOffset,textOffset+textSpacing*0)), "Arial", 25, RGB_C_L["BLACK"], "HP: {}".format(STARTING_HP))
    levelLabel = sprites.TextDisplay(("left", (leftOffset,textOffset+textSpacing*1)), "Arial", 25, RGB_C_L["BLACK"], "Level: {}".format(level))
    speedLabel = sprites.TextDisplay(("left", (leftOffset,textOffset+textSpacing*2)), "Arial", 25, RGB_C_L["BLACK"], "Qix Speed: {}".format(qixSpeed))
    sparxNumLabel = sprites.TextDisplay(("left", (leftOffset,textOffset+textSpacing*3)), "Arial", 25, RGB_C_L["BLACK"], "# Of Sparx: {}".format(numSparx))

    textGroup = pg.sprite.OrderedUpdates(percentLabel, hpLabel, levelLabel, speedLabel, sparxNumLabel)

    allSprites = pg.sprite.OrderedUpdates(board, textGroup, sparxGroup, player, playerVisual, qixGroup)

    # events
    randQix = pg.USEREVENT + 1
    pg.time.set_timer(randQix, 1000*3)

    # print(pg.PixelArray(board))

    completed = False
    run = True
    while run:
        clock.tick(FRAME_RATE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                # statements for free movement
                if not (event.key == pg.K_q and player.push) and not event.key == pg.K_ESCAPE:
                    sounds["blip"].play()
                if player.push:
                    if event.key == pg.K_w and player.dir[1] == 0:
                        player.dir = (0,-1)
                    elif event.key == pg.K_a and player.dir[0] == 0:
                        player.dir = (-1,0)
                    elif event.key == pg.K_s and player.dir[1] == 0:
                        player.dir = (0,1)
                    elif event.key == pg.K_d and player.dir[0] == 0:
                        player.dir = (1,0)
                else:
                    if event.key == pg.K_q:
                        pushStart(player, gameLogic)
                    elif event.key == pg.K_w:
                        player.dir = (0,-1)
                    elif event.key == pg.K_a:
                        player.dir = (-1,0)
                    elif event.key == pg.K_s:
                        player.dir = (0,1)
                    elif event.key == pg.K_d:
                        player.dir = (1,0)
            elif event.type == randQix:
                qix.dir = qix.getRandomDir((-90,90), (-90,90))


        xPos, yPos = player.getLogicPosition()
        currSpace = gameLogic[yPos][xPos]
        if player.push:
            failFlag = False
            for sparc in sparx:
                x, y = sparc.getLogicPosition()
                if gameLogic[y][x] == player.push[0]:
                    pushEnd(gameVisual, gameLogic, player, board, False, None, sounds)
                    failFlag = True
                    break

            if failFlag:
                pass
            elif currSpace.state == 1:
                pushEnd(gameVisual, gameLogic, player, board, True, percentLabel, sounds)
            elif currSpace.state == 2 and len(player.push) != 1:
                pushEnd(gameVisual, gameLogic, player, board, False, None, sounds)
            else:
                currSpace.state = 2
        #print(gameLogic[yPos][xPos].print())
        gameVisual[yPos][xPos] = STATE_C_L[gameLogic[yPos][xPos].state]

        # COLLISIONS
        if pg.sprite.spritecollide(player, sparxGroup, False):
            if sparxHitFlag:
                hp -= 1
                sounds["damage"].play()
                hpLabel.setText("HP: {}".format(hp))
                sparxHitFlag = False
        else:
            sparxHitFlag = True
        if pg.sprite.spritecollide(player, qixGroup, False) and gameLogic[yPos][xPos].state != 1:
            if qixHitFlag:
                hp -= 1
                sounds["damage"].play()
                hpLabel.setText("HP: {}".format(hp))
                qixHitFlag = False
        else:
            qixHitFlag = True

        if hp <= 0:
            run = False
        if board.fillPercent >= 60:
            run = False
            completed = True

        #print(board.getLogicPosition(sparc1.position))
        #print(sparc1.curr.adjacents)
        
        pg.surfarray.blit_array(board.image, np.transpose(gameVisual))
        
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pg.display.flip()
    
    return level, qixSpeed, numSparx, completed


def main():
    screen = pg.display.set_mode((800,700))
    pg.display.set_caption("mQix")
    clock = pg.time.Clock()

    level, qixSpeed, sparxNum = 1, 2, 1

    sounds = {"click": pg.mixer.Sound("click.wav"),
              "clickButton": pg.mixer.Sound("clickButton.wav"),
              "blip": pg.mixer.Sound("blip.mp3"),
              "damage": pg.mixer.Sound("damage.mp3"),
              "fill": pg.mixer.Sound("fill.mp3"),
              "gameOver": pg.mixer.Sound("gameOver.mp3"),
              "nextLevel": pg.mixer.Sound("nextLevel.mp3"),}

    option = menuScreen(screen, clock, sounds)
    while True:
        if option == "menu":
            option = menuScreen(screen, clock, sounds)
        elif option == "settings":
            option = settingScreen(screen, clock, sounds)
        elif option == "play":
            level, qixSpeed, sparxNum = 1, 2, 1
            winning = True
            while True:
                level, qixSpeed, sparxNum, winning = gameScreen(screen, clock, sounds, level, qixSpeed, sparxNum)
                if not winning:
                    sounds["gameOver"].play()
                    break
                level+=1
                qixSpeed+=1
                if level%2==0:
                    sparxNum+=1
                sounds["nextLevel"].play()
            option = resultScreen(screen, clock, sounds, level, qixSpeed, sparxNum)
        elif option == "quit":
            break
    time.sleep(0.5)

main()
