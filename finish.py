import pygame
import sys
import os
import math
import random

"""_______________________________Założenia projektu_____________________________________________"""

eta = 40                        # Warunek minimalnego rozmiaru zbiornika: nH, nL >= 20, max 75 min 20
R = 10                          # promień R
s = 2 * R                       # średnica
H = eta * R                     # wysokość zbiornika
L = eta * R                     # szerokość zbiornika
vGen = 3                        # zakres prędkości
tol = R / 10                    # tolerancja zderzenia
krok_czasu = vGen * 20          # ile klatek na sekundę
M = 10                          # wartość M
ilosc = 50                      # startowa ilosc atomow
nazwa_pliku = "M100A45.txt"
atomy = []                      # lista atomów
pomiar = False
delta_t = 0
time = 0
lambdy = []
coor = []

pygame.init()
czas = pygame.time.Clock()
os.environ['SDL_VIDEO_CENTERED'] = '1'

screen = pygame.display.set_mode((1480, 780), pygame.RESIZABLE)
pygame.time.set_timer(pygame.USEREVENT, 100)
pygame.display.set_caption("Symulacja atomów")

hand_cursor_string = (  # sized 16x24
    "                ",
    "    XX          ",
    "   X..X         ",
    "   X..X         ",
    "   X..X         ",
    "   X..XXX       ",
    "   X..X..XXX    ",
    "   X..X..X..XX  ",
    "   X..X..X..X.X ",
    "XXXX..X..X..X..X",
    "X..X........X..X",
    "X..X...........X",
    "X..............X",
    " X.............X",
    " X.............X",
    "  X............X",
    "  X...........X ",
    "   X..........X ",
    "   X..........X ",
    "    X........X  ",
    "    X........X  ",
    "    XXXXXXXXXX  ",
    "                ",
    "                ",)
datatuple, masktuple = pygame.cursors.compile(hand_cursor_string, black='.', white='X', xor='o')

"""________________________________________________________________________________________________________________"""


class Atom:
    def __init__(self, x, y, speed_x, speed_y, diameter, color):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.x = x
        self.y = y
        self.bounce = -1

        self.r = diameter / 2
        self.col = color

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def distance(self, atom2):
        return math.sqrt((atom2.x - self.x) ** 2 + (self.y - atom2.y) ** 2)

    # odbicia od ścian
    def walls(self, top, bottom, left, right):

        # górnej
        if self.y - self.r <= top:
            self.y = top + self.r
            self.speed_y *= -1
            self.bounce = -1

        # dolnej
        elif self.y + self.r >= bottom:
            self.y = bottom - self.r
            self.speed_y *= -1
            self.bounce = -1

        # lewej
        elif self.x - self.r <= left:
            self.x = left + self.r
            self.speed_x *= -1
            self.bounce = -1

        # prawej
        elif self.x + self.r >= right:
            self.x = right - self.r
            self.speed_x *= -1
            self.bounce = -1

    def new_velocity(self, atom):
        xs = self.x
        ys = self.y
        xs1 = atom.x
        ys1 = atom.y
        n = [None, None]
        t = [None, None]
        n[0] = (xs1 - xs) / (((xs1 - xs) ** 2 + (ys1 - ys) ** 2) ** 0.5)
        n[1] = (ys1 - ys) / (((xs1 - xs) ** 2 + (ys1 - ys) ** 2) ** 0.5)
        t[0] = (-1.0 * (ys1 - ys)) / (((xs1 - xs) ** 2 + (ys1 - ys) ** 2) ** 0.5)
        t[1] = (xs1 - xs) / (((xs1 - xs) ** 2 + (ys1 - ys) ** 2) ** 0.5)
        v1 = [self.speed_x, self.speed_y]
        v2 = [atom.speed_x, atom.speed_y]
        vn1 = vt1 = vn2 = vt2 = 0
        for i in range(2):
            vn1 += v1[i] * n[i]
            vt1 += v1[i] * t[i]
            vn2 += v2[i] * n[i]
            vt2 += v2[i] * t[i]
        vn1, vn2 = vn2, vn1
        v1[0], v1[1], v2[0], v2[1] = vn1 * n[0] + vt1 * t[0], vn1 * n[1] + vt1 * t[1], vn2 * n[0] + vt2 * t[0], vn2 * n[
            1] + vt2 * t[1]
        self.speed_x, self.speed_y, atom.speed_x, atom.speed_y = v1[0], v1[1], v2[0], v2[1]

    def check_distance(self, atom):

        a_road = math.sqrt((atom.x - (self.x - self.speed_x / 10)) ** 2 + (atom.y - (self.y - self.speed_y / 10)) ** 2)
        b_road = math.sqrt((self.x - (atom.x - atom.speed_x / 10)) ** 2 + (self.y - (atom.y - atom.speed_y / 10)) ** 2)
        c_road = math.sqrt((atom.x - self.x) ** 2 + ((self.y - self.speed_y / 10) - (atom.y - atom.speed_y / 10)) ** 2)
        d_road = math.sqrt(((self.x - self.speed_x / 10) - (atom.x - atom.speed_x / 10)) ** 2 + (self.y - atom.y) ** 2)
        e_road = math.sqrt(((self.x - self.speed_x / 10) - (atom.x - atom.speed_x / 10)) ** 2
                           + ((self.y - self.speed_y / 10) - (atom.y - atom.speed_y / 10)) ** 2)

        list = [a_road, b_road, c_road, d_road, e_road]
        if a_road == max(list):
            return "a"
        elif b_road == max(list):
            return "b"
        if c_road == max(list):
            return "c"
        if d_road == max(list):
            return "d"
        else:
            return "e"


def random_coordinates(top, bottom, left, right):
    first_x = random.uniform(left, right - R)
    first_y = random.uniform(top, bottom - R)
    x_list = [first_x]
    y_list = [first_y]
    i = first_x
    j = first_y
    while i < right - 3 * R:
        i += 2 * R + 2
        x_list.append(i)
    i = first_x

    while i > left + 3 * R:
        i -= 2 * R + 2
        x_list.append(i)

    while j < bottom - 3 * R:
        j += 2 * R + 2
        y_list.append(j)
    j = first_y

    while j > top + 3 * R:
        j -= 2 * R + 2
        y_list.append(j)

    for el in x_list:
        for ele in y_list:
            coor.append((el, ele))
    coor.sort()
    coor.pop(0)


def add_atoms(ile):
    coordinates = random.sample(coor, ile)
    for i in range(ile):
        xx = coordinates[i][0]
        yy = coordinates[i][1]
        speed_x, speed_y = random.uniform(-1.0 * vGen, vGen), random.uniform(-1.0 * vGen, vGen)
        atomy.append(Atom(xx, yy, speed_x, speed_y, s, (0, 0, 200)))


def add_on_click(xx, yy):
    atomy.append(Atom(xx, yy, random.uniform(-1.0 * vGen, vGen), random.uniform(-1.0 * vGen, vGen), s, (0, 0, 200)))


def delete():
    atomy.pop()


def ruch(window, top, bottom, left, right):
    global time, lambdy
    odl = 0

    for i in range(len(atomy)):

        """____________________________________ KOLIZJE Z ATOMAMI_______________________________________"""
        for j in range(i + 1, len(atomy)):

            # Sprawdzenie ewentualnej kolizji
            if s <= atomy[i].distance(atomy[j]) <= s + tol and (i != atomy[j].bounce or j != atomy[i].bounce):
                if i == 0 or j == 0:
                    lambdy.append(math.sqrt((time * atomy[0].speed_x) ** 2 + (time * atomy[0].speed_y) ** 2))
                    time = 0

                atomy[i].bounce = j
                atomy[j].bounce = i
                atomy[i].new_velocity(atomy[j])

            # Sprawdzanie czy po przemieszczeniu atomy w siebie "wniknęły"
            elif s > atomy[i].distance(atomy[j]) and (i != atomy[j].bounce or j != atomy[i].bounce):

                # Zapisanie pozycji czerwonego atomu przed oddaleniem atomów
                if i == 0 or j == 0:
                    pos1 = (atomy[0].x, atomy[0].y)

                # Znalezienie optymalnego sposobu rozdzielenia atomów
                ans = atomy[i].check_distance(atomy[j])

                # Oddalenie od siebie atomów
                while s > atomy[i].distance(atomy[j]):
                    if ans == "a":
                        atomy[i].x -= atomy[i].speed_x / 30
                        atomy[i].y -= atomy[i].speed_y / 30
                    elif ans == "b":
                        atomy[j].x -= atomy[j].speed_x / 30
                        atomy[j].y -= atomy[j].speed_y / 30
                    elif ans == "d":
                        atomy[i].x -= atomy[i].speed_x / 30
                        atomy[j].x -= atomy[j].speed_x / 30
                    elif ans == "c":
                        atomy[i].y -= atomy[i].speed_y / 30
                        atomy[j].y -= atomy[j].speed_y / 30
                    else:
                        atomy[i].x -= atomy[i].speed_x / 30
                        atomy[i].y -= atomy[i].speed_y / 30
                        atomy[j].x -= atomy[j].speed_x / 30
                        atomy[j].y -= atomy[j].speed_y / 30

                # Zapisanie pozycji czerwonego atomu po oddaleniu atomów
                if i == 0 or j == 0:
                    pos2 = (atomy[0].x, atomy[0].y)

                    # Sprawdzenie o jaką odległość czerwony atom się cofnął
                    if pos1 != pos2:
                        odl = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
                    else:
                        odl = 0

                if i == 0 or j == 0:
                    lambdy.append(math.sqrt((time * atomy[0].speed_x) ** 2 + (time * atomy[0].speed_y) ** 2) - odl)
                    time = 0

                atomy[i].bounce = j
                atomy[j].bounce = i
                atomy[i].new_velocity(atomy[j])

        atomy[i].walls(top, bottom, left, right)
        atomy[i].move()
        pygame.draw.circle(window, atomy[i].col, (int(atomy[i].x), int(atomy[i].y)), int(atomy[i].r))


class Button:
    def __init__(self, x, y, width, height, color=(0, 0, 0), caption='', hover_color=(0, 0, 0), hand=False):
        self.x = x
        self.y = y
        self.caption = caption
        self.width = width
        self.height = height

        self.text_color = (0, 0, 0)
        self.color = color
        self.back_color = color
        self.hover_color = hover_color
        self.hand = hand

    def draw(self, window):
        pygame.draw.rect(window, (20, 20, 20), (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(window, self.back_color, (self.x, self.y, self.width, self.height))

        if self.caption != '':
            font = pygame.font.SysFont(
                "sitkasmallsitkatextitalicsitkasubheadingitalicsitkaheadingitalicsitkadisplayitalicsitkabanneritalic",
                20)
            text = font.render(self.caption, 1, self.text_color, self.back_color)
            window.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y
                               + (self.height / 2 - text.get_height() / 2)))

    def mouse_over_button(self, poz):
        if self.x < poz[0] < self.x + self.width and self.y + self.height > poz[1] > self.y:
            self.back_color = self.hover_color
            self.text_color = (255, 255, 255)
            if self.hand:
                pygame.mouse.set_cursor((16, 24), (0, 0), datatuple, masktuple)
            return True
        else:
            self.back_color = self.color
            self.text_color = (0, 0, 0)
            return False


# Button(pozycjax,pozycjay, szerokość, wysokość, kolor, napis, hover kolor, kursor rączki)
button_color1 = (128, 0, 64)
button_color2 = (148, 20, 84)
hover_color = (108, 0, 24)

a = Button(100, 150, 300, 30, button_color1, "Liczba atomów: 50", hover_color)
am = Button(400, 150, 50, 30, button_color2, "-", hover_color, True)
ap = Button(450, 150, 50, 30, button_color1, "+", hover_color, True)

b = Button(100, 200, 300, 30, button_color1, "Rozmiar zbiornika η: 40", hover_color)
bm = Button(400, 200, 50, 30, button_color2, "-", hover_color, True)
bp = Button(450, 200, 50, 30, button_color1, "+", hover_color, True)

c = Button(100, 250, 300, 30, button_color1, "Krok czasu δt: 60", hover_color)
cm = Button(400, 250, 50, 30, button_color2, "-", hover_color, True)
cp = Button(450, 250, 50, 30, button_color1, "+", hover_color, True)

dd = Button(100, 300, 300, 30, button_color1, "Wartość M: 10", hover_color)
dm = Button(400, 300, 50, 30, button_color2, "-", hover_color, True)
dp = Button(450, 300, 50, 30, button_color1, "+", hover_color, True)

e = Button(100, 400, 300, 30, button_color1, "Dokonaj pomiaru -> ", hover_color)
es = Button(400, 400, 100, 30, button_color2, "Start", hover_color, True)

f = Button(50, 460, 500, 30, button_color1, "Liczba zderzeń: ?", hover_color)
g = Button(50, 500, 500, 30, button_color1, "Przebyta droga: : ?", hover_color)
h = Button(50, 540, 500, 30, button_color1, "Średnia droga λ: ?", hover_color)
i = Button(50, 580, 500, 30, button_color1, "Ilość kolizji w czasie: ?", hover_color)
zap = Button(50, 660, 500, 30, button_color1, "Zapisz do pliku", hover_color, True)

przyciski = [a, am, ap, b, bm, bp, c, cm, cp, dd, dm, dp, e, es, f, g, h, i]

# Zbiornik
con_x, con_y = 830, 190
frame = pygame.Rect(con_x - 8, con_y - 8, H + 16, L + 16)
container = pygame.Rect(con_x, con_y, H, L)

# wczytywanie tła
# tlo = pygame.image.load(os.path.join('wzory2.jpg')).convert_alpha()
# tlo = pygame.transform.scale(tlo, (1480, 780))


def draw_setup(window):
    window.fill((20, 20, 20))  # zmienia kolor tła okna
    # window.blit(tlo, (0, 0))
    pygame.draw.rect(window, (128, 0, 64), frame)
    pygame.draw.rect(window, (188, 143, 143), container)
    for el in przyciski:
        el.draw(window)


random_coordinates(con_y, con_y + H, con_x, con_x + L)
add_atoms(ilosc)


"""___________________________________________Pętla programu_____________________________________________________"""
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
                atomy = []
                ilosc += 5
                add_atoms(ilosc)
                a.caption = f"Liczba atomów: {len(atomy)}"
            elif am.mouse_over_button(pos) and atomy:
                for _ in range(5):
                    delete()
                ilosc -= 5
                a.caption = f"Liczba atomów: {len(atomy)}"
            elif con_x < pos[0] < con_x + L and con_y < pos[1] < con_y + H:
                add_on_click(pos[0], pos[1])
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
                random_coordinates(con_y, con_y + H, con_x, con_x + L)
                atomy = []
                add_atoms(ilosc)
            elif bp.mouse_over_button(pos) and eta < 75:
                eta += 5
                H = eta * R
                L = eta * R
                con_x -= R / 2 * 5
                con_y -= R / 2 * 5
                container = pygame.Rect(con_x, con_y, H, L)
                frame = pygame.Rect(con_x - 5, con_y - 5, H + 10, L + 10)
                b.caption = f"Rozmiar zbiornika η: {eta}"
                random_coordinates(con_y, con_y + H, con_x, con_x + L)
                atomy = []
                add_atoms(ilosc)
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
                atomy = []
                czerfony = Atom(con_x + R, con_y + R, random.uniform(-1.0 * vGen, vGen), random.uniform
                (-1.0 * vGen, vGen), s, (200, 0, 0))
                atomy.append(czerfony)
                add_atoms(ilosc)
                delta_t = M * krok_czasu
                lambdy = []
                time = 0
                a.caption = f"Liczba atomów: {len(atomy)}"
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
                if len(lambdy) > 0:
                    pl.write(str(srednia))
                else:
                    pl.write("0")
                pl.write(" ")
                pl.write(str(czestosc))
                pl.write("\n")

                pl.close()

        elif event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            for przycisk in przyciski:
                przycisk.mouse_over_button(pos)

        elif event.type == pygame.VIDEORESIZE:
            # tlo = pygame.transform.scale(tlo, (event.w, event.h))
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        elif event.type == pygame.USEREVENT:
            delta_t -= 1

    ruch(screen, con_y, con_y + H, con_x, con_x + L)

    pygame.display.flip()  # wyświetla obiekty
    czas.tick(krok_czasu)  # spowalnia, max 60 klatek na sekundę

    if pomiar:
        time += 1
        es.caption = f"{delta_t // 10}:{delta_t % 10}"
        if delta_t < 0:
            odb = len(lambdy)
            f.caption = f"Liczba zderzeń: {odb}"
            droga = round(sum(lambdy), 4)
            g.caption = f"Przebyta droga: {droga}"
            srednia = round(sum(lambdy) / len(lambdy), 4)
            h.caption = f"Średnia droga λ: {srednia}"
            czestosc = round(len(lambdy) / (M * krok_czasu), 4)
            i.caption = f"Częstość zderzeń: {czestosc}"
            pomiar = False
            es.caption = "Start"
            przyciski.append(zap)
            atomy.pop(0)
