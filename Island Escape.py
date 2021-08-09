#################################################
# CMU Final Project: Island Escape (a game)
# name: Jack Chang
# andrew id: jackchan
#
#################################################

from cmu_112_graphics import *
import string, math, time
from random import randint



# button class for all buttons
class Button(object):

    def __init__(self, x0, y0, x1, y1, clickEvent, regularFill, hoverFill,
    textColor, outline, text, font, fontSize, bold):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.clickEvent = clickEvent
        self.regularFill = regularFill
        self.textColor = textColor
        self.outline = outline
        self.text = text
        self.font = font
        self.fontSize = fontSize
        self.bold = bold
        self.hoverFill = hoverFill
        self.fill = regularFill
    
    # calculates the actual number values of the bounds of the button
    def getBounds(self, app):
        return (app.width * self.x0, app.height * self.y0, app.width * self.x1,
        app.height * self.y1)
    
    # puts together the string representing the font
    def getFont(self):
        curFont = self.font + " " + str(self.fontSize)
        if self.bold:
            curFont += " bold"
        return curFont



# class to represent all objects on the playing grid
class GridObject(object):

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visible = False



# class that extends GridObject, which has an added attribute chaseType
class Robot(GridObject):

    def __init__(self, row, col, chaseType):
        super().__init__(row, col)
        self.chaseType = chaseType



# initializes the buttons for the title screen and returns them in a list
def initializeTitleScreenButtons(app):
    startButton = Button(2 / 5, 7 / 20, 3 / 5, 9 / 20, "startGame", "red",
        "magenta", "lime", "black", "Start", "Arial", 25, False)
    settingsButton = Button(2 / 5, 31 / 60, 3 / 5, 37 / 60, "settings", "red",
        "magenta", "lime", "black", "Settings", "Arial", 25, False)
    quitButton = Button(2 / 5, 41 / 60, 3 / 5, 47 / 60, "quit", "red",
        "magenta", "lime", "black", "Quit", "Arial", 25, False)
    app.buttons.append(startButton)
    app.buttons.append(settingsButton)
    app.buttons.append(quitButton)

# initializes the buttons for the settings screen and returns them in a list
def initializeSettingsScreenButtons(app):
    return []

# initializes the buttons for the level select screen and returns them in a list
def initializeLevelSelectScreenButtons(app):
    for i in range (2):
        for j in range (3):
            curLevel = i * 3 + j + 1
            if curLevel in app.levelsUnlocked:
                curButton = Button((j * 2 + 1) / 7, 3 / 10 + i * 2 / 7,
                    (j + 1) * 2 / 7, 3 / 10 + (i * 2 + 1) / 7,
                    f"level{curLevel}", "red", "magenta", "lime", "black",
                    f"Level {curLevel}", "Arial", 20, False)
                app.buttons.append(curButton)
            else:
                curButton = Button((j * 2 + 1) / 7, 3 / 10 + i * 2 / 7,
                    (j + 1) * 2 / 7, 3 / 10 + (i * 2 + 1) / 7, None, "black",
                    "black", "lime", "black", "LOCKED", "Arial",
                    20, False)
                app.buttons.append(curButton)
    titleScreenButton = Button(1 / 4, 17 / 20, 3 / 4, 19 / 20, "titleScreen",
        "blue", "aqua", "red", "black", "Return To Title Screen", "Arial",
        25, False)
    app.buttons.append(titleScreenButton)

def initializeLevel1(app):
    app.rows = 6
    app.cols = 6
    app.grid.clear()
    app.robots.clear()
    for i in range (6):
        app.grid.append([])
        for j in range (6):
            app.grid[i].append("empty")
    app.grid[3][3] = "rock"
    app.player = GridObject(0, 0)
    app.exit = GridObject(5, 5)
    app.player.visible = True
    app.exit.visible = True
    robot1 = Robot(0, 5, "follow")
    robot1.visible = True
    app.robots.append(robot1)

def initializeLevel1v2(app):
    app.rows = 12
    app.cols = 12
    app.grid.clear()
    app.robots.clear()
    for i in range (12):
        app.grid.append([])
        for j in range (12):
            app.grid[i].append("empty")
    for i in range (randint(15, 50)):
        row = randint(0, 11)
        col = randint(0, 11)
        if (row == 0 and col == 0) or (row == 11 and col == 11):
            continue
        app.grid[row][col] = "rock"
    app.player = GridObject(0, 0)
    app.exit = GridObject(11, 11)
    app.player.visible = True
    app.exit.visible = True
    robot1 = Robot(randint(7, 10), randint(7, 10), "follow")
    while app.grid[robot1.row][robot1.col] != "empty":
        robot1.row = randint(5, 10)
        robot1.col = randint(5, 10)
    robot1.visible = True
    app.robots.append(robot1)

# switches screens by clearing the current screen and initializing buttons
def switchScreen(app, screen):
    app.mode = screen
    app.buttons.clear()
    if screen == "titleScreen":
        initializeTitleScreenButtons(app)
    elif screen == "settingsScreen":
        initializeSettingsScreenButtons(app)
    elif screen == "levelSelectScreen":
        initializeLevelSelectScreenButtons(app)
    elif screen == "level1":
        #initializeLevel1(app)
        initializeLevel1v2(app)

# checks if the click is within the bounds given
def insideButton(x0, y0, x1, y1, clickX, clickY):
    return clickX >= x0 and clickX <= x1 and clickY >= y0 and clickY <= y1

# loops through each button and checks if that button has been pressed
def checkForButtonPress(app, clickX, clickY):
    for button in app.buttons:
        (x0, y0, x1, y1) = button.getBounds(app)
        if insideButton(x0, y0, x1, y1, clickX, clickY):
            return button.clickEvent

# loops through each button and checks if the mouse if hovering over that button
def checkForButtonHover(app, mouseX, mouseY):
    for button in app.buttons:
        (x0, y0, x1, y1) = button.getBounds(app)
        if insideButton(x0, y0, x1, y1, mouseX, mouseY):
            button.fill = button.hoverFill
            return
        else:
            button.fill = button.regularFill

# gets the shortest path between two objects on a grid, using only empty tiles
def getShortestPath(app, object1, object2):
    x0 = object1.row
    y0 = object1.col
    x1 = object2.row
    y1 = object2.col
    q = [(x0, y0, 0, [])]
    minDist = None
    path = []
    visited = set()
    while len(q) != 0:
        (curX, curY, curDist, curPath) = q.pop(0)
        if not isValidPos(app, curX, curY) or (curX, curY) in visited:
            continue
        visited.add((curX, curY))
        if curX == x1 and curY == y1:
            if minDist == None or curDist < minDist:
                minDist = curDist
                path = curPath
            continue
        q.append((curX + 1, curY, curDist + 1, curPath + [(curX + 1, curY)]))
        q.append((curX - 1, curY, curDist + 1, curPath + [(curX - 1, curY)]))
        q.append((curX, curY + 1, curDist + 1, curPath + [(curX, curY + 1)]))
        q.append((curX, curY - 1, curDist + 1, curPath + [(curX, curY - 1)]))
    return (minDist, path)

# checks if a position is valid (if it is on the grid, and isn't an obstacle)
def isValidPos(app, row, col):
    return not (row < 0 or col < 0 or row >= app.rows or col >= app.cols or \
        app.grid[row][col] != "empty")



# gets the bounds of the cell at (row, col)
def getCellBounds(app, row, col):
    lMargin = app.width * app.leftMargin
    rMargin = app.width * app.rightMargin
    tMargin = app.height * app.topMargin
    bMargin = app.height * app.bottomMargin
    gridWidth  = app.width - lMargin - rMargin
    gridHeight = app.height - tMargin - bMargin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = lMargin + col * cellWidth
    x1 = lMargin + (col+ 1) * cellWidth
    y0 = tMargin + row * cellHeight
    y1 = tMargin + (row + 1) * cellHeight
    return (x0, y0, x1, y1)



def moveRobots(app):
    for robot in app.robots:
        if robot.chaseType == "follow":
            shortestPath = getShortestPath(app, robot, app.player)
            robot.row = shortestPath[1][0][0]
            robot.col = shortestPath[1][0][1]
            app.BFSPath = shortestPath[1]



# called when the app is first initialized
def appStarted(app):
    app.musicOn = True
    app.soundEffOn = True
    app.levelsUnlocked = set()
    app.levelsUnlocked.add(1)
    app.grid = []
    app.rows = 0
    app.cols = 0
    app.leftMargin = 1 / 40
    app.rightMargin = 1 / 40
    app.topMargin = 1 / 7
    app.bottomMargin = 1 / 40
    app.robots = []
    app.buttons = []
    app.player = GridObject(0, 0)
    app.exit = GridObject(0, 0)
    app.visualizeBFS = False
    app.BFSPath = []
    switchScreen(app, "titleScreen")

# draws all the buttons
def drawButtons(app, canvas):
    for button in app.buttons:
        (x0, y0, x1, y1) = button.getBounds(app)
        canvas.create_rectangle(x0, y0, x1, y1, fill = button.fill,
        outline = button.outline)
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text = button.text,
        fill = button.textColor,
        font = button.getFont())

# draws the grid
def drawGrid(app, canvas):
    for i in range (len(app.grid)):
        for j in range (len(app.grid[i])):
            lMargin = app.width * app.leftMargin
            rMargin = app.width * app.rightMargin
            tMargin = app.height * app.topMargin
            bMargin = app.height * app.bottomMargin
            tileWidth = (app.width - lMargin - rMargin) / app.cols
            tileHeight = (app.height - tMargin - bMargin) / app.rows
            canvas.create_rectangle(lMargin + tileWidth * j,
                tMargin + tileHeight * i,
                lMargin + tileWidth * (j + 1),
                tMargin + tileHeight * (i + 1),
                fill = "blue" if app.grid[i][j] == "empty" else "gray",
                outline = "black")

# draws the player
def drawPlayer(app, canvas):
    if not app.player.visible:
        return
    (x0, y0, x1, y1) = getCellBounds(app, app.player.row, app.player.col)
    canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text = "player",
        fill = "lime", font = "Arial 15")

# draws all the enemies (robots)
def drawRobots(app, canvas):
    for robot in app.robots:
        if not robot.visible:
            continue
        (x0, y0, x1, y1) = getCellBounds(app, robot.row, robot.col)
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text = "robot",
            fill = "red", font = "Arial 15")

# draws the exit
def drawExit(app, canvas):
    if not app.exit.visible:
        return
    (x0, y0, x1, y1) = getCellBounds(app, app.exit.row, app.exit.col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = "yellow", outline = "black")



# draws the background for the title screen
def drawTitleScreenBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "blue")

# draws the text for the title screen
def drawTitleScreenText(app, canvas):
    canvas.create_text(app.width / 2, app.height / 5,
    text = "Barn Escape", fill = "orange", font = "Arial 50 bold")

# the mousePressed function for the title screen
def titleScreen_mousePressed(app, event):
    clickEvent = checkForButtonPress(app, event.x, event.y)
    if clickEvent == "startGame":
        switchScreen(app, "levelSelectScreen")
    elif clickEvent == "settings":
        switchScreen(app, "settingsScreen")
    elif clickEvent == "quit":
        exit(0)

# the mouseMoved function for the title screen
def titleScreen_mouseMoved(app, event):
    checkForButtonHover(app, event.x, event.y)

# the redrawAll function for the title screen
def titleScreen_redrawAll(app, canvas):
    drawTitleScreenBackground(app, canvas)
    drawTitleScreenText(app, canvas)
    drawButtons(app, canvas)



# the redrawAll function for the settings screen
def settingsScreen_redrawAll(app, canvas):
    pass



# draws the background for the level select screen
def drawLevelSelectScreenBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "gray")

# draws the text for the level select screen
def drawLevelSelectScreenText(app, canvas):
    canvas.create_text(app.width / 2, app.height / 7,
    text = "Level Select", fill = "orange", font = "Arial 50 bold")

# the mousePressed function for the level select screen
def levelSelectScreen_mousePressed(app, event):
    clickEvent = checkForButtonPress(app, event.x, event.y)
    if clickEvent == "level1":
        switchScreen(app, "level1")
    elif clickEvent == "titleScreen":
        switchScreen(app, "titleScreen")

# the mouseMoved function for the level select screen
def levelSelectScreen_mouseMoved(app, event):
    checkForButtonHover(app, event.x, event.y)

# the redrawAll function for the level select screen
def levelSelectScreen_redrawAll(app, canvas):
    drawLevelSelectScreenBackground(app, canvas)
    drawLevelSelectScreenText(app, canvas)
    drawButtons(app, canvas)



# draws the background for the first level
def drawLevel1Background(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "aqua")

# draws the text for the first level
def drawLevel1Text(app, canvas):
    canvas.create_text(app.width / 2, app.height / 14,
    text = "Level 1", fill = "red", font = "Arial 50 bold")

# the keyPressed function for the first level
def level1_keyPressed(app, event):
    if event.key == "m":
        moveRobots(app)
    if event.key == "Up":
        if isValidPos(app, app.player.row - 1, app.player.col):
            app.player.row -= 1
            moveRobots(app)
    if event.key == "Down":
        if isValidPos(app, app.player.row + 1, app.player.col):
            app.player.row += 1
            moveRobots(app)
    if event.key == "Right":
        if isValidPos(app, app.player.row, app.player.col + 1):
            app.player.col += 1
            moveRobots(app)
    if event.key == "Left":
        if isValidPos(app, app.player.row, app.player.col - 1):
            app.player.col -= 1
            moveRobots(app)
    if event.key == "t":
        app.visualizeBFS = not app.visualizeBFS
    if event.key == "r":
        initializeLevel1v2(app)
    if event.key == "q":
        switchScreen(app, "levelSelectScreen")

# draws the path of the BFS if toggled
def drawBFSPath(app, canvas):
    if not app.visualizeBFS:
        return
    for (row, col) in app.BFSPath:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = "purple",
        outline = "black")

# the redrawAll function for the first level
def level1_redrawAll(app, canvas):
    drawLevel1Background(app, canvas)
    drawLevel1Text(app, canvas)
    drawGrid(app, canvas)
    drawBFSPath(app, canvas)
    drawPlayer(app, canvas)
    drawRobots(app, canvas)
    drawExit(app, canvas)



def main():
    runApp(width = 850, height = 700)



if __name__ == '__main__':
    main()