import pygame
import sys
import random
import math
import numpy
pygame.init()
czas = pygame.time.Clock()

H = 720                                      # wysokość zbiornika
L = 1280                                      # szerokość zbiornika
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

        if 54 < math.sqrt((atom.Rect.centerx - atom2.Rect.centerx)**2 + (atom.Rect.centery - atom2.Rect.centery)**2) <= 2 * atom.r + 3:

            '''print("Odleglosc: ", math.sqrt((atom.Rect.centerx - atom2.Rect.centerx)
                                           ** 2 + (atom.Rect.centery - atom2.Rect.centery)**2))
            print("kolizja")'''
            return i
    return -1


atomy = []  # lista atomów

s = 60  # średnica


# set 1 ukośne ten sam kierunek x
obiekt0 = pygame.Rect(200, 200, s, s)
atom0 = Atom(obiekt0, -3, -3, s, (100, 100, 250))
atomy.append(atom0)
obie1 = pygame.Rect(100, 100, s, s)
atom1 = Atom(obie1, 3, 3, s, (0, 0, 0))
atomy.append(atom1)

# set2 ukośne ten sam kierunek y
obiekt2 = pygame.Rect(650, 400, s, s)
atom2 = Atom(obiekt2, -3, -4, s, (255, 255, 255))
atomy.append(atom2)
obie3 = pygame.Rect(350, 300, s, s)
atom3 = Atom(obie3, 3, -2, s, (0, 0, 0))
atomy.append(atom3)

# set3    prawo lewo
obiekt4 = pygame.Rect(70, 430, s, s)
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
atomy.append(atom7)

# set5              góra dół
'''obiekt8 = pygame.Rect(200, 200, s, s)
atom8 = Atom(obiekt8, 0, 3, s, (250, 100, 250))
atomy.append(atom8)
obiekt9 = pygame.Rect(260, 300, s, s)
atom9 = Atom(obiekt9, -0.5, 0, s, (100, 250, 250))
atomy.append(atom9)'''
pozycja_x = []
pozycja_y = []
for atom in atomy:
    pozycja_x.append(atom.Rect.x)
    pozycja_y.append(atom.Rect.y)


def ruch():
    i = 0
    for atom in atomy:
        # print(atom.col,atom.Rect.x,atom.Rect.y)
        pozycja_x[i] += atom.speed_x
        pozycja_y[i] += atom.speed_y
        atom.Rect.x = int(pozycja_x[i])
        atom.Rect.y = int(pozycja_y[i])
        i += 1

        # print(atom.col, atom.Rect.x, atom.Rect.y)
    tablica = [0] * len(atomy)
    '''print(
        f"pozycja atomu {atom.col} {atom.Rect.center[0]} i {atom.Rect.center[1]}")'''

    for i in range(len(atomy)):
        atom = atomy[i]
        kol = kolizja(i, atomy)

        # współrzędne wskazują na lewy górny róg kwadratu który wypełnia kulka
        if atom.Rect.centerx - atom.r <= 0 and atom.speed_x < 0:
            print("PYK")
            print(atom.Rect.centerx - atom.r)
            print(atom.Rect.centerx)
            print(i, "SZYB:  ", atomy[i].speed_x)
            atom.speed_x *= -1
            print(atomy[i].speed_x)
        elif atom.Rect.centerx + atom.r >= L and atom.speed_x > 0:
            atomy[i].Rect.x = L - atom.r * 2
            #print("pyk róg")
            atomy[i].speed_x *= -1

        elif atom.Rect.centery - atom.r <= 0 and atom.speed_y < 0:
            #print("pyk odbicie")
            atomy[i].Rect.y = 0
            atomy[i].speed_y *= -1
        elif atom.Rect.centery + atom.r >= H and atom.speed_y > 0:
            atomy[i].Rect.y = H - atom.r * 2
            atomy[i].speed_y *= -1
        '''if atom.Rect.x <= 0 or atom.Rect.x + 2 * atom.r >= L:  # współrzędne wskazują na lewy górny róg kwadratu który wypełnia kulka
            print("pyk róg")
            atom.speed_x *= -1

        elif atom.Rect.y <= 0 or atom.Rect.y + 2 * atom.r >= H:
            print("pyk odbicie")
            atom.speed_y *= -1'''

        if kol >= 0 and tablica[kol] == 0:
            atom1 = atomy[kol]
            tablica[kol] = 1
            tablica[i] = 1
            xs = pozycja_x[i]
            ys = pozycja_y[i]
            xs1 = pozycja_x[kol]
            ys1 = pozycja_y[kol]
            print(atom.Rect.centerx)
            print(atom1.Rect.center)

            tupl = (xs - xs1,  # (r1 - r2)
                    ys - ys1)

            tupl2 = (xs1 - xs,  # (r2 - r1)
                     ys1 - ys)

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
            #print(atomy[i].speed_x, atomy[i].speed_y)
            #print(atomy[kol].speed_x, atomy[kol].speed_y)
            '''n = [None, None]
            t = [None, None]

            n[0] = (xs1 - xs) / (((xs1 - xs)**2 + (ys1 - ys)**2)**0.5)
            n[1] = (ys1 - ys) / (((xs1 - xs)**2 + (ys1 - ys)**2)**0.5)
            t[0] = (-1.0 * (ys1 - ys)) / (((xs1 - xs)**2 + (ys1 - ys)**2)**0.5)
            t[1] = (xs1 - xs) / (((xs1 - xs)**2 + (ys1 - ys)**2)**0.5)

            v1 = [atom.speed_x, atom.speed_y]
            v2 = [atom1.speed_x, atom1.speed_y]

            vn1 = vt1 = vn2 = vt2 = 0
            for i in range(2):
                vn1 += v1[i] * n[i]
                vt1 += v1[i] * t[i]
                vn2 += v2[i] * n[i]
                vt2 += v2[i] * t[i]

            vn1, vn2 = vn2, vn1

            v1[0], v1[1], v2[0], v2[1] = vn1 * n[0] + vt1 * t[0], vn1 * n[1] + vt1 * t[1], vn2 * n[0] + vt2 * t[0], vn2 * n[1] + vt2 * t[1]
            atom.speed_x, atom.speed_y, atom1.speed_x, atom1.speed_y = v1[0], v1[1], v2[0], v2[1]'''
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
