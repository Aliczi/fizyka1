import pygame
import sys
import os
import math
import random


"""     Założenia projektu      """

eta = 20  # Warunek minimalnego rozmiaru zbiornika: nH, nL >= 20
# max 75 min 20
R = 30  # promień R
s = 2 * R  # średnica
H = eta * R  # wysokość zbiornika
L = eta * R  # szerokość zbiornika
vGen = 5  # Prędkość
tol = R / 10  # tolerancja zderzenia'
krok_czasu = 60  # ile klatek na sekundę
M = 5  # wartość M
ilosc = 20  # startowa ilosc atomow
krok_czasu_startowy = (vGen * eta)
nazwa_pliku = "M100A45.txt"


pygame.init()
czas = pygame.time.Clock()
os.environ['SDL_VIDEO_CENTERED'] = '1'

screen = pygame.display.set_mode((1480, 780), pygame.RESIZABLE)
pygame.display.set_caption("Symulacja atomów")


# ________________________________________________________________________________________________________
class Button():

    def __init__(self, x, y, width, height, color=(0, 0, 0), caption='', hover_color=''):
        self.x = x
        self.y = y
        self.caption = caption
        self.width = width
        self.height = height

        self.text_color = (0, 0, 0)
        self.color = color
        self.back_color = color
        self.hover_color = hover_color

    def draw(self, screen):

        pygame.draw.rect(screen, self.back_color,
                         (self.x, self.y, self.width, self.height))

        if self.caption != '':
            font = pygame.font.SysFont(
                "sitkasmallsitkatextitalicsitkasubheadingitalicsitkaheadingitalicsitkadisplayitalicsitkabanneritalic", 20)
            text = font.render(
                self.caption, 1, self.text_color, self.back_color)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

    def mouse_over_button(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] < self.y + self.height and pos[1] > self.y:
            self.back_color = self.hover_color
            self.text_color = (255, 255, 255)
            return True
        else:
            self.back_color = self.color
            self.text_color = (0, 0, 0)
            return False


# Button(pozycjax,pozycjay, szerokość, wysokość, kolor, napis, hover kolor)
top_color = (128, 0, 64)
top_color2 = (148, 20, 84)
hoverr = (108, 0, 24)

a = Button(100, 150, 300, 30, top_color, "Liczba atomów: ?", hoverr)
am = Button(400, 150, 50, 30, top_color2, "-", hoverr)
ap = Button(450, 150, 50, 30, top_color, "+", hoverr)

b = Button(100, 200, 300, 30, top_color, "Rozmiar zbiornika η: 40", hoverr)
bm = Button(400, 200, 50, 30, top_color2, "-", hoverr)
bp = Button(450, 200, 50, 30, top_color, "+", hoverr)

c = Button(100, 250, 300, 30, top_color, "Krok czasu δt: 100", hoverr)
cm = Button(400, 250, 50, 30, top_color2, "-", hoverr)
cp = Button(450, 250, 50, 30, top_color, "+", hoverr)

dd = Button(100, 300, 300, 30, top_color, "Wartość M: 5", hoverr)
dm = Button(400, 300, 50, 30, top_color2, "-", hoverr)
dp = Button(450, 300, 50, 30, top_color, "+", hoverr)

e = Button(100, 400, 300, 30, top_color, "Dokonaj pomiaru -> ", hoverr)
es = Button(400, 400, 100, 30, top_color2, "Start", hoverr)


f = Button(50, 460, 500, 30, top_color, "Liczba zderzeń: ?", hoverr)
g = Button(50, 500, 500, 30, top_color, "Przebyta droga: : ?", hoverr)
h = Button(50, 540, 500, 30, top_color, "Średnia droga λ: ?", hoverr)
i = Button(50, 580, 500, 30, top_color, "Ilość kolizji w czasie: ?", hoverr)
zap = Button(50, 660, 500, 30, top_color, "Zapisz do pliku", hoverr)

przyciski = [a, am, ap, b, bm, bp, c, cm, cp, dd, dm, dp, e, es, f, g, h, i]

# Zbiornik
con_x, con_y = 830, 190
frame = pygame.Rect(con_x - 8, con_y - 8, H + 16, L + 16)
container = pygame.Rect(con_x, con_y, H, L)

# tlo=pygame.image.load(os.path.join('wzory2.jpg')).convert_alpha()
# tlo = pygame.transform.scale(tlo,(1480,780))
RosyBrown = (188, 143, 143)
Maroon = (128, 0, 64)


def draw_setup(screen):
    screen.fill((155, 100, 100))  # zmienia kolor tła okna
    # screen.blit(tlo, (0, 0))
    pygame.draw.rect(screen, Maroon, frame)
    pygame.draw.rect(screen, RosyBrown, container)
    for el in przyciski:
        el.draw(screen)


"""Mechanika ruchu"""


class Atom():
    def __init__(self, x, y, speed_x, speed_y, s, kolor):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.x = x
        self.y = y
        self.odbicia = -1

        self.r = s / 2
        self.col = kolor

    def move(self, czas):
        self.x += self.speed_x
        self.y += self.speed_y

    def dystans(self, atom2):
        return (math.sqrt((atom2.x - self.x) ** 2 + (self.y - atom2.y) ** 2))

    # odbicia od ścian
    def sciana(self, top, bottom, left, right, i):

        # górnej
        if self.y - self.r <= top and self.speed_y < 0:
            self.y = top + self.r
            self.speed_y *= -1
            self.odbicia = -1

        # dolnej
        elif self.y + self.r >= bottom and self.speed_y > 0:
            self.y = bottom - self.r
            self.speed_y *= -1
            self.odbicia = -1

        # lewej
        elif self.x - self.r <= left and self.speed_x < 0:
            self.x = left + self.r
            self.speed_x *= -1
            self.odbicia = -1

        # prawej
        elif self.x + self.r >= right and self.speed_x > 0:
            self.x = right - atomy[i].r
            self.speed_x *= -1
            self.odbicia = -1


atomy = []  # lista atomów

"""________________________________Dodatkowy atom______________________________________"""
time = 0
lambdy = []
czerfony = Atom(con_x + R, con_y + R, random.uniform(-1.0 * vGen,
                                                     vGen), random.uniform(-1.0 * vGen, vGen), s, (255, 0, 0))
atomy.append(czerfony)


def dodaj(top, bottom, left, right, R, vGen):
    i = len(atomy)
    while i != 0:
        xx = random.uniform(left, right - R)
        yy = random.uniform(top, bottom - R)
        i = len(atomy)
        at = Atom(xx, yy, random.uniform(-1.0 * vGen, vGen),
                  random.uniform(-1.0 * vGen, vGen), s, (0, 0, 255))
        for j in range(len(atomy)):
            if (at.dystans(atomy[j])) <= s + tol:
                break

            i -= 1

    atomy.append(at)


def dodaj_on_click(xx, yy, R, vGen):
    atomy.append(Atom(xx, yy, random.uniform(-1.0 * vGen, vGen),
                      random.uniform(-1.0 * vGen, vGen), s, (0, 0, 255)))


def usun():
    atomy.pop()


def ruch(screen, top, bottom, left, right):
    global time, lambdy

    for i in range(len(atomy)):
        atomy[i].move(krok_czasu)
    for i in range(len(atomy)):
        # KOLIZJE Z ATOMAMI
        for j in range(i + 1, len(atomy)):
            if i == 0 or j == 0:
                pos1 = (atomy[0].x, atomy[0].y)
            # sprawdzanie czy atomy w siebie "wniknęły" po przemieszczeniu, jeżeli tak to oddalają się od siebie
            while s > atomy[i].dystans(atomy[j]) and i != j and (i != atomy[j].odbicia or j != atomy[i].odbicia):
                atomy[i].x -= (atomy[i].speed_x / 4)
                atomy[i].y -= (atomy[i].speed_y / 4)

                print("wnik")
                # atom.Rect.x = int(pozycja_x[i])
                # atom.Rect.y = int(pozycja_y[i])

                atomy[j].x -= (atomy[j].speed_x / 4)
                atomy[j].y -= (atomy[j].speed_y / 4)
                # atom2.Rect.x = int(pozycja_x[j])
                # atom2.Rect.y = int(pozycja_y[j])

            if i == 0 or j == 0:
                pos2 = (atomy[0].x, atomy[0].y)

                # sprawdzanie czy czerwony atom się przesunąl i oblizanie o ile

                if pos1 != pos2:
                    odl = math.sqrt((pos1[0] - pos2[0]) **
                                    2 + (pos1[1] - pos2[1]) ** 2)
                else:
                    odl = 0

            # Odbicie
            if s < atomy[i].dystans(atomy[j]) <= s + tol and (i != atomy[j].odbicia or j != atomy[i].odbicia):
                if i == 0 or j == 0:
                    lambdy.append(
                        math.sqrt((time * atomy[0].speed_x) ** 2 + (time * atomy[0].speed_y) ** 2) - odl)
                    print(i, j)

                    time = 0
                atomy[i].odbicia = j
                atomy[j].odbicia = i
                xs = atomy[i].x
                ys = atomy[i].y
                xs1 = atomy[j].x
                ys1 = atomy[j].y
                tupl = (xs - xs1,  # (r1 - r2)
                        ys - ys1)

                tupl2 = (xs1 - xs,  # (r2 - r1)
                         ys1 - ys)

                d = (tupl[0] ** 2) + (tupl[1] ** 2)

                dot1 = ((atomy[i].speed_x - atomy[j].speed_x) * tupl[0] + (
                        atomy[i].speed_y - atomy[j].speed_y) * tupl[1]) / d  # (dot/d)

                dot2 = ((atomy[j].speed_x - atomy[i].speed_x) * tupl2[0] + (  # drugi atom
                        atomy[j].speed_y - atomy[i].speed_y) * tupl2[1]) / d

                x1 = dot1 * tupl[0]
                y1 = dot1 * tupl[1]
                x2 = dot2 * tupl2[0]
                y2 = dot2 * tupl2[1]

                atomy[i].speed_x -= x1
                atomy[i].speed_y -= y1
                atomy[j].speed_x -= x2
                atomy[j].speed_y -= y2

        atomy[i].sciana(top, bottom, left, right, i)
        pygame.draw.circle(screen, atomy[i].col, (int(
            atomy[i].x), int(atomy[i].y)), int(atomy[i].r))


pomiar = False


for _ in range(ilosc):
    dodaj(con_y, con_y + H, con_x, con_x + L, R, vGen)
a.caption = f"Liczba atomów: {len(atomy)}"

# Pętla programu
while True:
    draw_setup(screen)
    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # wyście iksem z okienka konczy program
            pygame.quit()
            sys.exit()

        # klikanie
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # dodaj atom
            if ap.mouse_over_button(pos) and len(atomy) < (eta * eta / 4):
                dodaj(con_y, con_y + H, con_x, con_x + L, R, vGen)
                a.caption = f"Liczba atomów: {len(atomy)}"
            elif am.mouse_over_button(pos) and atomy:
                usun()
                a.caption = f"Liczba atomów: {len(atomy)}"
            elif pos[0] > con_x and pos[0] < con_x + L and pos[1] > con_y and pos[1] < con_y + H:
                dodaj_on_click(pos[0], pos[1], R, vGen)
                a.caption = f"Liczba atomów: {len(atomy)}"
            # zmiana rozmiaru zbiornika
            elif bm.mouse_over_button(pos) and eta > 20:
                eta -= 5
                H = eta * R
                L = eta * R
                con_x += R / 2 * 5
                con_y += R / 2 * 5
                container = pygame.Rect(con_x, con_y, H, L)
                frame = pygame.Rect(con_x - 5, con_y - 5, H + 10, L + 10)
                b.caption = f"Rozmiar zbiornika η: {eta}"
            elif bp.mouse_over_button(pos) and eta < 75:
                eta += 5
                H = eta * R
                L = eta * R
                con_x -= R / 2 * 5
                con_y -= R / 2 * 5
                container = pygame.Rect(con_x, con_y, H, L)
                frame = pygame.Rect(con_x - 5, con_y - 5, H + 10, L + 10)
                b.caption = f"Rozmiar zbiornika η: {eta}"
            # zmiana kroku czasu
            elif cm.mouse_over_button(pos) and krok_czasu >= 10:
                krok_czasu -= 10
                c.caption = f"Krok czasu δt: {krok_czasu}"
            elif cp.mouse_over_button(pos):
                krok_czasu += 10
                c.caption = f"Krok czasu δt: {krok_czasu}"
            # zmiana wartości M
            elif dm.mouse_over_button(pos) and M > 10:
                M -= 10
                dd.caption = f"Wartość M: {M}"
            elif dp.mouse_over_button(pos):
                M += 10
                dd.caption = f"Wartość M: {M}"
            elif es.mouse_over_button(pos):
                pomiar = True
                es.caption = "Czekaj"
                delta_t = M * krok_czasu
                lambdy = []
                time = 0
                f.caption = f"Liczba zderzeń : 0"
                g.caption = f"Przebyta droga: 0"
                h.caption = f"Średnia droga λ: 0"
                i.caption = f"Częstość zderzeń: 0"
            elif zap.mouse_over_button(pos):
                pl = open(nazwa_pliku, 'a')
                pl.write(str(odb))
                pl.write(" ")
                pl.write(str(droga))
                pl.write(" ")
                if (len(lambdy) > 0):
                    pl.write(str(srednia))
                else:
                    pl.write("0")
                pl.write(" ")
                pl.write(str(czestosc))
                pl.write("\n")

                pl.close()

        elif event.type == pygame.MOUSEMOTION:
            for przycisk in przyciski:
                przycisk.mouse_over_button(pos)

        elif event.type == pygame.VIDEORESIZE:
            # tlo = pygame.transform.scale(tlo, (event.w, event.h))
            screen = pygame.display.set_mode(
                (event.w, event.h), pygame.RESIZABLE)

    ruch(screen, con_y, con_y + H, con_x, con_x + L)

    pygame.display.flip()  # wyświetla obiekty
    czas.tick(krok_czasu)  # spowalnia, max 60 klatek na sekundę

    if pomiar:
        time += 1
        delta_t -= 1

        es.caption = f"{delta_t//60}:{delta_t%60}"
        if delta_t < 0:
            f.caption = f"Liczba zderzeń: {len(lambdy)}"
            odb = len(lambdy)
            g.caption = f"Przebyta droga: {round(sum(lambdy),4)}"
            droga = round(sum(lambdy), 4)
            h.caption = f"Średnia droga λ: {round(sum(lambdy)/len(lambdy),4)}"
            srednia = round(sum(lambdy) / len(lambdy), 4)
            i.caption = f"Częstość zderzeń: {round(len(lambdy)/(M * krok_czasu),4)}"
            czestosc = round(len(lambdy) / (M * krok_czasu), 4)
            pomiar = False
            es.caption = "Start"
            przyciski.append(zap)
