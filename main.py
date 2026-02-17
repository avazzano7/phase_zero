import pygame
from game import Game

def main():
    pygame.init()

    pygame.mixer.init(44100, -16, 2, 512)
    pygame.mixer.set_num_channels(32)

    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
