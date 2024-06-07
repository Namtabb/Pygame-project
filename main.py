
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

WIDTH = 550
HEIGHT = 550
SCREEN_SIZE = (WIDTH, HEIGHT)
NUM_APPLES = 1
NUM_SEGMENTS= 1


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # making the snake
        self.image = pg.Surface((25,25))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (125,75)
        self.grow = False
        self.change_x = 0
        self.change_y = 0

       
    def update(self):
        
        # kills the snake if it touches the border
        if self.rect.top < 0:
            Player.kill(self)
        if self.rect.bottom > 550:
            Player.kill(self)
        if self.rect.left < 0:
            Player.kill(self)
        if self.rect.right > 550:
            Player.kill(self)

    # movement
        self.rect.x += self.change_x
        self.rect.y += self.change_y
    # how the snake moves 
    def go_left(self):
        self.change_x = -25
        self.change_y = 0

    def go_right(self):
        self.change_x = 25
        self.change_y = 0
 
    def go_down(self):
        self.change_y = 25
        self.change_x = 0
    
    def go_up(self):
        self.change_y = -25
        self.change_x = 0
    
    def body_grow(self):
        self.grow = True
    


class Apple(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
    # making the apple
        self.image = pg.Surface((25,25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        #spawning the apple   
        self.rect.x = random.randrange(0, WIDTH, 25)
        self.rect.y = random.randrange(0, HEIGHT, 25)

      
def start():
    """Environment Setup and Game Loop"""

    pg.init()

    # --Game State Variables--
    screen = pg.display.set_mode(SCREEN_SIZE)
    done = False
    clock = pg.time.Clock()

    apples_eaten = 0
    font = pg.font.SysFont("Futura", 24)

    # All sprites go in this sprite Group
    all_sprites = pg.sprite.Group()
    apple_sprites = pg.sprite.Group()
    snake_segment = pg.sprite.Group()
    

    player = Player()
    
    for _ in range(NUM_APPLES):
        apple = Apple()
        all_sprites.add(apple)
        apple_sprites.add(apple)
      
    all_sprites.add(player)

    pg.display.set_caption("Snake game")

    

    # --Main Loop--
    while not done:
        # --- Event Listener
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            # move the snake a direction when a key is pressed
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    player.go_left()
                    
                if event.key == pg.K_d:
                    player.go_right()
                    
                if event.key == pg.K_w:
                    player.go_up()
                    
                if event.key == pg.K_s:
                    player.go_down()

            

        # checks for apple and snake collision
        apples_collided = pg.sprite.spritecollide(player, apple_sprites, True)


        # prints the amount of apples eaten
        for apple in apples_collided:
            apples_eaten += 1 
        
        for i in apples_collided:
            player.body_grow()
            for _ in range(NUM_SEGMENTS):
                player = Player()

                all_sprites.add(player)
                snake_segment.add(player)


         #spawns apple after eaten
        if len(apple_sprites) <= 0:
            for _ in range(NUM_APPLES):
                apple = Apple()

                all_sprites.add(apple)
                apple_sprites.add(apple)

        # --- Draw items
        screen.fill(BLACK)

        score_image = font.render(f"Score: {apples_eaten}", True, WHITE)

        
        screen.blit(score_image, (5,5))
                
        # --- Update the world state
        all_sprites.update()


        all_sprites.draw(screen)

        # Update the screen with anything new
        pg.display.flip()

        # how fast the game moves
        clock.tick(10)  # 10 fps

    pg.quit()


def main():
    start()


if __name__ == "__main__":
    main()