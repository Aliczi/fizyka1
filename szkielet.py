import pygame, sys, os, math, random


"""     Założenia projektu      """

eta = 40 # Warunek minimalnego rozmiaru zbiornika: nH, nL >= 20
      # max 75 min 20
R = 10  # promień R
s = 2 * R  # średnica
H = eta * R  # wysokość zbiornika
L = eta * R  # szerokość zbiornika
vGen = 5  # Prędkość
d = R / 10  # tolerancja zderzenia'
krok_czasu=vGen*20     #ile klatek na sekundę
M=5                    #wartość M

delta_t = M * krok_czasu


pygame.init()
czas = pygame.time.Clock()
os.environ['SDL_VIDEO_CENTERED'] = '1'

screen = pygame.display.set_mode((1480, 780),pygame.RESIZABLE)
pygame.display.set_caption("Symulacja atomów")



#________________________________________________________________________________________________________
class Button():

    def __init__(self, x, y, width, height, color=(0, 0, 0), caption='',hover_color=''):
        self.x=x
        self.y=y
        self.caption = caption
        self.width = width
        self.height = height

        self.text_color=(0,0,0)
        self.color = color
        self.back_color = color
        self.hover_color=hover_color


    def draw(self,screen):

        pygame.draw.rect(screen, self.back_color, (self.x, self.y, self.width, self.height))

        if self.caption != '':
            font = pygame.font.SysFont("sitkasmallsitkatextitalicsitkasubheadingitalicsitkaheadingitalicsitkadisplayitalicsitkabanneritalic", 20)
            text = font.render(self.caption, 1, self.text_color, self.back_color)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


    def mouse_over_button(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] < self.y + self.height and pos[1] > self.y:
            self.back_color = self.hover_color
            self.text_color=(255,255,255)
            return True
        else:
            self.back_color=self.color
            self.text_color = (0, 0, 0)
            return False




#Button(pozycjax,pozycjay, szerokość, wysokość, kolor, napis, hover kolor)
top_color=(128,0,64)
top_color2=(148,20,84)
hoverr=(108,0,24)

a = Button(100, 150, 300, 30, top_color, "Liczba atomów: 45",hoverr)
am = Button(400, 150, 50, 30, top_color2, "-",hoverr)
ap = Button(450, 150, 50, 30, top_color, "+",hoverr)

b = Button(100, 200, 300, 30, top_color, "Rozmiar zbiornika η: 40",hoverr)
bm =Button(400, 200, 50, 30, top_color2, "-",hoverr)
bp = Button(450, 200, 50, 30, top_color, "+",hoverr)

c = Button(100, 250, 300, 30, top_color, "Krok czasu δt: 100",hoverr)
cm =Button(400, 250, 50, 30, top_color2, "-",hoverr)
cp = Button(450, 250, 50, 30, top_color, "+",hoverr)

dd = Button(100, 300, 300, 30, top_color, "Wartość M: 5",hoverr)
dm =Button(400, 300, 50, 30, top_color2, "-",hoverr)
dp = Button(450, 300, 50, 30, top_color, "+",hoverr)

e = Button(100, 400, 300, 30, top_color, "Dokonaj pomiaru -> ",hoverr)
es =Button(400, 400, 100, 30, top_color2, "Start",hoverr)


f = Button(50, 460, 500, 30, top_color, "Liczba zderzeń: ?", hoverr)
g = Button(50, 500, 500, 30, top_color, "Przebyta droga: : ?", hoverr)
h = Button(50, 540, 500, 30, top_color, "Średnia droga λ: ?", hoverr)
i = Button(50, 580, 500, 30, top_color, "Ilość kolizji w czasie: ?", hoverr)


przyciski=[a,am,ap,b,bm,bp,c,cm,cp,dd,dm,dp,e,es,f,g,h,i]

#Zbiornik
con_x, con_y = 830,190
frame=pygame.Rect(con_x-8,con_y-8,H+16,L+16)
container = pygame.Rect(con_x,con_y,H,L)

# tlo=pygame.image.load(os.path.join('wzory2.jpg')).convert_alpha()
# tlo = pygame.transform.scale(tlo,(1480,780))
RosyBrown=(188,143,143)
Maroon=(128,0,64)


def draw_setup(screen):
    screen.fill((155, 100, 100))  # zmienia kolor tła okna
    # screen.blit(tlo, (0, 0))
    pygame.draw.rect(screen, Maroon, frame)
    pygame.draw.rect(screen, RosyBrown,container)
    for el in przyciski:
        el.draw(screen)



"""Mechanika ruchu"""

class Atom():
    def __init__(self, Rect, x, y, s, color):
        self.Rect = Rect
        self.speed_x = x
        self.speed_y = y
        self.x = Rect.center[0]
        self.y = Rect.center[1]

        self.r = s / 2
        self.col = color


atomy = []  # lista atomów
pozycja_x = []
pozycja_y = []
odbicia=[-1]*len(atomy)

"""________________________________Dodatkowy atom______________________________________"""
time = 0
lambdy = []
czerwony = Atom(pygame.Rect(con_x, con_y, s, s), 3, 3, s, (255, 0, 0))
atomy.append(czerwony)
pozycja_x.append(con_x)
pozycja_y.append(con_y)
odbicia.append(-1)




def dodaj(top,bottom,left,right, R, vGen):
    xx = random.uniform(left, right - R )
    yy = random.uniform(top, bottom - R )
    atomy.append( Atom(pygame.Rect(xx, yy, 2 * R, 2 * R), random.uniform(-1.0 * vGen, vGen), random.uniform(-1.0 * vGen, vGen), 2*R, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

    pozycja_x.append(xx)
    pozycja_y.append(yy)
    odbicia.append(-1)



def dodaj_on_click(xx,yy, R, vGen):
    atomy.append( Atom(pygame.Rect(xx+R, yy+R, 2 * R, 2 * R), random.uniform(-1.0 * vGen, vGen), random.uniform(-1.0 * vGen, vGen), 2*R, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

    pozycja_x.append(xx)
    pozycja_y.append(yy)
    odbicia.append(-1)


def usun():
    atomy.pop()
    pozycja_x.pop()
    pozycja_y.pop()
    odbicia.append(-1)



def kolizja(j, atomy):  # zwraca indeks pierwszego atomu z którym wykryje zdarzenie
    atom = atomy[j]
    for i in range(len(atomy)):
        atom2 = atomy[i]
        if 54 < math.sqrt((atom.Rect.x - atom2.Rect.x) ** 2 + (atom.Rect.y - atom2.Rect.y) ** 2) < 2 * atom.r + 3:
            return i
    return -1



def ruch(screen,top,bottom,left,right):
    global time, lambdy
    i = 0

    # print(odbicia)
    for atom in atomy:
        # print(atom.col,atom.Rect.x,atom.Rect.y)
        pozycja_x[i] += atom.speed_x
        pozycja_y[i] += atom.speed_y
        atom.Rect.x = int(pozycja_x[i])
        atom.Rect.y = int(pozycja_y[i])
        i += 1



    # tablica = [0] * len(atomy)
    pozx = pozycja_x
    pozy = pozycja_y
    for i in range(len(atomy)):
        atom = atomy[i]
        # KOLIZJE Z ATOMAMI
        for j in range(len(atomy)):
            atom2 = atomy[j]
            # sprawdzanie czy atomy w siebie "wniknęły" po przemieszczeniu, jeżeli tak to oddalają się od siebie
            if i == 0 or j == 0:
                pos1 = (pozycja_x[0], pozycja_y[0])

            while s > (math.sqrt((pozx[j] - pozx[i]) ** 2 + (pozy[j] - pozy[i]) ** 2)) and i != j and i != odbicia[j]:
                pozycja_x[i] -= atom.speed_x / 4
                pozycja_y[i] -= atom.speed_y / 4
                atom.Rect.x = int(pozycja_x[i])
                atom.Rect.y = int(pozycja_y[i])


                pozycja_x[j] -= atom2.speed_x / 4
                pozycja_y[j] -= atom2.speed_y / 4
                atom2.Rect.x = int(pozycja_x[j])
                atom2.Rect.y = int(pozycja_y[j])

            if i == 0 or j == 0:
                pos2 = (pozycja_x[0], pozycja_y[0])

                # sprawdzanie czy czerwony atom się przesunąl i oblizanie o ile

                if pos1 != pos2:
                    odl = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
                else:
                    odl = 0

            # Odbicie
            if s < (math.sqrt((pozx[j] - pozx[i]) ** 2 + (pozy[j] - pozy[i]) ** 2)) <= s + 3 and i != j and i != \
                    odbicia[j]:
                """____________________Liczenie przebytej drogi czerwonego atomu______________________"""
                if i == 0 or j == 0:
                    lambdy.append(math.sqrt((time * atomy[0].speed_x) ** 2 + (time * atomy[0].speed_y) ** 2) - odl)
                    time = 0

                atom1 = atomy[j]
                odbicia[j] = i
                odbicia[i] = j

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


    #odbicia od ścian
        #górnej
        if atom.Rect.centery - atom.r <= top and atom.speed_y < 0:
            atomy[i].Rect.y = top
            pozycja_y[i]=top
            atom.speed_y *= -1
            odbicia[i] = -1

        #dolnej
        elif atom.Rect.centery + atom.r >= bottom and atom.speed_y > 0:
            atomy[i].Rect.y = bottom - atom.r * 2
            pozycja_y[i] = bottom - atom.r * 2
            atomy[i].speed_y *= -1
            odbicia[i] = -1

        #lewej
        elif atom.Rect.centerx - atom.r <= left and atom.speed_x < 0:
            atomy[i].Rect.x = left
            pozycja_x[i] = left
            atomy[i].speed_x *= -1
            odbicia[i] = -1

        #prawej
        elif atom.Rect.centerx + atom.r >= right and atom.speed_x > 0:
            atomy[i].Rect.x = right - atom.r * 2
            pozycja_x[i] = right - atom.r * 2
            atomy[i].speed_x *= -1
            odbicia[i] = -1

        pygame.draw.ellipse(screen, atom.col, atom.Rect)




pomiar = False


for _ in range(45):
    dodaj(con_y, con_y + H, con_x, con_x + L, R, vGen)


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
            #dodaj atom
            if ap.mouse_over_button(pos) and len(atomy) < (eta * eta / 4):
                dodaj(con_y,con_y+H,con_x,con_x+L, R, vGen)
                a.caption=f"Liczba atomów: {len(atomy)}"
            elif am.mouse_over_button(pos) and atomy:
                usun()
                a.caption = f"Liczba atomów: {len(atomy)}"
            elif pos[0] > con_x and pos[0] < con_x + L and pos[1] > con_y and pos[1] < con_y + H:
                dodaj_on_click(pos[0],pos[1],R,vGen)
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
                b.caption=f"Rozmiar zbiornika η: {eta}"
            elif bp.mouse_over_button(pos) and eta < 75:
                eta += 5
                H = eta * R
                L = eta * R
                con_x -= R / 2 * 5
                con_y -= R / 2 * 5
                container = pygame.Rect(con_x, con_y, H, L)
                frame = pygame.Rect(con_x - 5, con_y - 5, H + 10, L + 10)
                b.caption = f"Rozmiar zbiornika η: {eta}"
            #zmiana kroku czasu
            elif cm.mouse_over_button(pos) and krok_czasu >= 10:
                krok_czasu -= 10
                c.caption=f"Krok czasu δt: {krok_czasu}"
            elif cp.mouse_over_button(pos):
                krok_czasu += 10
                c.caption = f"Krok czasu δt: {krok_czasu}"
            #zmiana wartości M
            elif dm.mouse_over_button(pos) and M>10:
                M -= 10
                dd.caption=f"Wartość M: {M}"
            elif dp.mouse_over_button(pos):
                M += 10
                dd.caption = f"Wartość M: {M}"
            elif es.mouse_over_button(pos):
                pomiar=True
                es.caption= "Czekaj"
                delta_t = M * krok_czasu
                lambdy=[]
                time=0
                f.caption = f"Liczba zderzeń : 0"
                g.caption = f"Przebyta droga: 0"
                h.caption = f"Średnia droga λ: 0"
                i.caption = f"Częstość zderzeń: 0"


        elif event.type == pygame.MOUSEMOTION:
            for przycisk in przyciski:
                przycisk.mouse_over_button(pos)

        elif event.type == pygame.VIDEORESIZE:
            # tlo = pygame.transform.scale(tlo, (event.w, event.h))
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


    ruch(screen,con_y,con_y+H,con_x,con_x+L)



    pygame.display.flip()  # wyświetla obiekty
    czas.tick(krok_czasu)  # spowalnia, max 60 klatek na sekundę


    if pomiar:
        time+=1
        delta_t -= 1

        es.caption = f"{delta_t//60}:{delta_t%60}"
        if delta_t < 0:
            f.caption = f"Liczba zderzeń: {len(lambdy)}"
            g.caption = f"Przebyta droga: {round(sum(lambdy),4)}"
            h.caption = f"Średnia droga λ: {round(sum(lambdy)/len(lambdy),4)}"
            i.caption = f"Częstość zderzeń: {round(len(lambdy)/(M * krok_czasu),4)}"
            pomiar = False
            es.caption = "Start"




