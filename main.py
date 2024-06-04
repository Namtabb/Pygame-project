
import random
import pygame as pg

# --CONSTANTS--
# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
EMERALD = (21, 219, 147)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

NUM_ENEMIES = 3

WIDTH = 720
HEIGHT = 480
SCREEN_SIZE = (WIDTH, HEIGHT)


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # making the snake
        self.image = pg.Surface((25,25))
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

        self.rect.centerx = random.randrange(0, WIDTH + 1)

       
    def update(self):
        # kills the snake if it touches the border
        if self.rect.top < 0:
            Player.kill(self)
        if self.rect.bottom > 480:
            Player.kill(self)
        if self.rect.left < 0:
            Player.kill(self)
        if self.rect.right > 720:
            Player.kill(self)


        self.rect.x += self.change_x
        self.rect.y += self.change_y
    
    def go_left(self):
        # changes direction when going left side
        self.change_x = -3
 
    def go_right(self):
        # changes direction when going right side
        self.change_x = 3
 
    def go_down(self):
        # changes direction when going down
        self.change_y = 3
    
    def go_up(self):
        #changes direction when going up
        self.change_y = -3

    

class Apple(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.Surface((25,25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        self.rect.centerx = random.randrange(0, WIDTH + 1)

    def update(self):
        apple_position = [random.randrange(1, (WIDTH//10)) * 10, 
                  random.randrange(1, (HEIGHT//10)) * 10]
    



         
def start():
    """Environment Setup and Game Loop"""

    pg.init()

    # --Game State Variables--
    screen = pg.display.set_mode(SCREEN_SIZE)
    done = False
    clock = pg.time.Clock()

    # All sprites go in this sprite Group
    all_sprites = pg.sprite.Group()

    player = Player()

    apple = Apple()

    
    all_sprites.add(player, apple)

    

    pg.display.set_caption("Snake game")

    

    # --Main Loop--
    while not done:
        # --- Event Listener
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    player.go_left()
                if event.key == pg.K_d:
                    player.go_right()
                if event.key == pg.K_w:
                    player.go_up()
                if event.key == pg.K_s:
                    player.go_down()
 
 
            
            
            
            
            
            
            

            

        # --- Update the world state
        all_sprites.update()

        

       

        
        
        
            

        # --- Draw items
        screen.fill(BLACK)

        all_sprites.draw(screen)

        # Update the screen with anything new
        pg.display.flip()

        # --- Tick the Clock
        clock.tick(60)  # 60 fps

    pg.quit()


def main():
    start()


if __name__ == "__main__":
    main()