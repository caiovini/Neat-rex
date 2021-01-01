import pygame as pg

from assets import Ground, Trex, Cactus, Bird
from os.path import join

import sys
import random
import pickle
import neat

SCREEN_WIDTH, SCREEN_HEIGHT = 550, 200
WHITE = pg.Color(255, 255, 255)
BLACK = pg.Color(0, 0, 0)

clock = pg.time.Clock()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ground = Ground()
cactus = Cactus()
bird = Bird()


def main(genomes, config) -> None:
    nets, list_trex = [], []
    font = pg.font.Font(join("fonts", "segoe-ui-symbol.ttf"), 15)


    for _, gen in genomes:
        net = neat.nn.FeedForwardNetwork.create(gen, config)
        trex = Trex()
        trex.set_position(50, SCREEN_HEIGHT - trex.rect.h)
        bird.set_position(bird.rect.w * 2 + SCREEN_WIDTH, 10)

        nets.append(net)
        list_trex.append(trex)
        gen.fitness = .0


    ground.set_position(x=0, y=SCREEN_HEIGHT - ground.rect.h)
    cactus.set_position(cactus.rect.w + SCREEN_WIDTH, 165)

    ground_soil_y = [random.randint(196, 200) for _ in range(50)]
    ground_soil_x = [random.randint(0, 2100) for _ in range(50)]

    max_score, speed, game_over, done = 0, 10, False, False
    while not done:

        screen.fill(WHITE)
        screen.blit(bird.image, (bird.rect.x + ground.rect.x, bird.rect.y))
        screen.blit(ground.image, ground.rect)
        screen.blit(cactus.image, (cactus.rect.x +
                                   ground.rect.x, cactus.rect.y))
        bird.animate()
            

        for x, y in zip(ground_soil_x, ground_soil_y):
            pg.draw.line(screen, BLACK, (x + ground.rect.x, y),
                         (x + ground.rect.x + 2, y), width=2)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                done = True
                sys.exit()

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    done = True
                    sys.exit()
        
        remainders = 0
        for (_, gen), net, trex in zip(genomes, nets, list_trex):


            if trex.is_alive:
                
                remainders += 1

                screen.blit(trex.image, (trex.rect.x, trex.rect.y - trex.jump_height))
                trex.animate()

                distance = trex.rect.x + cactus.rect.x + ground.rect.x
                output = net.activate((distance,)) # Tuple
                jump = output.index(max(output))

                
                if jump and not trex.jump_height:
                    trex.is_jumping = True

                if trex.is_jumping:
                    trex.jump_height += 8 # Speed jump
                    if trex.jump_height == 80: # Max height t-rex will jump
                        trex.is_jumping = False

                else:
                    if trex.jump_height > 0:
                        trex.jump_height -= 8

                if ground.rect.x == 0: # Allow trex to score whenever ground position x is zero again
                    trex.did_score = False

                if cactus.rect.x + ground.rect.x < trex.rect.x and not trex.did_score:
                    trex.score += 1
                    trex.did_score = True


                if trex.rect.colliderect(pg.Rect(cactus.rect.x + ground.rect.x,
                                                cactus.rect.y - trex.jump_height, cactus.rect.w, cactus.rect.h)):
                    trex.is_alive = False
                    continue

                gen.fitness = trex.score

        score = [t.score for t in list_trex if t.is_alive]
        if len(score) > 0:
            max_score = max(score)

        ground.rect.x -= speed
        if ground.rect.x < -1510: # Repeat ground at this x point
            speed += max_score / 10
            ground.rect.x = 0


        label = font.render(f"SCORE {max_score}", 1, BLACK) 
        screen.blit(label, (SCREEN_WIDTH / 2.4, SCREEN_HEIGHT / 2.5))

        if not remainders:
            done = True

        pg.display.flip()
        clock.tick(30)  # FPS


if __name__ == "__main__":

    pg.init()
    pg.display.set_caption("Neat t-rex")

    # Set configuration file
    config_path = "config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create core evolution algorithm class
    p = neat.Population(config)

    # Add reporter for fancy statistical result
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    winner = p.run(main)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    with open("winner.pkl", "wb") as file:
        pickle.dump(winner, file)

    sys.exit()

