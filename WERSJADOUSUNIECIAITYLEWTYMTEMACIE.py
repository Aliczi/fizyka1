import pygame
import sys
import os
import math
import random

"""     Założenia projektu      """

eta = 40        # Warunek minimalnego rozmiaru zbiornika: nH, nL >= 20, max 75 min 20
R = 10  # promień R
s = 2 * R  # średnica
H = eta * R  # wysokość zbiornika
L = eta * R  # szerokość zbiornika
vGen = 3  # Prędkość
tol = R / 10  # tolerancja zderzenia'
krok_czasu = vGen*20     # ile klatek na sekundę
M = 5                    # wartość M
ilosc = 100  # startowa ilosc atomow
krok_czasu_startowy = (vGen * eta)
nazwa_pliku = "M100A45.txt"
atomy = []  # lista atomów
pomiar = False
delta_t = 0


pygame.init()
czas = pygame.time.Clock()
os.environ['SDL_VIDEO_CENTERED'] = '1'

screen = pygame.display.set_mode((1480, 780), pygame.RESIZABLE)
pygame.time.set_timer(pygame.USEREVENT, 100)
pygame.display.set_caption("Symulacja atomów")


thickarrow_strings = (            # sized 16x24
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
datatuple, masktuple = pygame.cursors.compile(thickarrow_strings, black='.', white='X', xor='o')


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
        pygame.draw.rect(window, (0, 0, 0), (self.x-2, self.y-2, self.width+4, self.height+4))
        pygame.draw.rect(window, self.back_color, (self.x, self.y, self.width, self.height))

        if self.caption != '':
            font = pygame.font.SysFont(
                "sitkasmallsitkatextitalicsitkasubheadingitalicsitkaheadingitalicsitkadisplayitalicsitkabanneritalic",
                20)
            text = font.render(self.caption, 1, self.text_color, self.back_color)
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y
                               + (self.height/2 - text.get_height()/2)))

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


# Button(pozycjax,pozycjay, szerokość, wysokość, kolor, napis, hover kolor)
top_color = (128, 0, 64)
top_color2 = (148, 20, 84)
hoverr = (108, 0, 24)

a = Button(100, 150, 300, 30, top_color, "Liczba atomów: ?", hoverr)
am = Button(400, 150, 50, 30, top_color2, "-", hoverr, True)
ap = Button(450, 150, 50, 30, top_color, "+", hoverr, True)

b = Button(100, 200, 300, 30, top_color, "Rozmiar zbiornika η: 40", hoverr)
bm = Button(400, 200, 50, 30, top_color2, "-", hoverr, True)
bp = Button(450, 200, 50, 30, top_color, "+", hoverr, True)

c = Button(100, 250, 300, 30, top_color, "Krok czasu δt: 100", hoverr)
cm = Button(400, 250, 50, 30, top_color2, "-", hoverr, True)
cp = Button(450, 250, 50, 30, top_color, "+", hoverr, True)

dd = Button(100, 300, 300, 30, top_color, "Wartość M: 5", hoverr)
dm = Button(400, 300, 50, 30, top_color2, "-", hoverr, True)
dp = Button(450, 300, 50, 30, top_color, "+", hoverr, True)

e = Button(100, 400, 300, 30, top_color, "Dokonaj pomiaru -> ", hoverr)
es = Button(400, 400, 100, 30, top_color2, "Start", hoverr, True)


f = Button(50, 460, 500, 30, top_color, "Liczba zderzeń: ?", hoverr)
g = Button(50, 500, 500, 30, top_color, "Przebyta droga: : ?", hoverr)
h = Button(50, 540, 500, 30, top_color, "Średnia droga λ: ?", hoverr)
i = Button(50, 580, 500, 30, top_color, "Ilość kolizji w czasie: ?", hoverr)
zap = Button(50, 660, 500, 30, top_color, "Zapisz do pliku", hoverr, True)

przyciski = [a, am, ap, b, bm, bp, c, cm, cp, dd, dm, dp, e, es, f, g, h, i]

# Zbiornik
con_x, con_y = 830, 190
frame = pygame.Rect(con_x-8, con_y-8, H+16, L+16)
container = pygame.Rect(con_x, con_y, H, L)

tlo = pygame.image.load(os.path.join('wzory2.jpg')).convert_alpha()
tlo = pygame.transform.scale(tlo, (1480, 780))
RosyBrown = (188, 143, 143)
Maroon = (128, 0, 64)


def draw_setup(window):
    window.fill((155, 100, 100))  # zmienia kolor tła okna
    window.blit(tlo, (0, 0))
    pygame.draw.rect(window, Maroon, frame)
    pygame.draw.rect(window, RosyBrown, container)
    for el in przyciski:
        el.draw(window)


"""Mechanika ruchu"""


class Atom:
    def __init__(self, x, y, speed_x, speed_y, diameter, kolor):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.x = x
        self.y = y
        self.bounce = -1

        self.r = diameter / 2
        self.col = kolor

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def dystans(self, atom2):
        return math.sqrt((atom2.x - self.x) ** 2 + (self.y - atom2.y) ** 2)

    # odbicia od ścian
    def sciana(self, top, bottom, left, right):

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

    def which_closer(self, atom):
        s=math.sqrt((atom.x - self.x) ** 2 + (self.y - atom.y) ** 2)
        ale = self.y - self.speed_y / 10
        ble = self.x - self.speed_x / 10
        sself = math.sqrt((atom.x - ble) ** 2 + (ale - atom.y) ** 2)
        cle = atom.y - atom.speed_y / 10
        dle = atom.x - atom.speed_x / 10
        satom = math.sqrt((dle - self.x) ** 2 + (self.y - cle) ** 2)

        if sself>satom:
            return True
        else:
            return False


"""________________________________Dodatkowy atom______________________________________"""
time = 0
lambdy = []


coor = []
def ustalanie_pozycji(top, bottom, left, right):
    l=[]
    l2=[]
    liczba = random.uniform(left, right - R)
    licz = random.uniform(top, bottom - R )
    i=liczba
    ii=liczba
    j=licz
    jj=licz
    l.append(i)
    l2.append(j)
    while ii > left + 3*R:
        ii -= 2* R + 2
        l.append(ii)

    while i < right - 3*R:
        i += 2 * R + 2
        l.append(i)

    l.sort()
    while jj > top + 3*R:
        jj -= 2 * R + 2
        l2.append(jj)

    while j < bottom - 3*R:
        j += 2 * R + 2
        l2.append(j)
    l2.sort()
    for el in l:
        for le in l2:
            coor.append((el,le))
    coor.sort()
    coor.pop(0)


ustalanie_pozycji(con_y, con_y+H, con_x,con_x+L)



def dodaj(ile):
    co=random.sample(coor, ile)
    for i in range(ile):
        xx=co[i][0]
        yy=co[i][1]
        sx,sy = random.uniform(-1.0 * vGen, vGen), random.uniform(-1.0 * vGen, vGen)
        atomy.append(Atom(xx, yy, sx,sy, 2*R, (0, 0, 255)))
        sprawd.append((xx,yy,sx,sy))

def dodaj2(top, bottom, left, right):
    length = len(atomy)
    at = None
    while length != 0:
        xx = random.uniform(left, right - R)
        yy = random.uniform(top, bottom - R)
        length = len(atomy)
        at = Atom(xx, yy, random.uniform(-1.0 * vGen, vGen), random.uniform(-1.0 * vGen, vGen), s, (0, 0, 255))
        for j in range(len(atomy)):
            if (at.dystans(atomy[j])) <= s + tol:
                break
            length -= 1
    atomy.append(at)




def dodaj_on_click(xx, yy):
    atomy.append(Atom(xx, yy, random.uniform(-1.0 * vGen, vGen), random.uniform(-1.0 * vGen, vGen), s, (0, 0, 255)))


def usun():
    atomy.pop()

aaa=0
bbb=0
ccc=0
ddd=0
def ruch(window, top, bottom, left, right):
    global time, lambdy
    odl = 0
    pos1 = None

    for i in range(len(atomy)):
        # KOLIZJE Z ATOMAMI
        for j in range(i + 1, len(atomy)):
            # print("oooooooooooooooooooooooooooooooooooooooooooooo")
            wnik = False
            if i == 0 or j == 0:
                pos1 = (atomy[0].x, atomy[0].y)

            # Odbicie
            if s  <= atomy[i].dystans(atomy[j]) <= s + tol  and (i != atomy[j].bounce or j != atomy[i].bounce):
                # print("ładnie")
                # print(atomy[i].dystans(atomy[j]))
                if i == 0 or j == 0:
                    lambdy.append(
                        math.sqrt((time * atomy[0].speed_x) ** 2 + (time * atomy[0].speed_y) ** 2))

                    time = 0

                atomy[i].bounce = j
                atomy[j].bounce = i
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

            # sprawdzanie czy atomy w siebie "wniknęły" po przemieszczeniu, jeżeli tak to oddalają się od siebie
            elif s > atomy[i].dystans(atomy[j]) and (i != atomy[j].bounce or j != atomy[i].bounce):
                # print("A", atomy[0].x, atomy[0].y, atomy[1].x, atomy[1].y)
                while s > atomy[i].dystans(atomy[j]):
                    global aaa, bbb, ccc, ddd,aa,bb,cc,dd

                    if atomy[i].speed_x*atomy[j].speed_x < 0 and atomy[i].speed_y*atomy[j].speed_y >= 0:
                        # print("ifxxxxxxxxxxx")
                        # print(atomy[i].dystans(atomy[j]))
                        aaa=1
                        atomy[i].x -= atomy[i].speed_x / 30
                        atomy[j].x -= atomy[j].speed_x / 30
                        if i == 91 and j == 91:
                            print("if",i, j, s, atomy[i].dystans(atomy[j]), atomy[i].x, atomy[i].y, atomy[j].x, atomy[j].y)

                    elif atomy[i].speed_x*atomy[j].speed_x >= 0 and atomy[i].speed_y*atomy[j].speed_y < 0:
                        # print("elifyyyyy")
                        # print(atomy[i].dystans(atomy[j]))
                        bbb=1
                        atomy[i].y -= atomy[i].speed_y / 30
                        atomy[j].y -= atomy[j].speed_y / 30
                        if i == 91 and j == 91:
                            print("elif",i, j, s, atomy[i].dystans(atomy[j]), atomy[i].x, atomy[i].y, atomy[j].x, atomy[j].y)
                    elif atomy[i].speed_x * atomy[j].speed_x >= 0 and atomy[i].speed_y * atomy[j].speed_y >= 0:
                        # print("elifffxxxxxxxxxxxxyyyyyyyyyyyyyyy", atomy[i].dystans((atomy[j])))
                        ccc=1
                        if atomy[i].which_closer(atomy[j]) and  i!=1:
                            print(True, atomy[i].dystans(atomy[j]))
                            atomy[i].y -= atomy[i].speed_y / 10
                            atomy[i].x -= atomy[i].speed_x / 10
                        else:
                            if i!=1:
                                print(False)
                                atomy[j].y -= atomy[j].speed_y / 10
                                atomy[j].x -= atomy[j].speed_x / 10

                        if i==1:
                            print("111111111111111111111111111")
                            atomy[j].y -= atomy[j].speed_y / 10
                            atomy[j].x -= atomy[j].speed_x / 10
                        else:
                            atomy[i].y -= atomy[i].speed_y / 10
                            atomy[i].x -= atomy[i].speed_x / 10

                        if i == 91 and j == 91:
                            print("elif", i, j, s, atomy[i].dystans(atomy[j]), atomy[i].x, atomy[i].y, atomy[j].x,
                                  atomy[j].y)

                    else:
                        # print("elseee", atomy[i].dystans(atomy[j]), atomy[i].speed_x * atomy[j].speed_x, atomy[i].speed_y * atomy[j].speed_y)
                        ddd=1
                        if i==1:
                            print("111111111111111111111111111")
                            atomy[i].x -= atomy[i].speed_x / 30
                            atomy[i].y -= atomy[i].speed_y / 30

                            atomy[j].x += atomy[j].speed_x / 30
                            atomy[j].y += atomy[j].speed_y / 30
                        else:
                            atomy[i].x -= atomy[i].speed_x / 30
                            atomy[i].y -= atomy[i].speed_y / 30

                            atomy[j].x -= atomy[j].speed_x / 30
                            atomy[j].y -= atomy[j].speed_y / 30
                        # print("elseee2", atomy[i].dystans(atomy[j]))
                        # if j == 91 or i == 91:
                        #     print("else",i, j, s, atomy[i].dystans(atomy[j]), atomy[i].x, atomy[i].y, atomy[j].x, atomy[j].y)
                    # print("B",atomy[0].x, atomy[0].y, atomy[1].x, atomy[1].y)

                #     h=s-atomy[i].dystans(atomy[j])
                #     atomy[i].x -= atomy[i].speed_x /6
                #     atomy[i].y -= atomy[i].speed_y/6
                #
                #     atomy[j].x -= atomy[j].speed_x/6
                #     atomy[j].y -= atomy[j].speed_y/6
                #
                #
                #
                # # while 19.2 > atomy[i].dystans(atomy[j]):
                # #     h = s - atomy[i].dystans(atomy[j])
                # #     atomy[i].x -= atomy[i].speed_x / 6
                # #     atomy[i].y -= atomy[i].speed_y / 6
                # #
                # #     atomy[j].x -= atomy[j].speed_x / 6
                # #     atomy[j].y -= atomy[j].speed_y / 6
                # #
                # #     break

                    if i == 32 and j== 84:
                        print(i, j, s, atomy[i].dystans(atomy[j]), atomy[i].x, atomy[i].y, atomy[j].x, atomy[j].y)
                aa+=aaa
                bb+=bbb
                cc+=ccc
                dd+=ddd
                aaa, bbb, ccc, ddd = 0, 0, 0, 0
                if i == 0 or j == 0:
                    pos2 = (atomy[0].x, atomy[0].y)

                    # sprawdzanie czy czerwony atom się przesunąl i oblizanie o ile

                    if pos1 != pos2:
                        odl = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
                    else:
                        odl = 0

                if i == 0 or j == 0:
                    lambdy.append(
                        math.sqrt((time * atomy[0].speed_x) ** 2 + (time * atomy[0].speed_y) ** 2) - odl)

                    time = 0

                # print(atomy[i].dystans(atomy[j]))

                atomy[i].bounce = j
                atomy[j].bounce = i
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

                atomy[i].x += atomy[i].speed_x
                atomy[i].y += atomy[i].speed_y
                atomy[j].x += atomy[j].speed_x
                atomy[j].y += atomy[j].speed_y


        atomy[i].sciana(top, bottom, left, right)
        atomy[i].move()
        if i!=32 or i ==91 or i==84:
            pygame.draw.circle(window, atomy[i].col, (int(atomy[i].x), int(atomy[i].y)), int(atomy[i].r))

sprawd = [(1027.6109254209348, 503.6284721142879, 0.49178809897750764, 0.7322518848207091), (1115.6109254209348, 393.6284721142879, 0.3308466332354165, 0.5201583671907808), (895.6109254209348, 349.6284721142879, -0.3706799679057078, 0.34941294857806393), (917.6109254209348, 547.6284721142879, 0.6395131993108691, 0.6821387741299871), (895.6109254209348, 525.6284721142879, 0.4530200222536933, 0.4199676903358778), (961.6109254209348, 393.6284721142879, 0.5552717862388832, 0.9293834176078808), (1049.6109254209348, 349.6284721142879, -0.43206640518694295, 0.635034387742025), (895.6109254209348, 503.6284721142879, -0.8352465457887008, -0.4229279481455257), (873.6109254209348, 437.6284721142879, 0.4149434129209719, -0.6867703056966257), (1203.6109254209348, 415.6284721142879, 0.635574032901399, 0.15663507247935438), (1137.6109254209348, 261.6284721142879, -0.24543300542744628, -0.3633447436338857), (1005.6109254209348, 569.6284721142879, 0.5954336208458151, -0.1505833216039445), (1071.6109254209348, 503.6284721142879, 0.5857814366767502, -0.23550251424914204), (1027.6109254209348, 349.6284721142879, 0.9875065306330248, -0.41027918728461255), (961.6109254209348, 261.6284721142879, 0.3066564703994632, -0.9165531823479476), (1005.6109254209348, 503.6284721142879, -0.6786538847852406, -0.7345275922538386), (1181.6109254209348, 305.6284721142879, -0.01090212155944803, -0.5681438995883499), (1181.6109254209348, 327.6284721142879, 0.6114376390656089, 0.8378173336909562), (1203.6109254209348, 393.6284721142879, 0.8044730099273438, 0.9369143065609218), (851.6109254209348, 503.6284721142879, 0.5853736220820926, 0.05294748067856814), (1071.6109254209348, 569.6284721142879, -0.15812045788674234, 0.7921551883205022), (983.6109254209348, 393.6284721142879, -0.01608752486337206, -0.7652280233116888), (1137.6109254209348, 547.6284721142879, 0.5823599270269104, -0.24200277673182935), (1049.6109254209348, 481.6284721142879, -0.7509023752736277, 0.49977710407923515), (983.6109254209348, 327.6284721142879, 0.8436504056102541, 0.9344496979821366), (1159.6109254209348, 415.6284721142879, -0.41655635683211023, -0.08586344247511701), (895.6109254209348, 393.6284721142879, -0.9074846345999628, 0.4437632072319564), (1115.6109254209348, 437.6284721142879, 0.7674550785151457, -0.41672637244651867), (917.6109254209348, 283.6284721142879, 0.12587723700774012, -0.14560705265339746), (939.6109254209348, 525.6284721142879, 0.3454615188532366, -0.219109634187449), (961.6109254209348, 569.6284721142879, 0.4389548040721407, -0.3755048124284197), (1049.6109254209348, 261.6284721142879, -0.9718914504174507, -0.6637436699948749), (983.6109254209348, 305.6284721142879, -0.7444824375330075, 0.03035813630505446), (939.6109254209348, 217.6284721142879, 0.6497686453496159, 0.45173472993067576), (873.6109254209348, 393.6284721142879, -0.33575928389245324, -0.9180593924452134), (1203.6109254209348, 525.6284721142879, 0.3191048832515686, -0.5873505651603113), (1181.6109254209348, 415.6284721142879, -0.05547550401518442, -0.79318615949866), (1049.6109254209348, 525.6284721142879, 0.12110353529606965, 0.13237215550455073), (851.6109254209348, 481.6284721142879, 0.627760193051603, -0.29939527182646986), (1005.6109254209348, 305.6284721142879, -0.20523419552398803, -0.4727787519022111), (1049.6109254209348, 371.6284721142879, 0.11334713638764371, 0.20675633460503096), (1159.6109254209348, 525.6284721142879, 0.2240596031967388, 0.3351199455276588), (873.6109254209348, 459.6284721142879, -0.6528772563580736, 0.8790365048821243), (917.6109254209348, 437.6284721142879, 0.7598766928762286, 0.4613490159055309), (1203.6109254209348, 283.6284721142879, 0.7454676634773909, 0.6322838446251986), (917.6109254209348, 393.6284721142879, 0.5716818743701548, 0.2499271821393585), (983.6109254209348, 525.6284721142879, 0.8949564366128244, 0.13804221733738586), (1181.6109254209348, 283.6284721142879, 0.252434603892552, 0.8469960900406321), (961.6109254209348, 415.6284721142879, 0.7934810243049653, 0.2096707435332501), (851.6109254209348, 437.6284721142879, 0.6839440027692474, -0.6520560478713797), (1049.6109254209348, 327.6284721142879, -0.774030390360853, 0.11843874468870275), (1027.6109254209348, 217.6284721142879, -0.009121785285430617, -0.9285770104311213), (1027.6109254209348, 525.6284721142879, -0.4944351061527168, -0.9111916211944486), (939.6109254209348, 305.6284721142879, 0.15276335579341183, -0.2471480925677314), (851.6109254209348, 415.6284721142879, 0.3522701765259584, 0.7095978406567727), (1093.6109254209348, 547.6284721142879, 0.21338996684082367, 0.2681764808183442), (851.6109254209348, 327.6284721142879, 0.8772136902174914, -0.21973563498675963), (1093.6109254209348, 239.6284721142879, -0.2938223698821407, 0.24953388786044095), (1203.6109254209348, 327.6284721142879, -0.8789288561654263, -0.8248752255754919), (939.6109254209348, 261.6284721142879, 0.5105904178822136, -0.3804951433303434), (1137.6109254209348, 283.6284721142879, -0.3970119276492259, -0.26213845041851824), (983.6109254209348, 261.6284721142879, 0.2920487848965372, 0.12376204892503329), (917.6109254209348, 371.6284721142879, -0.09866411159858801, 0.5464972857025983), (939.6109254209348, 415.6284721142879, 0.5895639800892951, 0.40635070346232216), (895.6109254209348, 437.6284721142879, -0.985675387366487, -0.31033581032337443), (1181.6109254209348, 349.6284721142879, -0.7333504976900183, 0.5662327080667311), (873.6109254209348, 327.6284721142879, -0.279899592146569, -0.1704355526781831), (983.6109254209348, 217.6284721142879, -0.5672889135994421, 0.9236465697776759), (917.6109254209348, 305.6284721142879, 0.751142618830313, -0.040505744344271344), (961.6109254209348, 503.6284721142879, -0.44088433011253847, 0.23122106875342463), (939.6109254209348, 547.6284721142879, -0.3597214569961329, -0.9982758867612724), (1027.6109254209348, 239.6284721142879, -0.721298117379894, -0.5590534766923416), (917.6109254209348, 415.6284721142879, 0.5752947627475471, -0.29540990981402104), (1071.6109254209348, 239.6284721142879, -0.8220361006870682, -0.8114028700418099), (873.6109254209348, 305.6284721142879, -0.8583640788871458, -0.970620732267768), (895.6109254209348, 547.6284721142879, 0.7264237552358421, -0.12638532672967417), (961.6109254209348, 525.6284721142879, -0.5566555455684894, -0.6895684054793667), (1049.6109254209348, 437.6284721142879, -0.6815756175004855, -0.9005482194134926), (1203.6109254209348, 305.6284721142879, -0.9204774937710245, 0.5381202654198054), (1137.6109254209348, 349.6284721142879, -0.6424658112514365, 0.1606235239237226), (1093.6109254209348, 459.6284721142879, 0.3990686843557998, -0.8930071150650043), (895.6109254209348, 481.6284721142879, 0.23931697508980254, -0.789913047066974), (851.6109254209348, 569.6284721142879, 0.9990566711993385, 0.008737419635288957), (895.6109254209348, 217.6284721142879, 0.84387003962399, 0.04488846762848642), (1027.6109254209348, 305.6284721142879, 0.41411726885822153, -0.19321691357849602), (1071.6109254209348, 217.6284721142879, 0.2870410303344084, 0.5694131110039895), (1181.6109254209348, 217.6284721142879, 0.053027000206163244, -0.45965780882031515), (1203.6109254209348, 569.6284721142879, -0.9702523151372224, 0.10868221767034258), (851.6109254209348, 283.6284721142879, 0.23772337503258956, -0.3817277682485407), (939.6109254209348, 393.6284721142879, 0.9094184631930693, 0.24995037024120048), (983.6109254209348, 371.6284721142879, 0.8114160030895814, 0.6020576844395065), (1005.6109254209348, 327.6284721142879, -0.6953012918424881, -0.932116392791208), (1159.6109254209348, 459.6284721142879, 0.5260926918406597, 6.969207047236026e-06), (1049.6109254209348, 415.6284721142879, 0.5707246345064647, -0.5088324825443706), (1137.6109254209348, 371.6284721142879, 0.6823926005333902, 0.8300082195619471), (873.6109254209348, 283.6284721142879, 0.01921423935961797, -0.24629666177300003), (961.6109254209348, 305.6284721142879, 0.2617382122634846, -0.739316093116775), (961.6109254209348, 459.6284721142879, 0.31964124788555903, 0.035202513988459305), (1159.6109254209348, 261.6284721142879, -0.9134454393594849, -0.0483160726136076), (1005.6109254209348, 239.6284721142879, -0.1502212940496206, 0.2088141259094325)]
# sprawd = [(1010,400,0,-5),(1049,400,-5,0),(1010,349,0,5),(900, 200,0,5),(900,297,0,1)]
for oo in sprawd:
    atomy.append(Atom(oo[0], oo[1], oo[2], oo[3], 20, (0, 0, 255)))

# atomy[91].col = (150,150,50)
# atomy[84].col = (150,150,50)
# atomy[32].col = (150,10,50)
atomy[1].col = (250,250,250)
atomy[0].col = (150,150,50)
atomy[3].col = (0,0,0)
a.caption = f"Liczba atomów: {len(atomy)}"
aa=0
bb=0
cc=0
dd=0

# Pętla programu
while True:
    # print(atomy[0].dystans(atomy[1]))
    # print(atomy[0].x, atomy[0].y, atomy[1].x, atomy[1].y)
    # print(atomy[3].dystans(atomy[4]))
    # print("____________________________________________________________" )
    # print(atomy[91].x, atomy[91].y, atomy[39].x, atomy[39].y, atomy[91].dystans(atomy[39]))
    # print("speed", atomy[39].speed_x, atomy[91].speed_y, atomy[39].speed_x, atomy[84].speed_y)
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
                atomy=[]
                ilosc += 1
                dodaj(ilosc)
                a.caption = f"Liczba atomów: {len(atomy)}"
            elif am.mouse_over_button(pos) and atomy:
                usun()
                a.caption = f"Liczba atomów: {len(atomy)}"
            elif con_x < pos[0] < con_x + L and con_y < pos[1] < con_y + H:
                dodaj_on_click(pos[0], pos[1])
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
                ustalanie_pozycji(con_y, con_y + H, con_x, con_x + L)
            elif bp.mouse_over_button(pos) and eta < 75:
                eta += 5
                H = eta * R
                L = eta * R
                con_x -= R / 2 * 5
                con_y -= R / 2 * 5
                container = pygame.Rect(con_x, con_y, H, L)
                frame = pygame.Rect(con_x - 5, con_y - 5, H + 10, L + 10)
                b.caption = f"Rozmiar zbiornika η: {eta}"
                ustalanie_pozycji(con_y, con_y + H, con_x, con_x + L)
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
                            (-1.0 * vGen, vGen), s, (255, 0, 0))
                atomy.append(czerfony)
                dodaj(ilosc)
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
            tlo = pygame.transform.scale(tlo, (event.w, event.h))
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        elif event.type == pygame.USEREVENT:
            delta_t -= 1

    ruch(screen, con_y, con_y+H, con_x, con_x+L)

    pygame.display.flip()  # wyświetla obiekty
    czas.tick(30)  # spowalnia, max 60 klatek na sekundę

    if pomiar:
        time += 1
        es.caption = f"{delta_t//10}:{delta_t%10}"
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


    print(aa,bb,cc,dd)
