import pygame
import json
import time
import csv
import os

import pygame.sysfont

pygame.init()

screendims = [9 * 50, 16 * 50] # [450, 800]
displayw, displayh = pygame.display.Info().current_w, pygame.display.Info().current_h # Display dimensions

def displayper(wh: int, per: int) -> int:
    """Function that returns a percentage of the screen's width or height in pixels"""
    return displayw * (per / 100) if wh == 0 else displayh * (per / 100)

class bin:
    class cfgs:
        colors = json.loads(open("./bin/cfgs/colors.cfg", "r").read())
        text = json.loads(open("./bin/cfgs/text.cfg", "r").read())
        for size in text["sizes"]: # The original text size is in percentage, this for loop converts it into pixels
            text["sizes"][size] = round((displayper(0, text["sizes"][size]) + displayper(1, text["sizes"][size])) / 2)
    class icons:
        account = pygame.transform.scale(pygame.image.load("./bin/icons/account.png"), (displayper(1, 8), displayper(1, 8)))
        information = pygame.transform.scale(pygame.image.load("./bin/icons/information.png"), (displayper(1, 8), displayper(1, 8)))
        investments = pygame.transform.scale(pygame.image.load("./bin/icons/investments.png"), (displayper(1, 8), displayper(1, 8)))
        menu = pygame.transform.scale(pygame.image.load("./bin/icons/menu.png"), (displayper(1, 5), displayper(1, 5)))
        back = pygame.transform.scale(pygame.image.load("./bin/icons/back.png"), (displayper(1, 5), displayper(1, 5)))
        backarrow = pygame.transform.scale(pygame.image.load("./bin/icons/backarrow.png"), (displayper(1, 6), displayper(1, 6)))
        frontarrow = pygame.transform.scale(pygame.image.load("./bin/icons/frontarrow.png"), (displayper(1, 6), displayper(1, 6)))
    stocks = {}
    for stock in os.listdir("./bin/stocks/"):
        fields = []
        rows = []

        with open("./bin/stocks/" + stock, "r") as file:
            csvreader = csv.reader(file)
            fields = next(csvreader)
            for row in csvreader:
                rows.append(row)
        stocks[stock[::-1][4:][::-1]] = rows

def ismouseinrect(mousepos: list[int, int], rect: list[int, int, int, int] | pygame.Rect) -> bool:
    """Function that return a bool if the mouse's position in on top of a rect"""
    rect = [[rect[0], rect[1]], [rect[2], rect[3]]]
    if mousepos[0] > rect[0][0] and mousepos[0] < rect[0][0] + rect[1][0]:
        if mousepos[1] > rect[0][1] and mousepos[1] < rect[0][1] + rect[1][1]:
            return True
    return False

def getTopleftFromMiddle(middle: list[int, int], surfaceSize: list[int, int] | pygame.Surface) -> list[int, int]:
    mx, my = middle
    if type(surfaceSize) == list:
        top = my - (surfaceSize[1] // 2)
        left = mx - (surfaceSize[0] // 2)
    else:
        top = my - (surfaceSize.get_height() // 2)
        left = mx - (surfaceSize.get_width() // 2)
    return [left, top]

def text(fontFamily: str, fontSize: int, text: str, bold: bool = False, italic: bool = False) -> pygame.Surface:
    font = pygame.font.SysFont(fontFamily, fontSize, bold, italic)

def checkEvents(events: list) -> dict:
    """Function to check window events"""
    output = {"quit": False}
    for event in events:
        if event.type == pygame.QUIT:
            output["quit"] = True # Ends the program if the QUIT event is triggered
    return output

def drawMenuBar(display: pygame.Surface, page: int) -> None:
    """Function that draws the menubar to the given window (display)"""
    barHeight = displayper(1, 12.5)
    coords = [0, displayh - barHeight] # Top left coordenates
    
    pygame.draw.rect(display, bin.cfgs.colors["menubackground"], pygame.Rect(coords[0], coords[1], displayw - coords[0], displayh - coords[1])) # Menu rectangle

    display.blit(text())

def main() -> None:
    """Main function, displaying the window, drawing the main objects, ..."""

    page = 0 # 0: Portfolio
             # 1: Investing
             # 2: Learning

    while 1:
        events = checkEvents(pygame.event.get())
        if events["quit"]:
            return 0
        
        display.fill(bin.cfgs.colors["background"]) # Filling the window with the background color

        drawMenuBar(display, page) # Draw the menu bar

        if page == 0:
            pass

        if page == 1:
            pass
        
        if page == 2:
            pass

        pygame.display.flip() # Clearing the screen

# NOTE: Replace screendims with [displayw, displayh] before compiling
display = pygame.display.set_mode(screendims) # Screen dimensions

# ted
main()

pygame.quit()
