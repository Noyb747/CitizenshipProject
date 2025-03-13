import pygame
import json
import time
import csv
import os

import pygame.sysfont

pygame.init()

ROOT = os.path.dirname(__file__).replace("\\", "/")[0].upper() + "".join(os.path.dirname(__file__).replace("\\", "/")[1:]) # __file__/../ (./CitizenshipProject/)

# NOTE: Replace with [pygame.display.Info().current_w, pygame.display.Info().current_h] before compiling
screendims = [9 * 50, 16 * 50] # [450, 800]
displayw, displayh = screendims

def displayper(wh: int, per: int) -> int:
    """Returns a percentage of the screen's width or height in pixels"""
    return displayw * (per / 100) if wh == 0 else displayh * (per / 100)

class bin:
    class cfgs:
        colors = json.loads(open(ROOT + "/bin/cfgs/colors.cfg", "r").read())
        text = json.loads(open(ROOT + "/bin/cfgs/text.cfg", "r").read())
        for size in text["sizes"]: # The original text size is in percentage, this for loop converts it into pixels
            text["sizes"][size] = round((displayper(0, text["sizes"][size]) + displayper(1, text["sizes"][size])) / 2)
        display = json.loads(open(ROOT + "/bin/cfgs/display.cfg", "r").read())
    class icons:
        account = pygame.transform.scale(pygame.image.load(ROOT + "/bin/icons/account.png"), (displayper(1, 8), displayper(1, 8)))
        information = pygame.transform.scale(pygame.image.load(ROOT + "/bin/icons/information.png"), (displayper(1, 8), displayper(1, 8)))
        investments = pygame.transform.scale(pygame.image.load(ROOT + "/bin/icons/investments.png"), (displayper(1, 8), displayper(1, 8)))
        menu = pygame.transform.scale(pygame.image.load(ROOT + "/bin/icons/menu.png"), (displayper(1, 5), displayper(1, 5)))
        back = pygame.transform.scale(pygame.image.load(ROOT + "/bin/icons/back.png"), (displayper(1, 5), displayper(1, 5)))
        backarrow = pygame.transform.scale(pygame.image.load(ROOT + "/bin/icons/backarrow.png"), (displayper(1, 6), displayper(1, 6)))
        frontarrow = pygame.transform.scale(pygame.image.load(ROOT + "/bin/icons/frontarrow.png"), (displayper(1, 6), displayper(1, 6)))
    stocks = {}
    for stock in os.listdir(ROOT + "/bin/stocks/"):
        fields = []
        rows = []

        with open(ROOT + "/bin/stocks/" + stock, "r") as file:
            csvreader = csv.reader(file)
            fields = next(csvreader)
            for row in csvreader:
                rows.append(row)
        stocks[stock[::-1][4:][::-1]] = rows
    class saves:
        account = json.loads(open(ROOT + "/bin/saves/account.json", "r").read())

class Portfolio:
    def __init__(self, data: dict = None):
        self.data = data
    
    def loadFile(self, filepath: str) -> None:
        """Loads the portfolio data from a json file"""
        self.data = json.loads(open(filepath, "r").read())
    
    def loadDict(self, _dict: dict) -> None:
        """Loads the portfolio data from a python dictionary"""
        self.data = _dict

    def getNumInvestments(self) -> int:
        """Returns the number of stocks, ETFs or cryptocoins bought"""
        investments = 0
        for category in self.data:
            for investment in self.data[category]:
                investments += self.data[category][investment]
        return investments
    
    def getNumInvestmentsTags(self) -> int:
        """Returns the number of different stocks, ETFs or cryptocoins bought"""
        return len(self.data["stocks"]) + len(self.data["etfs"]) + len(self.data["cryptocoins"])

def ismouseinrect(mousepos: list[int, int], rect: list[int, int, int, int] | pygame.Rect) -> bool:
    """Returns a bool if the mouse's position in on top of a rect"""
    rect = [[rect[0], rect[1]], [rect[2], rect[3]]]
    if mousepos[0] > rect[0][0] and mousepos[0] < rect[0][0] + rect[1][0]:
        if mousepos[1] > rect[0][1] and mousepos[1] < rect[0][1] + rect[1][1]:
            return True
    return False

def getTopleftFromMiddle(middle: list[int, int], surfaceSize: list[int, int] | pygame.Surface) -> list[int, int]:
    """Returns the top & left coords from the middle coords and a surfaceSize or surface"""
    mx, my = middle
    if type(surfaceSize) == list:
        sx, sy = surfaceSize[0], surfaceSize[1]
        top = my - (sy // 2)
        left = mx - (sx // 2)
    else:
        sx, sy = surfaceSize.get_width(), surfaceSize.get_height()
        top = my - (sy // 2)
        left = mx - (sx // 2)
    return [left, top]

def text(fontFamily: str, fontSize: int, text: str, color: list[int, int, int], bold: bool = False, italic: bool = False, antialias: bool = True) -> pygame.Surface:
    """Returns a surface that can be blit onto the screen"""
    return pygame.font.SysFont(fontFamily, fontSize, bold, italic).render(text, antialias, color)

def checkEvents(events: list) -> dict:
    """Checks window events"""
    output = {"quit": False, "mouseDown": False}
    for event in events:
        if event.type == pygame.QUIT:
            output["quit"] = True # Ends the program if the QUIT event is triggered
        if event.type == pygame.MOUSEBUTTONDOWN:
            output["mouseDown"] = True # Checks if the mouse is pressed down
    return output

def drawMenuBar(display: pygame.Surface, page: int) -> None:
    """Draws the menubar to the given window (display)"""
    barHeight = displayper(1, 12.5)
    coords = [0, displayh - barHeight] # Top left coordenates
    
    pygame.draw.rect(display, bin.cfgs.colors["menubackground"], pygame.Rect(coords[0], coords[1], displayw - coords[0], displayh - coords[1])) # Menu rectangle

    t = text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["menubar"], "Portfólio", bin.cfgs.colors["text"])
    display.blit(
        t, 
        getTopleftFromMiddle([displayper(0, 15), displayper(1, 90)], t)
    ) # Portfolio text

    t = text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["menubar"], "Investir", bin.cfgs.colors["text"])
    display.blit(
        t, 
        getTopleftFromMiddle([displayper(0, 49), displayper(1, 90)], t)
    ) # Investing text

    t = text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["menubar"], "Aprender", bin.cfgs.colors["text"])
    display.blit(
        t, 
        getTopleftFromMiddle([displayper(0, 85), displayper(1, 90)], t)
    ) # Learning text

    display.blit(
        bin.icons.account, 
        getTopleftFromMiddle([displayper(0, 15), displayper(1, 95)], bin.icons.account)
    ) # Portfolio icon

    display.blit(
        bin.icons.investments, 
        getTopleftFromMiddle([displayper(0, 49), displayper(1, 95)], bin.icons.investments)
    ) # Investing icon

    display.blit(
        bin.icons.information, 
        getTopleftFromMiddle([displayper(0, 85), displayper(1, 95)], bin.icons.information)
    ) # Learning icon

def renderPortfolio(display: pygame.Surface, balance: float) -> None:
    """Renders the portfolio page onto the display"""

    t = text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account1"], bin.saves.account["accnum"], bin.cfgs.colors["text"], bold=True)
    display.blit(t, getTopleftFromMiddle([displayper(0, 50), displayper(1, 3)], t)) # Drawing the account number on the top

    t = text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], f"Balance: {balance}", bin.cfgs.colors["text"])
    display.blit(t, [displayper(0, 10), displayper(1, 10)]) # Displaying the users balance

def renderInvesting(display: pygame.Surface) -> None:
    """Renders the investing page onto the display"""

    t = text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["invest1"], "Investing page", bin.cfgs.colors["text"], bold= True, italic= True, antialias= True)
    display.blit(t, [displayper(0, 10), displayper(1, 10)])

def renderLearning(display: pygame.Surface) -> None:
    """Renders the learning page onto the display"""

    t = text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["invest1"], "Learning page", bin.cfgs.colors["text"], bold= True, italic= True, antialias= True)
    display.blit(t, [displayper(0, 10), displayper(1, 10)])

def main(display: pygame.Surface, clock) -> None:
    """Main function, displaying the window, drawing the main objects, ..."""
    display = pygame.display.set_mode(screendims) # Display setup
    pygame.display.set_caption("Aprender a investir") # Setting app title
    clock = pygame.time.Clock()
    balance = bin.saves.account["balance"] # Stored money, total minus the stocks bought or sold, doesn't change with time

    portfolio = Portfolio()
    portfolio.loadDict(bin.saves.account["portfolio"])

    page = 0 # 0: Portfolio
            # 1: Investing
            # 2: Learning

    while 1:
        events = checkEvents(pygame.event.get())
        if events["quit"]:
            return 0
        if events["mouseDown"]:
            if ismouseinrect(pygame.mouse.get_pos(), [displayper(0, 5), displayper(1, 90), displayper(0, 20), displayper(1, 10)]): # Checks if the mouse pressed the portfolio icon
                page = 0
            elif ismouseinrect(pygame.mouse.get_pos(), [displayper(0, 39), displayper(1, 90), displayper(0, 20), displayper(1, 10)]): # Checks if the mouse pressed the investing icon
                page = 1
            elif ismouseinrect(pygame.mouse.get_pos(), [displayper(0, 75), displayper(1, 90), displayper(0, 20), displayper(1, 10)]): # Checks if the mouse pressed the learning icon
                page = 2

        display.fill(bin.cfgs.colors["background"]) # Filling the window with the background color
        
        if page == 0: renderPortfolio(display, balance)
        if page == 1: renderInvesting(display)
        if page == 2: renderLearning(display)
        
        drawMenuBar(display, page) # Drawing the menu bar

        pygame.display.flip() # Clearing the screen

        clock.tick(bin.cfgs.display["fps"])

# ted
main()

pygame.quit()
