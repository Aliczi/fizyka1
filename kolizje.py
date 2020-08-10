import pygame
import sys
import math
import random







"""     Założenia projektu      """

etaH = 25  # Warunek minimalnego rozmiaru zbiornika: nH, nL >= 20
etaL = 25
R = 30  # promień R
s = 2 * R  # średnica
vGen = 1     # Prędkość
tol = R / 10  # tolerancja zderzenia'
M = 10
time = 0
lambdy = []
H = etaH * R  # wysokość zbiornika
L = etaL * R  # szerokość zbiornika
ilosc=45 #ilosc atomow
krok_czasu_startowy = (vGen * min(etaH, etaL))
krok_czasu = krok_czasu_startowy
delta_t = M * krok_czasu
nazwa = "M10A45.txt"
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
    def __init__(self, x, y, speed_x, speed_y, s, kolor):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.x = x
        self.y = y

        self.r = s / 2
        self.col = kolor

    def move(self, czas):
        self.x += self.speed_x
        self.y += self.speed_y

    def dystans (self,atom2):
        return (math.sqrt((atom2.x - self.x) ** 2 + (self.y - atom2.y) ** 2))


atomy = []  # lista atomów

def dodaj(L, H, R, vGen, atomy,z):
    print(H)
    for g in range(z):
        i=7
        while i != 0:
            xx = int(random.randrange(0.0 + R, L -  R))
            yy = int(random.randrange(0.0 + R, H - R))
            i = len(atomy)
            at = Atom(xx, yy, random.uniform(-1.0 * vGen, vGen), random.uniform(-1.0 * vGen, vGen), s, (0, 0, 255))
            for j in range(len(atomy)):
                if (at.dystans(atomy[j])) <= s + tol:
                    break

                i -= 1
        print(at.x, at.y)
        atomy.append(at)
        odbicia.append(-1)


s = R*2  # średnica

"""________________________________Dodatkowy atom______________________________________"""
time = 0
lambdy = []
czerfony = Atom(R, R, random.uniform(-1.0 * vGen, vGen), random.uniform(-1.0 * vGen, vGen), s, (255, 0, 0))
atomy.append(czerfony)

"""________________________________Testowy zestaw atomów______________________________________"""

# atom0 = Atom(200,200, -vGen, -vGen, s, (100, 100, 250))
# atomy.append(atom0)
# atom1 = Atom(100,100, vGen, vGen, s, (250, 100, 100))
# atomy.append(atom1)
#
# atom2 = Atom(360,360, -vGen, -vGen, s, (255, 255, 255))
# atomy.append(atom2)
# atom3 = Atom(350,290, vGen, -vGen, s, (0, 0, 0))
# atomy.append(atom3)
#
# # set3    prawo lewo
# atom4 = Atom(70,430, vGen, 0, s, (50, 150, 100))
# atomy.append(atom4)
# atom5 = Atom(200,430, -vGen, 0, s, (250, 250, 100))
# atomy.append(atom5)
# #
# # set4              góra dół
# atom6 = Atom(80,200, 0, vGen, s, (250, 100, 250))
# atomy.append(atom6)
# atom7 = Atom(80,360, 0, -vGen, s, (100, 250, 250))
# atomy.append(atom7)

#test
# obiekt6 = pygame.Rect(80, 310, s, s)
# atom6 = Atom(obiekt6, 0, vGen, s, (250, 100, 250))
# atomy.append(atom6)
# obiekt7 = pygame.Rect(80, 370, s, s)
# atom7 = Atom(obiekt7, 0, -3, s, (100, 250, 250))
# atomy.append(atom7)
#
# obiekt4 = pygame.Rect(80, 435, s, s)
# atom4 = Atom(obiekt4, 0, -3, s, (50, 150, 100))
# atomy.append(atom4)
# obie5 = pygame.Rect(80, 430, s, s)
# atom5 = Atom(obie5, -vGen, 0, s, (250, 250, 100))
# atomy.append(atom5)



def ruch():
    global etaH, etaL, R, s, H, L, vGen, tol, M, atomy, lamby, time, ilosc, krok_czasu_startowy, krok_czasu, delta_t, nazwa
    # poruszanie atomami
    for i in range(len(atomy)):
        atom = atomy[i]
        # KOLIZJE Z ATOMAMI
        for j in range(i + 1, len(atomy)):
            atom2 = atomy[j]
            if i == 0 or j == 0:
                pos1 = (atomy[0].x, atomy[0].y)
            # sprawdzanie czy atomy w siebie "wniknęły" po przemieszczeniu, jeżeli tak to oddalają się od siebie
            while s >= atom.dystans(atom2) and (i != odbicia[j] or j != odbicia[i]):
                atom.x -= atom.speed_x / 4
                atom.y -= atom.speed_y / 4

                print("wnik")
                # atom.Rect.x = int(pozycja_x[i])
                # atom.Rect.y = int(pozycja_y[i])

                atom2.x -= atom2.speed_x / 4
                atom2.y -= atom2.speed_y / 4
                # atom2.Rect.x = int(pozycja_x[j])
                # atom2.Rect.y = int(pozycja_y[j])

            if i == 0 or j == 0:
                pos2 = (atomy[0].x, atomy[0].y)

                # sprawdzanie czy czerwony atom się przesunąl i oblizanie o ile

                if pos1 != pos2:
                    odl = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
                else:
                    odl = 0

            # Odbicie
            if s < atom.dystans(atom2) <= s + tol and (i != odbicia[j] or j != odbicia[i]):
                if i == 0 or j == 0:
                    lambdy.append(math.sqrt((time * atomy[0].speed_x) ** 2 + (time * atomy[0].speed_y) ** 2) - odl)
                    print(i, j)

                    time = 0
                atom1 = atomy[j]
                odbicia[i] = j
                odbicia[j] = i
                xs = atom.x
                ys = atom.y
                xs1 = atom1.x
                ys1 = atom1.y
                tupl = (xs - xs1,  # (r1 - r2)
                        ys - ys1)

                tupl2 = (xs1 - xs,  # (r2 - r1)
                         ys1 - ys)

                d = (tupl[0] ** 2) + (tupl[1] ** 2)

                dot1 = ((atom.speed_x - atom1.speed_x) * tupl[0] + (
                        atom.speed_y - atom1.speed_y) * tupl[1]) / d  # (dot/d)

                dot2 = ((atom1.speed_x - atom.speed_x) * tupl2[0] + (  # drugi atom
                        atom1.speed_y - atom.speed_y) * tupl2[1]) / d

                x1 = dot1 * tupl[0]
                y1 = dot1 * tupl[1]
                x2 = dot2 * tupl2[0]
                y2 = dot2 * tupl2[1]

                atom.speed_x -= x1
                atom.speed_y -= y1
                atom1.speed_x -= x2
                atom1.speed_y -= y2
        atom = atomy[i]
        if atom.x - atom.r < 0:
            atomy[i].x = atom.r
            atom.speed_x *= -1
            # print(atomy[i].speed_x)
            odbicia[i] = -1
        elif atom.x + atom.r > L:
            atomy[i].x = L - atom.r
            # print("pyk róg")
            atomy[i].speed_x *= -1
            odbicia[i] = -1
        elif atom.y - atom.r < 0:
            # print("pyk odbicie")
            atomy[i].y = atom.r
            atomy[i].speed_y *= -1
            odbicia[i] = -1
        elif atom.y + atom.r > H:
            print(H)
            atomy[i].y = H - atom.r
            atomy[i].speed_y *= -1
            odbicia[i] = -1

    for i in range(len(atomy)):
        atomy[i].move(krok_czasu)

"""__________________________________________________________________________________________________________________________________"""


# zwraca indeks pierwszego atomu z którym wykryje zdarzenie

odbicia = [-1] * len(atomy)

"""_________________________________________________________________"""
def main():
    global etaH,etaL,R,s,H, L, vGen,tol,M, atomy, lamby, time,ilosc, krok_czasu_startowy,krok_czasu,delta_t,nazwa

    print(H)


    screen = pygame.display.set_mode((L, H), pygame.RESIZABLE)

    pygame.display.set_caption("Symulacja atomów")
    pygame.init()
    czasowy.caption = f" γt = {krok_czasu_startowy}"
    nowy_atom.caption = f"Atomy: {len(atomy)} "
    czas = pygame.time.Clock()
    dodaj(L , H , R , vGen, atomy,ilosc)

    # Pętla programu
    while True:
        if delta_t > 0:
            delta_t -= 1
            time += 1
            czas.tick(krok_czasu)  # spowalnia, max 60 klatek na sekundę
            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # wyście iksem z okienka konczy program
                    pygame.quit()
                    sys.exit()
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     if jedenminus.mouse_over_button(pos) and etaH > 20:
                #         etaH -= 1
                #         H = etaH * R
                #         screen = pygame.display.set_mode((L, H + 40))
                #         jeden.caption = "etaH: " + str(etaH)
                #     elif jedenplus.mouse_over_button(pos) and etaH < 40:
                #         etaH += 1
                #         H = etaH * R
                #         screen = pygame.display.set_mode((L, H + 40))
                #         jeden.caption = "etaH: " + str(etaH)
                #     elif dwaplus.mouse_over_button(pos) and etaL < 40:
                #         etaL += 1
                #         L = etaL * R
                #         panel.rect.width = L
                #         screen = pygame.display.set_mode((L, H))
                #         dwa.caption = "etaL: " + str(etaL)
                #     elif dwaminus.mouse_over_button(pos) and etaL > 20:
                #         etaL -= 1
                #         L = etaL * R
                #         screen = pygame.display.set_mode((L, H))
                #         panel.rect.width = L
                #         dwa.caption = "etaL: " + str(etaL)
                #     elif czasowyminus.mouse_over_button(pos) and krok_czasu >= 10:
                #         krok_czasu -= 10
                #         czasowy.caption = "γt: " + str(krok_czasu)
                #     elif czasowyplus.mouse_over_button(pos):
                #         krok_czasu += 10
                #         czasowy.caption = "γt: " + str(krok_czasu)
                #     elif nowy_atom_plus.mouse_over_button(pos) and len(atomy) < (etaH * etaL / 4):
                #         dodaj(L, H, R, vGen)
                #
                #         nowy_atom.caption = f"Atomy: {len(atomy)} "
                #     elif nowy_atom_minus.mouse_over_button(pos) and atomy:
                #         atomy.pop()
                #         odbicia.pop()
                #         nowy_atom.caption = f"Atomy: {len(atomy)} "
                #
                # elif event.type == pygame.VIDEORESIZE:
                #     L = event.w
                #     H = event.h
                #     panel.rect.width = L
                #     screen = pygame.display.set_mode(
                #         (event.w, event.h), pygame.RESIZABLE)

            # poruszanie atomami
            for i in range(len(atomy)):
                atom = atomy[i]
                # KOLIZJE Z ATOMAMI
                for j in range(i + 1, len(atomy)):
                    atom2 = atomy[j]
                    if i == 0 or j == 0:
                        pos1 = (atomy[0].x, atomy[0].y)
                    # sprawdzanie czy atomy w siebie "wniknęły" po przemieszczeniu, jeżeli tak to oddalają się od siebie
                    while s >= atom.dystans(atom2) and (i != odbicia[j] or j != odbicia[i]):
                        atom.x -= atom.speed_x / 4
                        atom.y -= atom.speed_y / 4

                        print("wnik")
                        # atom.Rect.x = int(pozycja_x[i])
                        # atom.Rect.y = int(pozycja_y[i])

                        atom2.x -= atom2.speed_x / 4
                        atom2.y -= atom2.speed_y / 4
                        # atom2.Rect.x = int(pozycja_x[j])
                        # atom2.Rect.y = int(pozycja_y[j])

                    if i == 0 or j == 0:
                        pos2 = (atomy[0].x, atomy[0].y)

                        # sprawdzanie czy czerwony atom się przesunąl i oblizanie o ile

                        if pos1 != pos2:
                            odl = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
                        else:
                            odl = 0

                    # Odbicie
                    if s < atom.dystans(atom2) <= s + tol and (i != odbicia[j] or j != odbicia[i]):
                        if i == 0 or j == 0:
                            lambdy.append(
                                math.sqrt((time * atomy[0].speed_x) ** 2 + (time * atomy[0].speed_y) ** 2) - odl)
                            print(i, j)

                            time = 0
                        atom1 = atomy[j]
                        odbicia[i] = j
                        odbicia[j] = i
                        xs = atom.x
                        ys = atom.y
                        xs1 = atom1.x
                        ys1 = atom1.y
                        tupl = (xs - xs1,  # (r1 - r2)
                                ys - ys1)

                        tupl2 = (xs1 - xs,  # (r2 - r1)
                                 ys1 - ys)

                        d = (tupl[0] ** 2) + (tupl[1] ** 2)

                        dot1 = ((atom.speed_x - atom1.speed_x) * tupl[0] + (
                                atom.speed_y - atom1.speed_y) * tupl[1]) / d  # (dot/d)

                        dot2 = ((atom1.speed_x - atom.speed_x) * tupl2[0] + (  # drugi atom
                                atom1.speed_y - atom.speed_y) * tupl2[1]) / d

                        x1 = dot1 * tupl[0]
                        y1 = dot1 * tupl[1]
                        x2 = dot2 * tupl2[0]
                        y2 = dot2 * tupl2[1]

                        atom.speed_x -= x1
                        atom.speed_y -= y1
                        atom1.speed_x -= x2
                        atom1.speed_y -= y2
                atom = atomy[i]
                if atom.x - atom.r < 0:
                    atomy[i].x = atom.r
                    atom.speed_x *= -1
                    # print(atomy[i].speed_x)
                    odbicia[i] = -1
                elif atom.x + atom.r > L:
                    atomy[i].x = L - atom.r
                    # print("pyk róg")
                    atomy[i].speed_x *= -1
                    odbicia[i] = -1
                elif atom.y - atom.r < 0:
                    # print("pyk odbicie")
                    atomy[i].y = atom.r
                    atomy[i].speed_y *= -1
                    odbicia[i] = -1
                elif atom.y + atom.r > H:
                    print(H)
                    atomy[i].y = H - atom.r
                    atomy[i].speed_y *= -1
                    odbicia[i] = -1

            for i in range(len(atomy)):
                atomy[i].move(krok_czasu)
            screen.fill((100, 100, 100))  # zmienia kolor tła okna
            for atom in atomy:
                #print(atom.x, atom.y)
                pygame.draw.circle(screen,atom.col,(int(atom.x),int(atom.y)), int(atom.r))

            # rysowanie menu
            #rys_menu(screen)
            pygame.display.update()

        else:
            screen.fill((100, 100, 100))  # zmienia kolor tła okna
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # wyście iksem z okienka konczy program
                    f = open(nazwa, 'a')
                    f.write(str(len(lambdy)))
                    f.write(" ")
                    f.write(str(sum(lambdy)))
                    f.write(" ")
                    if (len(lambdy)>0):
                        f.write(str(sum(lambdy) / len(lambdy)))
                    else:
                        f.write("0")
                    f.write(" ")
                    f.write(str(len(lambdy) / (M * krok_czasu)))
                    f.write("\n")

                    f.close()
                    pygame.quit()
                    sys.exit()

            font = pygame.font.SysFont("ebrima", 20)
            text1 = font.render(f"Liczba zderzeń: {len(lambdy)}", False, (0, 0, 0))
            text2 = font.render(f"Przebyta droga: {sum(lambdy)}", False, (0, 0, 0))
            if (len(lambdy) > 0):
                text3 = font.render(f"Średnia droga między zderzeniami: {sum(lambdy) / len(lambdy)}", False, (0, 0, 0))
            else:
                text3 = font.render("0",False, (0, 0, 0))
            text4 = font.render(f"Częstość zderzeń: {len(lambdy) / (M * krok_czasu)}", False, (0, 0, 0))
            screen.blit(text1, (0, 0))
            screen.blit(text2, (0, 20))
            screen.blit(text3, (0, 40))
            screen.blit(text4, (0, 60))

            pygame.display.flip()


if __name__ == '__main__':
    main()
