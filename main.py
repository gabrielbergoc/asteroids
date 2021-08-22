import sys
import pygame_menu
from objects import *

# global variables
default_vel = 5
default_ang_vel = 6
max_asteroid_n = 10

# initialize pygame and screen
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Gabsteroids")
pygame.key.set_repeat(100)

# main menu loop - calls game loop
def main():

    menu = pygame_menu.Menu("Welcome to Gabsteroids", 800, 600)
    menu.add.button("Play", gameloop)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(screen)

def gameloop():

    # initialize background
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # initialize game objects
    player = Player()
    player_sprite = pygame.sprite.RenderPlain(player)

    asteroids_sprites = pygame.sprite.RenderPlain(Asteroids())
    debris_sprites = pygame.sprite.RenderPlain()

    bullets_sprites = pygame.sprite.RenderPlain()

    scoreboard = Scoreboard()

    clock = pygame.time.Clock()
    time_intervals = 0          # keep track of time to create new asteroids

    # game main loop
    while True:
        clock.tick(60)
        time_intervals += clock.get_time()

        # create new asteroids every 2 seconds
        if time_intervals > 2000 and asteroids_sprites.__len__() < max_asteroid_n:
            asteroids_sprites.add(Asteroids())
            time_intervals = 0

        # event handling
        for event in pygame.event.get():
            # print(event)
            if event.type == QUIT:
                return
            if event.type == KEYDOWN and event.key == K_UP:
                player._move(default_vel)
            if event.type == KEYUP and event.key == K_UP:
                player._stop()
            if event.type == KEYDOWN and event.key == K_LEFT:
                player._turn(default_ang_vel)
            if event.type == KEYDOWN and event.key == K_RIGHT:
                player._turn(-default_ang_vel)
            if event.type == KEYUP and event.key == K_LEFT:
                player._stop_turn()
            if event.type == KEYUP and event.key == K_RIGHT:
                player._stop_turn()
            if event.type == KEYDOWN and \
                    (event.key == K_c  or event.key == K_KP0):
                bullets_sprites.add(Bullets(player.rect.center, player.angle))

        # collision checks
        for bullet in bullets_sprites.sprites():
            if not bullet.area.contains(bullet.rect):
                bullet.kill()   # get rid of bullets offscreen

            # check bullet-asteroids collisions
            for asteroid in asteroids_sprites.sprites():
                if pygame.sprite.collide_mask(bullet, asteroid):

                    # divide asteroids into two
                    if asteroid.size > 0.1:
                        new_asteroids = asteroid._split()
                        if new_asteroids[0].size < 0.1:
                            debris_sprites.add(new_asteroids)   # if too small, they become debris
                        else:
                            asteroids_sprites.add(new_asteroids)
                    bullet.kill()
                    asteroid.kill()
                    scoreboard.score += 1
                    scoreboard.update_score()

        # check player-asteroids collisions, break if True
        if pygame.sprite.spritecollide(player, asteroids_sprites, True, pygame.sprite.collide_mask):
            scoreboard.update_highscore()
            break

        # update everything
        screen.blit(background, (0, 0))
        player_sprite.update()
        player_sprite.draw(screen)
        asteroids_sprites.update()
        asteroids_sprites.draw(screen)
        debris_sprites.update()
        debris_sprites.draw(screen)
        bullets_sprites.update()
        bullets_sprites.draw(screen)
        screen.blit(scoreboard.surface, scoreboard.pos)
        pygame.display.flip()

    # game over screen
    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_RETURN:
                return

        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 40)
        text = font.render("GAME OVER", True, (0, 0, 0))
        text_pos = (background.get_width() / 2, background.get_height() / 2)
        text_rect = text.get_rect(centerx=text_pos[0], centery=text_pos[1])
        background.blit(text, text_rect)
        pygame.display.flip()


if __name__ == '__main__':
    main()
