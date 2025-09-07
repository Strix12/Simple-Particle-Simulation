import sys
import pygame as sdl
from dataclasses import dataclass
from random import random


RESOLUTION = (1000, 1000)
CENTER = (RESOLUTION[0]/2, RESOLUTION[1]/2)
SIZE = 15.0
BACKGROUND = (0, 0, 0)
COLOR = (255, 255, 255)


@dataclass
class Particle:
    position: sdl.Vector2
    velocity: sdl.Vector2
    size: float


def print_help():
    print("USAGE: python main.py [OPTIONS]")
    print("\n-h | Display this output")
    print("\n-r | Set resolution of window")
    print("\t-r [INT > 0] [INT > 0]")
    print("\n-s | Set size of particle")
    print("\t-s [FLOAT]")
    print("\n-f | Set color of particle")
    print("\t-f [0 <= INT < 256] [0 <= INT < 256] [0 <= INT < 256]")
    print("\n-b | Set color of background")
    print("\t-b [0 <= INT < 256] [0 <= INT < 256] [0 <= INT < 256]")


def check_collisions(particle: Particle, particle_list: list[Particle]):
    for particle2 in particle_list:
        if particle is particle2:
            return

        distance = particle.position.distance_to(particle2.position)
        collision_distance = particle.size + particle2.size
        collides = distance < collision_distance

        if collides:
            collide(particle, particle2)
            overlap = collision_distance - distance
            to_move = overlap * 0.5
            particle.position += particle.velocity.normalize() * to_move
            particle2.position += particle2.velocity.normalize() * to_move


def collide(p1: Particle, p2: Particle):
    dv1 = p1.velocity - p2.velocity
    dv2 = p2.velocity - p1.velocity
    dx1 = p1.position - p2.position
    dx2 = p2.position - p1.position
    total_mass = p1.size + p2.size

    p1.velocity -= ((2*p2.size)/total_mass) * \
        (dv1.dot(dx1)/dx1.length_squared()) * dx1
    p2.velocity -= ((2*p1.size)/total_mass) * \
        (dv2.dot(dx2)/dx2.length_squared()) * dx2


def update_particle(particle: Particle, delta_time: float):
    left_border = top_border = particle.size
    right_border = RESOLUTION[0] - particle.size
    bottom_border = RESOLUTION[1] - particle.size

    if particle.position.x < left_border or particle.position.x > right_border:
        particle.position.x = max(particle.position.x, left_border)
        particle.position.x = min(particle.position.x, right_border)
        particle.velocity.x = -particle.velocity.x

    if particle.position.y < top_border or particle.position.y > bottom_border:
        particle.position.y = max(particle.position.y, top_border)
        particle.position.y = min(particle.position.y, bottom_border)
        particle.velocity.y = -particle.velocity.y

    particle.position += particle.velocity * delta_time


def main():
    sdl.init()
    sdl.display.set_mode(RESOLUTION)
    sdl.display.set_caption("Particle Simulation")
    running = True
    display_surface = sdl.display.get_surface()
    particles: list[Particle] = []
    clock = sdl.time.Clock()

    while running:
        clock.tick()
        sdl.display.update()
        display_surface.fill(BACKGROUND)

        delta_time = clock.get_time()

        for event in sdl.event.get():
            if event.type == sdl.QUIT:
                running = False
            elif event.type == sdl.MOUSEBUTTONDOWN:
                particles.append(
                    Particle(sdl.Vector2(sdl.mouse.get_pos()), sdl.Vector2(
                        random()-0.5, random()-0.5), SIZE)
                )

        for particle in particles:
            sdl.draw.circle(display_surface, COLOR,
                            particle.position, particle.size)
            update_particle(particle, delta_time)
            check_collisions(particle, particles)

    sdl.quit()


if __name__ == "__main__":
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-r":
            RESOLUTION = (int(sys.argv[i+1]), int(sys.argv[i+2]))
        elif sys.argv[i] == "-s":
            SIZE = float(sys.argv[i+1])
        elif sys.argv[i] == "-f":
            COLOR = (int(sys.argv[i+1]),
                     int(sys.argv[i+2]), int(sys.argv[i+3]))
        elif sys.argv[i] == "-b":
            BACKGROUND = (int(sys.argv[i+1]),
                          int(sys.argv[i+2]), int(sys.argv[i+3]))
        elif sys.argv[i] == "-h":
            print_help()
            sys.exit(0)

    main()
