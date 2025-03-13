import random
import pygame
import json
import time
import csv
import os

pygame.init()

screendims = [9 * 50, 16 * 50] # pygame.display.Info().current_w, pygame.display.Info().current_h
display = pygame.display.set_mode(screendims)

def displayper(wh, per):
    return screendims[wh] / 100 * per

def displayperwomenu(wh, per):
    if wh == 1:
        return (screendims[1] - displayper(1, 15)) / 100 * per
    return screendims[wh] / 100 * per

def ismouseinrect(mousepos, rect):
    rect = [[rect[0], rect[1]], [rect[2], rect[3]]]
    if mousepos[0] > rect[0][0] and mousepos[0] < rect[0][0] + rect[1][0]:
        if mousepos[1] > rect[0][1] and mousepos[1] < rect[0][1] + rect[1][1]:
            return True
    return False

account = []
date = 0

class bin:
    class cfgs:
        colors = json.loads(open("./bin/cfgs/colors.cfg", "r").read())
        text = json.loads(open("./bin/cfgs/text.cfg", "r").read())
        for size in text["sizes"]:
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

def text(font, fontsize, text, antialias, color):
    return pygame.font.SysFont(font, fontsize, 1).render(text, antialias, color)

def getstocksindex(stocks, index):
    n = 0
    for stock in stocks:
        if n == index:
            return stock
        n += 1

def drawgraph(d, graphcolor, topleft, bottomright, values, valuescale, interval):
    pygame.draw.rect(d, graphcolor, pygame.Rect(topleft[0], topleft[1], bottomright[0] - topleft[0], bottomright[1] - topleft[1]), 1)
    points = []
    i = 0
    for value in values:
        points.append([i, value * valuescale])
        i += interval
    
    lines = []
    i = 0
    while i < len(values):
        if i % 2 == 0:
            lines.append([points[i], points[i+1]])
        i += 1

    for line in lines:
        pygame.draw.line(d, graphcolor, [topleft[0] + line[0][0], bottomright[1] - line[0][1]], [topleft[0] + line[1][0], bottomright[1] - line[1][1]])

def getstockpricefromindex(stock, index):
    i = 0
    for data in stock:
        if i == index:
            return (float(data[1]) + float(data[4])) / 2
        i += 1

def getfortunefromlog(stocks, logs):
    fortune = 0
    for log in logs:
        fortune -= log[2] * getstockpricefromindex(stocks[log[0]], log[1])
    return fortune

displaystate = 1
investdisplaystate = -1
investstocksdisplaystate = 0
investspecificstock = ""
page = 1
lastaction = time.time()
startcounter = time.time()

clock = pygame.time.Clock()
while displaystate:
    if time.time() - startcounter >= 3:
        date += 1
        startcounter = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            displaystate = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ismouseinrect(pygame.mouse.get_pos(), [displayper(0, 13) - (displayper(1, 6) / 2) - displayper(1, 4), displayper(1, 89) - displayper(1, 4), displayper(1, 6) + displayper(1, 10), displayper(1, 6) + displayper(1, 10)]):
                page = 0
                lastaction = time.time()
            if ismouseinrect(pygame.mouse.get_pos(), [displayper(0, 50) - (displayper(1, 6) / 2) - displayper(1, 4), displayper(1, 89) - displayper(1, 4), displayper(1, 6) + displayper(1, 10), displayper(1, 6) + displayper(1, 10)]):
                page = 1
                lastaction = time.time()
            if ismouseinrect(pygame.mouse.get_pos(), [displayper(0, 87) - (displayper(1, 6) / 2) - displayper(1, 4), displayper(1, 89) - displayper(1, 4), displayper(1, 6) + displayper(1, 10), displayper(1, 6) + displayper(1, 10)]):
                page = 2
                lastaction = time.time()
            if page == 0:
                pass
            if page == 1:
                if investdisplaystate == -1:
                    if ismouseinrect(pygame.mouse.get_pos(), [0, 0, screendims[0], displayperwomenu(1, 33.3)]):
                        investdisplaystate = 0
                        lastaction = time.time()
                    if ismouseinrect(pygame.mouse.get_pos(), [0, displayperwomenu(1, 33.3), screendims[0], displayperwomenu(1, 33.3)]):
                        investdisplaystate = 1
                        lastaction = time.time()
                    if ismouseinrect(pygame.mouse.get_pos(), [0, displayperwomenu(1, 66.6), screendims[0], displayperwomenu(1, 33.3)]):
                        investdisplaystate = 2
                        lastaction = time.time()
                if investdisplaystate == 0:
                    if investspecificstock == "":
                        if ismouseinrect(pygame.mouse.get_pos(), [0, 0, displayper(0, 3) + displayper(1, 7), displayper(1, 1.5) + displayper(1, 7)]):
                            investdisplaystate = -1
                            lastaction = time.time()
                        if ismouseinrect(pygame.mouse.get_pos(), [0, displayperwomenu(1, 90), displayper(0, 50), displayperwomenu(1, 10)]):
                            if investstocksdisplaystate != 0:
                                investstocksdisplaystate -= 8
                                lastaction = time.time()
                        if ismouseinrect(pygame.mouse.get_pos(), [displayper(0, 50), displayperwomenu(1, 90), displayper(0, 50), displayperwomenu(1, 10)]):
                            investstocksdisplaystate += 8
                            lastaction = time.time()
                        for i in range(1, 9):
                            if time.time() - lastaction > .2 and ismouseinrect(pygame.mouse.get_pos(), [0, displayperwomenu(1, i*10), screendims[0], displayperwomenu(1, 10)]):
                                investspecificstock = getstocksindex(bin.stocks, i - 1 + investstocksdisplaystate)
                                lastaction = time.time()
                    else:
                        if ismouseinrect(pygame.mouse.get_pos(), [0, displayper(1, 70), displayper(0, 50), displayperwomenu(1, 100) - displayper(1, 70)]):
                            account.append([investspecificstock, date, 1])
                            lastaction = time.time()
                        if ismouseinrect(pygame.mouse.get_pos(), [displayper(0, 50), displayper(1, 70), displayper(0, 50), displayperwomenu(1, 100) - displayper(1, 70)]):
                            account.append([investspecificstock, date, -1])
                            lastaction = time.time()
                if investdisplaystate == 1:
                    if ismouseinrect(pygame.mouse.get_pos(), [0, 0, displayper(0, 3) + displayper(1, 7), displayper(1, 1.5) + displayper(1, 7)]):
                        investdisplaystate = -1
                        lastaction = time.time()
                if investdisplaystate == 2:
                    if ismouseinrect(pygame.mouse.get_pos(), [0, 0, displayper(0, 3) + displayper(1, 7), displayper(1, 1.5) + displayper(1, 7)]):
                        investdisplaystate = -1
                        lastaction = time.time()
            if page == 2:
                pass
    
    display.fill(bin.cfgs.colors["background"])
    
    if page == 0:
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account1"], "1234 5678 9012 3456", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 1)))

        pygame.draw.line(display, bin.cfgs.colors["text"], (displayper(0, 2), displayper(1, 7)), (displayper(0, 98), displayper(1, 7)))

        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], f"Saldo Atual: {getfortunefromlog(bin.stocks, account):.2f} $", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 8)))

        pygame.draw.line(display, bin.cfgs.colors["text"], (displayper(0, 2), displayper(1, 12.5)), (displayper(0, 98), displayper(1, 12.5)))

        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "Ação Recomendada:", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 13.5)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "TSLA", True, bin.cfgs.colors["text"]), (displayper(0, 85.5), displayper(1, 13.5)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "ETF Recomendado:", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 17)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "S$P 500", True, bin.cfgs.colors["text"]), (displayper(0, 76.5), displayper(1, 17)))

        pygame.draw.line(display, bin.cfgs.colors["text"], (displayper(0, 2), displayper(1, 21.5)), (displayper(0, 98), displayper(1, 21.5)))

        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "Ações Mais Investidas:", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 22.5)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "1. TSLA      1234.56 EUR   +1.23%", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 26)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "2. AMZN      1000.00 EUR   +2.34%", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 29.5)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "3. APPL       900.00 EUR   +3.45%", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 33)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "4. GOGL       800.00 EUR   +4.56%", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 36.5)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "5. INTL       700.00 EUR   +5.67%", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 40)))

        pygame.draw.line(display, bin.cfgs.colors["text"], (displayper(0, 2), displayper(1, 44.5)), (displayper(0, 98), displayper(1, 44.5)))
        
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "Ações Mais Lucrativas:", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 45.5)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "5. TSLA      1234.56 EUR   +1.23%", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 63)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "4. AMZN      1000.00 EUR   +2.34%", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 59.5)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "3. APPL       900.00 EUR   +3.45%", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 56)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "2. GOGL       800.00 EUR   +4.56%", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 52.5)))
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account2"], "1. INTL       700.00 EUR   +5.67%", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 49)))

        pygame.draw.line(display, bin.cfgs.colors["text"], (displayper(0, 2), displayper(1, 67.5)), (displayper(0, 98), displayper(1, 67.5)))
    elif page == 1:
        if investdisplaystate == -1:
            display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account1"], "Ações", True, bin.cfgs.colors["text"]), (displayper(0, 50) - (len("Ações") * (bin.cfgs.text["sizes"]["account1"]) / 1.7 / 2), displayperwomenu(1, 16.6) - (bin.cfgs.text["sizes"]["account1"] / 2)))

            pygame.draw.line(display, bin.cfgs.colors["darkbar"], (displayper(0, 2), displayperwomenu(1, 33.3)), (displayper(0, 98), displayperwomenu(1, 33.3)))

            display.blit(text(bin.cfgs.text["font"],bin.cfgs.text["sizes"]["account1"], "ETFs", True, bin.cfgs.colors["text"]), (displayper(0, 50) - (len("ETFs") * (bin.cfgs.text["sizes"]["account1"]) / 1.7 / 2), displayperwomenu(1, 50) - (bin.cfgs.text["sizes"]["account1"] / 2)))

            pygame.draw.line(display, bin.cfgs.colors["darkbar"], (displayper(0, 2), displayperwomenu(1, 66.6)), (displayper(0, 98), displayperwomenu(1, 66.6)))

            display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account1"], "Criptomoedas", True, bin.cfgs.colors["text"]), (displayper(0, 50) - (len("Criptomoedas") * (bin.cfgs.text["sizes"]["account1"]) / 1.7 / 2),displayperwomenu(1, 83.3) - (bin.cfgs.text["sizes"]["account1"] / 2)))
        if investdisplaystate == 0:
            if investspecificstock == "":
                display.blit(bin.icons.back, (displayper(0, 3), displayper(1, 1.5)))
                for i in range(1, 10):
                    pygame.draw.line(display, bin.cfgs.colors["darkbar"], (displayper(0, 2), displayperwomenu(1, i*10)), (displayper(0, 98), displayperwomenu(1, i*10)))
                range_ = [0 + investstocksdisplaystate, 8 + investstocksdisplaystate]
                i = 0
                y = 0
                for stock in bin.stocks:
                    if i >= range_[0]:
                        if i < range_[1]:
                            display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["invest1"], stock, True, bin.cfgs.colors["text"]), (displayper(0, 3), displayperwomenu(1, y*10 + 13)))
                            y += 1
                    i += 1
                display.blit(bin.icons.backarrow, (displayper(0, 10), displayper(1, 78)))
                display.blit(bin.icons.frontarrow, (displayper(0, 80), displayper(1, 78)))
            else:
                display.blit(bin.icons.back, (displayper(0, 3), displayper(1, 1.5)))
                display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["invest1"], investspecificstock, True, bin.cfgs.colors["text"]), (displayper(0, 15), displayper(1, 1)))
                drawgraph(display, [255, 255, 255], [displayper(0, 5), displayper(1, 20)], [displayper(1, 53.5), displayper(1, 60)], [(float(bin.stocks[investspecificstock][i][1]) + float(bin.stocks[investspecificstock][i][2])) / 2 for i in range(date if date % 2 == 0 else date + 1)], 1.5, .1)

                display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["invest2"], f"Valor atual: {getstockpricefromindex(bin.stocks[investspecificstock], date)} $", True, [255, 255, 255]), (displayper(0, 5), displayper(1, 17)))

                pygame.draw.line(display, [0, 0, 0], [displayper(0, 2), displayper(1, 70)], [displayper(0, 98), displayper(1, 70)])

                pygame.draw.rect(display, [0, 255, 0], pygame.Rect(displayper(0, 5), displayper(1, 72.5), displayper(0, 40), displayper(1, 10)), border_radius=15)
                pygame.draw.rect(display, [255, 0, 0], pygame.Rect(displayper(0, 55), displayper(1, 72.5), displayper(0, 40), displayper(1, 10)), border_radius=15)

                display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["invest1"], "Comprar", True, [0, 0, 0]), (displayper(0, 10), displayper(1, 75)))
                display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["invest1"], "Vender", True, [0, 0, 0]), (displayper(0, 60), displayper(1, 75)))
        if investdisplaystate == 1:
            display.blit(bin.icons.back, (displayper(0, 3), displayper(1, 1.5)))
            for i in range(1, 10):
                pygame.draw.line(display, bin.cfgs.colors["darkbar"], (displayper(0, 2), displayperwomenu(1, i*10)), (displayper(0, 98), displayperwomenu(1, i*10)))
        if investdisplaystate == 2:
            display.blit(bin.icons.back, (displayper(0, 3), displayper(1, 1.5)))
            for i in range(1, 10):
                pygame.draw.line(display, bin.cfgs.colors["darkbar"], (displayper(0, 2), displayperwomenu(1, i*10)), (displayper(0, 98), displayperwomenu(1, i*10)))
    elif page == 2:
        display.blit(text(bin.cfgs.text["font"], bin.cfgs.text["sizes"]["account1"], "Vamos aprender!", True, bin.cfgs.colors["text"]), (displayper(0, 2), displayper(1, 1)))

    pygame.draw.rect(display, (bin.cfgs.colors["menubackground"]), pygame.Rect(0, displayper(1, 85), screendims[0], screendims[1]))

    if page == 0:
        pygame.draw.rect(display, (20, 20, 20), pygame.Rect(displayper(0, 16.6) - (displayper(1, 8) / 2) - displayper(1, 2), displayper(1, 89) - displayper(1, 2), displayper(1, 12), displayper(1, 12)), border_radius=10)
    if page == 1:
        pygame.draw.rect(display, (20, 20, 20), pygame.Rect(displayper(0, 50) - (displayper(1, 8) / 2) - displayper(1, 2), displayper(1, 89) - displayper(1, 2), displayper(1, 12), displayper(1, 12)), border_radius=10)
    if page == 2:
        pygame.draw.rect(display, (20, 20, 20), pygame.Rect(displayper(0, 83.3) - (displayper(1, 8) / 2) - displayper(1, 2), displayper(1, 89) - displayper(1, 2), displayper(1, 12), displayper(1, 12)), border_radius=10)

    display.blit(bin.icons.account, (displayper(0, 16.6) - (displayper(1, 8) / 2), displayper(1, 89)))
    display.blit(bin.icons.investments, (displayper(0, 50) - (displayper(1, 8) / 2), displayper(1, 89)))
    display.blit(bin.icons.information, (displayper(0, 83.3) - (displayper(1, 8) / 2), displayper(1, 89)))

    pygame.display.flip()
    clock.tick(24)

pygame.quit()
