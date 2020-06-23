import sys
import random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import math


def add_ball(space):
    mass = 1
    radius = 15
    moment = 10  # 1
    body = pymunk.Body(mass, moment)  # 2
    x = random.randint(100, 1250)
    y = random.randint(30, 700)
    body.position = x, y  # 3

    body.angle = random.randint(0, 360)
    body.apply_impulse_at_local_point((body.angle, 0))
    shape = pymunk.Circle(body, radius)  # 4
    shape.elasticity = 1
    shape.damping = 0

    space.add(body, shape)  # 5
    return shape


'''def draw_ball(screen, ball):
    p = int(ball.body.position.x), 600 - int(ball.body.position.y)
    pygame.draw.circle(screen, (0, 0, 255), p, int(ball.radius), 2)'''


def add_static_L(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)  # 1
    body.position = (0, 0)
    l1 = pymunk.Segment(body, (1280, 0), (0, 0), 5)  # 2
    l2 = pymunk.Segment(body, (0, 720), (0, 0), 5)
    l3 = pymunk.Segment(body, (1280, 720), (0, 720), 5)
    l4 = pymunk.Segment(body, (1280, 720), (1280, 0), 5)
    l2.elasticity = 1
    l3.elasticity = 1
    l4.elasticity = 1
    l1.elasticity = 1

    space.add(l1, l2, l3, l4)  # 3
    return l1, l2, l3, l4


'''def draw_lines(screen, lines):
    for line in lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)  # 1
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)  # 2
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1, p2])


def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y + 600)'''


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280, 720))
    space = pymunk.Space()  # 2
    space.gravity = (0, 0)
    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    number = random.randint(1, 15)
    lines = add_static_L(space)
    number = 20
    while number > 0:
        ball_shape = add_ball(space)
        balls.append(ball_shape)
        number -= 1
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

        space.step(1 / 50.0)  # 3
        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(50)


if __name__ == '__main__':
    sys.exit(main())
