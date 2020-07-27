import pygame
import sys
import math
import random


global d, R

pygame.init()
czas = pygame.time.Clock()


"""     Założenia projektu      """

etaH = 20  # Warunek minimalnego rozmiaru zbiornika: nH, nL >= 20
etaL = 20
R = 30  # promień R
s = 2 * R  # średnica
H = etaH * R  # wysokość zbiornika
L = etaL * R  # szerokość zbiornika
vGen = 3  # Prędkość
d = R / 10  # tolerancja zderzenia'

krok_czasu_startowy = vGen * min(etaH, etaL)
krok_czasu = krok_czasu_startowy

screen = pygame.display.set_mode((L, H + 40), pygame.RESIZABLE)
pygame.display.set_caption("Symulacja atomów")


"""_________________________________________________________"""


class Button():

    def __init__(self, x, y, width, height, color=(0, 0, 0), caption="Nowy przycisk"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.caption = caption

    def draw(self, screen):
        font = pygame.font.SysFont("ebrima", 20)
        text = font.render(self.caption, 1, (0, 0, 0))

        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text, self.rect)

    def mouse_over_button(self, pos):
        if pos[0] < self.rect.x + self.rect.width and pos[0] > self.rect.x:
            if pos[1] < self.rect.y + self.rect.height and pos[1] > self.rect.y:
                return True
        return False


przyciski = []

panel = Button(0, 0, 500, 40, (200, 200, 200))
przyciski.append(panel)

jeden = Button(0, 0, 80, 40, (200, 200, 200), " etaH: 20")
przyciski.append(jeden)
jedenplus = Button(100, 0, 20, 40, (0, 200, 200), "+")
przyciski.append(jedenplus)
jedenminus = Button(80, 0, 20, 40, (200, 200, 0), " -")
przyciski.append(jedenminus)

dwa = Button(120, 0, 80, 40, (200, 200, 200), " etaL: 20")
przyciski.append(dwa)
dwaplus = Button(220, 0, 20, 40, (0, 200, 200), "+")
przyciski.append(dwaplus)
dwaminus = Button(200, 0, 20, 40, (200, 200, 0), " -")
przyciski.append(dwaminus)

czasowy = Button(240, 0, 80, 40, (200, 200, 200), "")
przyciski.append(czasowy)
czasowyplus = Button(340, 0, 20, 40, (0, 200, 200), "+")
przyciski.append(czasowyplus)
czasowyminus = Button(320, 0, 20, 40, (200, 200, 0), " -")
przyciski.append(czasowyminus)

nowy_atom = Button(360, 0, 100, 40, (200, 200, 200), "")
przyciski.append(nowy_atom)
nowy_atom_plus = Button(480, 0, 20, 40, (0, 200, 200), "+")
przyciski.append(nowy_atom_plus)
nowy_atom_minus = Button(460, 0, 20, 40, (200, 200, 0), " -")
przyciski.append(nowy_atom_minus)


def rys_menu(screen):
    for el in przyciski:
        el.draw(screen)


"""__________________________________________________________________"""


class Atom():
    def __init__(self, Rect, x, y, s, kolor):
        self.Rect = Rect
        self.speed_x = x
        self.speed_y = y
        self.x = Rect.center[0]
        self.y = Rect.center[1]

        self.r = s / 2
        self.col = kolor


atomy = []  # lista atomów
pozycja_x = []
pozycja_y = []


def dodaj(L, H, R, vGen):
    xx = random.uniform(0.0 + R, L - R)
    yy = random.uniform(0.0 + R, H - R)
    atomy.append(Atom(pygame.Rect(xx, yy, 2 * R, 2 * R), random.uniform(-1.0 * vGen, vGen), random.uniform(-1.0 *
                                                                                                           vGen, vGen), s, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

    pozycja_x.append(xx)
    pozycja_y.append(yy)
    odbicia.append(-1)


"""________________________________Testowy zestaw atomów______________________________________"""
s = 60  # średnica

obiekt0 = pygame.Rect(200, 200, s, s)
atom0 = Atom(obiekt0, -3, -3, s, (100, 100, 250))
atomy.append(atom0)
obie1 = pygame.Rect(100, 100, s, s)
atom1 = Atom(obie1, 3, 3, s, (250, 100, 100))
atomy.append(atom1)

obiekt2 = pygame.Rect(360, 360, s, s)
atom2 = Atom(obiekt2, -3, -4, s, (255, 255, 255))
atomy.append(atom2)
obie3 = pygame.Rect(350, 290, s, s)
atom3 = Atom(obie3, 3, -2, s, (0, 0, 0))
atomy.append(atom3)

# set3    prawo lewo
obiekt4 = pygame.Rect(70, 430, s, s)
atom4 = Atom(obiekt4, 3, 0, s, (50, 150, 100))
atomy.append(atom4)
obie5 = pygame.Rect(200, 430, s, s)
atom5 = Atom(obie5, -3, 0, s, (250, 250, 100))
atomy.append(atom5)
#
# set4              góra dół
obiekt6 = pygame.Rect(80, 200, s, s)
atom6 = Atom(obiekt6, 0, 3, s, (250, 100, 250))
atomy.append(atom6)
obiekt7 = pygame.Rect(80, 360, s, s)
atom7 = Atom(obiekt7, 0, -3, s, (100, 250, 250))
atomy.append(atom7)
for atom in atomy:
    pozycja_x.append(atom.Rect.x)
    pozycja_y.append(atom.Rect.y)

"""__________________________________________________________________________________________________________________________________"""


# zwraca indeks pierwszego atomu z którym wykryje zdarzenie
def kolizja(j, atomy, pozx, pozy):
    atom = atomy[j]
    for i in range(len(atomy)):
        atom2 = atomy[i]
        # print(math.sqrt((atom.Rect.x - atom2.Rect.x) ** 2 + (atom.Rect.y - atom2.Rect.y) ** 2))
        # zamiast 56 2xpromień a x powinien r/10
        # zamiast 56 2xpromień a x powinien r/10
        if 60 > (math.sqrt((pozx[j] - pozx[i])**2 + (pozy[j] - pozy[i])**2)) and i != j and i != odbicia[j]:
            return i, True
        if 60 < (math.sqrt((pozx[j] - pozx[i])**2 + (pozy[j] - pozy[i])**2)) <= 60 + 3 and i != j and i != odbicia[j]:

            '''print("Odleglosc: ", math.sqrt((atom.Rect.centerx - atom2.Rect.centerx)
                                           ** 2 + (atom.Rect.centery - atom2.Rect.centery)**2))
            print("kolizja")'''
            return i, False
    return -1, False


odbicia = [-1] * len(atomy)


def ruch(screen, L, H):
    i = 0

    # print(odbicia)
    for atom in atomy:
        # print(atom.col,atom.Rect.x,atom.Rect.y)
        pozycja_x[i] += atom.speed_x
        pozycja_y[i] += atom.speed_y
        atom.Rect.x = int(pozycja_x[i])
        atom.Rect.y = int(pozycja_y[i])
        i += 1

        # print(atom.col, atom.Rect.x, atom.Rect.y)
    '''print(
        f"pozycja atomu {atom.col} {atom.Rect.center[0]} i {atom.Rect.center[1]}")'''

    #tablica = [0] * len(atomy)
    pozx=pozycja_x
    pozy=pozycja_y
    for i in range(len(atomy)):
        atom = atomy[i]
        #KOLIZJE Z ATOMAMI
        for j in range(len(atomy)):
            atom2 = atomy[j]
            # sprawdzanie czy atomy w siebie "wniknęły" po przemieszczeniu, jeżeli tak to oddalają się od siebie
            while 60 > (math.sqrt((pozx[j] - pozx[i]) ** 2 + (pozy[j] - pozy[i]) ** 2)) and i != j and i != odbicia[j]:
                pozycja_x[i] -= atom.speed_x/4
                pozycja_y[i] -= atom.speed_y/4
                atom.Rect.x = int(pozycja_x[i])
                atom.Rect.y = int(pozycja_y[i])

                pozycja_x[j] -= atom2.speed_x / 4
                pozycja_y[j] -= atom2.speed_y / 4
                atom2.Rect.x = int(pozycja_x[j])
                atom2.Rect.y = int(pozycja_y[j])
            #Odbicie
            if 60 < (math.sqrt((pozx[j] - pozx[i]) ** 2 + (pozy[j] - pozy[i]) ** 2)) <= 60 + 3 and i != j and i != \
                    odbicia[j]:
                atom1 = atomy[j]
                odbicia[j] = i
                odbicia[i] = j
                # tablica[kol] = 1
                # tablica[i] = 1
                xs = pozycja_x[i]
                ys = pozycja_y[i]
                xs1 = pozycja_x[j]
                ys1 = pozycja_y[j]
                n = [None, None]
                t = [None, None]
                n[0] = (xs1 - xs) / (((xs1 - xs) ** 2 + (ys1 - ys) ** 2) ** 0.5)
                n[1] = (ys1 - ys) / (((xs1 - xs) ** 2 + (ys1 - ys) ** 2) ** 0.5)
                t[0] = (-1.0 * (ys1 - ys)) / (((xs1 - xs) ** 2 + (ys1 - ys) ** 2) ** 0.5)
                t[1] = (xs1 - xs) / (((xs1 - xs) ** 2 + (ys1 - ys) ** 2) ** 0.5)
                v1 = [atom.speed_x, atom.speed_y]
                v2 = [atom1.speed_x, atom1.speed_y]
                vn1 = vt1 = vn2 = vt2 = 0
                for i in range(2):
                    vn1 += v1[i] * n[i]
                    vt1 += v1[i] * t[i]
                    vn2 += v2[i] * n[i]
                    vt2 += v2[i] * t[i]
                vn1, vn2 = vn2, vn1
                v1[0], v1[1], v2[0], v2[1] = vn1 * n[0] + vt1 * t[0], vn1 * n[1] + \
                                             vt1 * t[1], vn2 * n[0] + vt2 * t[0], vn2 * n[1] + vt2 * t[1]
                atom.speed_x, atom.speed_y, atom1.speed_x, atom1.speed_y = v1[0], v1[1], v2[0], v2[1]
        # współrzędne wskazują na lewy górny róg kwadratu który wypełnia kulka
        if atom.Rect.centerx - atom.r <= 0 and atom.speed_x < 0:
            # print("PYK")
            #print(atom.Rect.centerx - atom.r)
            # print(atom.Rect.centerx)
            #print(i, "SZYB:  ", atomy[i].speed_x)
            atom.speed_x *= -1
            # print(atomy[i].speed_x)
            odbicia[i] = -1
        elif atom.Rect.centerx + atom.r >= L and atom.speed_x > 0:
            atomy[i].Rect.x = L - atom.r * 2
            # print("pyk róg")
            atomy[i].speed_x *= -1
            odbicia[i] = -1
        elif atom.Rect.centery - atom.r <= 0 and atom.speed_y < 0:
            # print("pyk odbicie")
            atomy[i].Rect.y = 0
            atomy[i].speed_y *= -1
            odbicia[i] = -1
        elif atom.Rect.centery + atom.r >= H and atom.speed_y > 0:
            atomy[i].Rect.y = H - atom.r * 2
            atomy[i].speed_y *= -1
            odbicia[i] = -1
        '''if atom.Rect.x <= 0 or atom.Rect.x + 2 * atom.r >= L:  # współrzędne wskazują na lewy górny róg kwadratu który wypełnia kulka
            print("pyk róg")
            atom.speed_x *= -1
        elif atom.Rect.y <= 0 or atom.Rect.y + 2 * atom.r >= H:
            print("pyk odbicie")
            atom.speed_y *= -1

        if kol >= 0 and (odbicia[i] != kol or odbicia[kol] != i):
            atom1 = atomy[kol]
            odbicia[kol] = i
            odbicia[i] = kol
            #tablica[kol] = 1
            #tablica[i] = 1
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
            # print(atomy[i].speed_x, atomy[i].speed_y)
            # print(atomy[kol].speed_x, atomy[kol].speed_y)
            n = [None, None]
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
            v1[0], v1[1], v2[0], v2[1] = vn1 * n[0] + vt1 * t[0], vn1 * n[1] + \
                vt1 * t[1], vn2 * n[0] + vt2 * t[0], vn2 * n[1] + vt2 * t[1]
            atom.speed_x, atom.speed_y, atom1.speed_x, atom1.speed_y = v1[0], v1[1], v2[0], v2[1]
    print("_____________________________",atom.Rect.colliderect(atom1.Rect))'''
        pygame.draw.ellipse(screen, atom.col, atom.Rect)


"""_________________________________________________________________"""


czasowy.caption = f" γt = {krok_czasu_startowy}"
nowy_atom.caption = f"Atomy: {len(atomy)} "


# Pętla programu
while True:
    screen.fill((100, 100, 100))  # zmienia kolor tła okna
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # wyście iksem z okienka konczy program
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if jedenminus.mouse_over_button(pos) and etaH > 20:
                etaH -= 1
                H = etaH * R
                screen = pygame.display.set_mode((L, H + 40))
                jeden.caption = "etaH: " + str(etaH)
            elif jedenplus.mouse_over_button(pos) and etaH < 40:
                etaH += 1
                H = etaH * R
                screen = pygame.display.set_mode((L, H + 40))
                jeden.caption = "etaH: " + str(etaH)
            elif dwaplus.mouse_over_button(pos) and etaL < 40:
                etaL += 1
                L = etaL * R
                panel.rect.width = L
                screen = pygame.display.set_mode((L, H))
                dwa.caption = "etaL: " + str(etaL)
            elif dwaminus.mouse_over_button(pos) and etaL > 20:
                etaL -= 1
                L = etaL * R
                screen = pygame.display.set_mode((L, H))
                panel.rect.width = L
                dwa.caption = "etaL: " + str(etaL)
            elif czasowyminus.mouse_over_button(pos) and krok_czasu >= 10:
                krok_czasu -= 10
                czasowy.caption = "γt: " + str(krok_czasu)
            elif czasowyplus.mouse_over_button(pos):
                krok_czasu += 10
                czasowy.caption = "γt: " + str(krok_czasu)
            elif nowy_atom_plus.mouse_over_button(pos) and len(atomy) < (etaH * etaL / 4):
                dodaj(L, H, R, vGen)

                nowy_atom.caption = f"Atomy: {len(atomy)} "
            elif nowy_atom_minus.mouse_over_button(pos) and atomy:
                atomy.pop()
                nowy_atom.caption = f"Atomy: {len(atomy)} "

        elif event.type == pygame.VIDEORESIZE:
            L = event.w
            H = event.h
            panel.rect.width = L
            screen = pygame.display.set_mode(
                (event.w, event.h), pygame.RESIZABLE)

    # rysowanie menu
    rys_menu(screen)

    # poruszanie atomami
    ruch(screen, L, H)

    pygame.display.flip()  # wyświetla obiekty
    czas.tick(krok_czasu)  # spowalnia, max 60 klatek na sekundę
