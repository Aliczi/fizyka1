import pygame
import sys
import random
import math
import numpy
pygame.init()
czas = pygame.time.Clock()

H = 500                                       # wysokość zbiornika
L = 800                                       # szerokość zbiornika
screen = pygame.display.set_mode((L, H))     # -------------


class Atom():
    def __init__(self, Rect, x, y, s, kolor):
        self.Rect = Rect
        self.speed_x = x
        self.speed_y = y
        self.x = Rect.center[0]
        self.y = Rect.center[1]

        self.r = s / 2
        self.col = kolor


def kolizja(j, atomy):  # zwraca indeks pierwszego atomu z którym wykryje zdarzenie
    atom = atomy[j]
    for i in range(len(atomy)):
        atom2 = atomy[i]
        # print(math.sqrt((atom.Rect.x - atom2.Rect.x) ** 2 + (atom.Rect.y - atom2.Rect.y) ** 2))
        # zamiast 56 2xpromień a x powinien r/10
        # zamiast 56 2xpromień a x powinien r/10
        if 54 < math.sqrt((atom.Rect.x - atom2.Rect.x)**2 + (atom.Rect.y - atom2.Rect.y)**2) < 2 * atom.r + 4:
            print("kolizja")
            return i
    return -1


atomy = []  # lista atomów

s = 60  # średnica


# set 1 ukośne ten sam kierunek x
obiekt0 = pygame.Rect(200, 200, s, s)
atom0 = Atom(obiekt0, -3, -3, s, (100, 100, 250))
atomy.append(atom0)
obie1 = pygame.Rect(100, 100, s, s)
atom1 = Atom(obie1, 3, 3, s, (250, 100, 100))
atomy.append(atom1)

# set2 ukośne ten sam kierunek y
obiekt2 = pygame.Rect(650, 400, s, s)
atom2 = Atom(obiekt2, -3, -4, s, (255, 255, 255))
atomy.append(atom2)
obie3 = pygame.Rect(350, 300, s, s)
atom3 = Atom(obie3, 3, -2, s, (0, 0, 0))
atomy.append(atom3)

# set3    prawo lewo
'''obiekt4 = pygame.Rect(70, 430, s, s)
atom4 = Atom(obiekt4, 3, 0, s, (50, 150, 100))
atomy.append(atom4)
obie5 = pygame.Rect(200, 430, s, s)
atom5 = Atom(obie5, -3, 0, s, (250, 250, 100))
atomy.append(atom5)

# set4              góra dół
obiekt6 = pygame.Rect(80, 200, s, s)
atom6 = Atom(obiekt6, 0, 3, s, (250, 100, 250))
atomy.append(atom6)
obiekt7 = pygame.Rect(80, 360, s, s)
atom7 = Atom(obiekt7, 0, -3, s, (100, 250, 250))
atomy.append(atom7)'''


def ruch():
    for atom in atomy:
        # print(atom.col,atom.Rect.x,atom.Rect.y)
        atom.Rect.x += int(atom.speed_x)
        atom.Rect.y += int(atom.speed_y)
        # print(atom.col, atom.Rect.x, atom.Rect.y)
    tablica = [0] * len(atomy)
    '''print(
        f"pozycja atomu {atom.col} {atom.Rect.center[0]} i {atom.Rect.center[1]}")'''

    for i in range(len(atomy)):
        atom = atomy[i]
        kol = kolizja(i, atomy)

        # współrzędne wskazują na lewy górny róg kwadratu który wypełnia kulka
        if atom.Rect.centerx - atom.r <= 0:
            atom.Rect.x = 0
            atom.speed_x *= -1

        if atom.Rect.centerx + atom.r >= L:
            atom.Rect.x = L - atom.r * 2

            #print("pyk róg")
            atom.speed_x *= -1

        if atom.Rect.centery - atom.r <= 0:
            #print("pyk odbicie")
            atom.Rect.y = 0
            atom.speed_y *= -1
        if atom.Rect.centery + atom.r >= H:
            atom.Rect.y = H - atom.r * 2
            atom.speed_y *= -1

        if kol >= 0 and tablica[kol] == 0:
            print("PYK")
            print(atomy[i].speed_x, atomy[i].speed_y)
            print(atomy[kol].speed_x, atomy[kol].speed_y)

            atom1 = atomy[kol]
            tablica[kol] = 1
            tablica[i] = 1
            print(atom.Rect.center)
            print(atom1.Rect.center)

            tupl = (atom.Rect.centerx - atom1.Rect.centerx,  # (r1 - r2)
                    atom.Rect.centery - atom1.Rect.centery)

            tupl2 = (atom1.Rect.centerx - atom.Rect.centerx,  # (r2 - r1)
                     atom1.Rect.centery - atom.Rect.centery)

            d = (tupl[0]**2) + (tupl[1]**2)
            d2 = (tupl2[0]**2) + (tupl2[1]**2)

            dot1 = ((atom.speed_x - atom1.speed_x) * tupl[0] + (
                atom.speed_y - atom1.speed_y) * tupl[1]) / d  # (dot/d)

            dot2 = ((atom1.speed_x - atom.speed_x) * tupl2[0] + (  # drugi atom
                atom1.speed_y - atom.speed_y) * tupl2[1]) / d

            x1 = dot1 * tupl[0]
            y1 = dot1 * tupl[1]
            x2 = dot2 * tupl2[0]
            y2 = dot2 * tupl2[1]

            atomy[i].speed_x -= x1
            atomy[i].speed_y -= y1
            atomy[kol].speed_x -= x2
            atomy[kol].speed_y -= y2
            print(atomy[i].speed_x, atomy[i].speed_y)
            print(atomy[kol].speed_x, atomy[kol].speed_y)

    # print("_____________________________",atom.Rect.colliderect(atom1.Rect))

        pygame.draw.ellipse(screen, atom.col, atom.Rect)


# Pętla programu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # wyście iksem z okienka konczy program
            pygame.quit()
            sys.exit()

    screen.fill((80, 80, 80))  # zmienia kolor tła okna
    ruch()
    pygame.display.flip()  # wyświetla obiekty
    czas.tick(60)  # spowalnia, max 60 klatek na sekundę
