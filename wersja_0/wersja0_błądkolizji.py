import pygame, sys
import random
import math

pygame.init()
czas = pygame.time.Clock()

# Założenia projektu

etaH=20                                            # Warunek minimalnego rozmiaru zbiornika: nH, nL >= 20
etaL=30
R=30                                               # promień R
s=2*R                                              # średnica
H=etaH*R                                           # wysokość zbiornika
L=etaL*R                                           # szerokość zbiornika
N = 5                                              # Liczba atomów N
vGen = 3                                           # Prędkość


if N>etaH*etaL/4:                                  # Sprawdzenie czy liczba atomów nie jest zbyt duża
    print("Zbyt duża liczba atomów!")
    sys.exit()


screen = pygame.display.set_mode((L,H))



class Atom():
    def __init__(self,Rect,x,y,s,kolor):
        self.Rect = Rect
        self.speed_x = x
        self.speed_y = y
        self.r = s/2
        self.col = kolor


def kolizja(j,atomy):                       #zwraca indeks pierwszego atomu z którym wykryje zdarzenie
    atom=atomy[j]
    for i in range(len(atomy)):
        atom2=atomy[i]
        # print(math.sqrt((atom.Rect.x - atom2.Rect.x) ** 2 + (atom.Rect.y - atom2.Rect.y) ** 2))
        if 60 < math.sqrt((atom.Rect.x - atom2.Rect.x)**2 + (atom.Rect.y-atom2.Rect.y)**2) < 2*atom.r + 4:      #zamiast 56 2xpromień a x powinien r/10
            return i
    return -1



atomy=[]                #lista atomów


# Generator atomów
atomy = [Atom(pygame.Rect(random.uniform(0.0 + R, L - R), random.uniform(0.0 + R, H - R), 2*R, 2*R),random.uniform(-1.0 * vGen, vGen), random.uniform(-1.0 * vGen, vGen), s, (random.randint(0,255),random.randint(0,255),random.randint(0,255))) for i in range(N)]




# set 1 ukośne ten sam kierunek x
obiekt0 = pygame.Rect(200, 200, s, s)
atom0 = Atom(obiekt0,-3,-3,s,(100,100,250))
atomy.append(atom0)
obie1 = pygame.Rect(100, 100, s, s )
atom1 = Atom(obie1,3,3,s,(250,100,100))
atomy.append(atom1)

#set2 ukośne ten sam kierunek y
obiekt2 = pygame.Rect(650, 400, s, s )
atom2 = Atom(obiekt2,-3,-4,s,(255,255,255))
atomy.append(atom2)
obie3 = pygame.Rect(350, 300, s, s )
atom3 = Atom(obie3,3,-2,s,(0,0,0))
atomy.append(atom3)

# set3    prawo lewo
obiekt4 = pygame.Rect(70, 430, s, s)
atom4 = Atom(obiekt4,3,0,s,(50,150,100))
atomy.append(atom4)
obie5 = pygame.Rect(200, 430, s, s )
atom5 = Atom(obie5,-3,0,s,(250,250,100))
atomy.append(atom5)

# set4              góra dół
obiekt6 = pygame.Rect(80, 200, s, s )
atom6 = Atom(obiekt6,0,3,s,(250,100,250))
atomy.append(atom6)
obiekt7 = pygame.Rect(80, 360, s, s )
atom7 = Atom(obiekt7,0,-3,s,(100,250,250))
atomy.append(atom7)


def ruch():
    for atom in atomy:

        atom.Rect.x += atom.speed_x
        atom.Rect.y += atom.speed_y

    tablica = [0] * len(atomy)

    for i in range(len(atomy)):
        atom=atomy[i]
        kol=kolizja(i,atomy)

        if atom.Rect.centerx - atom.r <= 0:
            atom.Rect.x = 0
            atom.speed_x *= -1

        elif atom.Rect.centerx + atom.r >= L:
            atom.Rect.x = L - atom.r * 2

            #print("pyk róg")
            atom.speed_x *= -1

        elif atom.Rect.centery - atom.r <= 0:
            #print("pyk odbicie")
            atom.Rect.y = 0
            atom.speed_y *= -1
        elif atom.Rect.centery + atom.r >= H:
            atom.Rect.y = H - atom.r * 2
            atom.speed_y *= -1

        elif kol>=0 and tablica[kol]==0:
            atom1=atomy[kol]
            tablica[kol]=1
            tablica[i]=1

            atom.speed_y, atom1.speed_y = atom1.speed_y, atom.speed_y
            atom.speed_x, atom1.speed_x = atom1.speed_x, atom.speed_x

        pygame.draw.ellipse(screen,atom.col,atom.Rect)




# Pętla programu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       #wyście iksem z okienka konczy program
            pygame.quit()
            sys.exit()


    screen.fill((80,80,80))     #zmienia kolor tła okna
    ruch()
    pygame.display.flip()                   #wyświetla obiekty
    czas.tick(60)                           #spowalnia, max 60 klatek na sekundę
