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

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Making the snake head
        self.image = pg.Surface((25, 25))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 125
        self.rect.y = 75
        self.change_x = 0
        self.change_y = 0
        self.segments = []
        self.grow = False

    def update(self):
        # Movement
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Check for collision with the border
        if self.rect.top < 0 or self.rect.bottom > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

        # Check for collision with itself
        if len(self.segments) > 0:
            if pg.sprite.spritecollideany(self, self.segments):
                self.kill()

        # Handle body segments
        if len(self.segments) > 0:
            # Move the last segment to the player's current position
            old_segment = self.segments.pop()
            old_segment.rect.x = self.rect.x - self.change_x
            old_segment.rect.y = self.rect.y - self.change_y
            self.segments.insert(0, old_segment)

        # Add new segment if growing
        if self.grow:
            new_segment = BodySegment(self.rect.x, self.rect.y)
            self.segments.insert(0, new_segment)
            all_sprites.add(new_segment)
            self.grow = False

    def go_left(self):
        if self.change_x == 0:  # Prevent moving left if already moving right
            self.change_x = -25
            self.change_y = 0

    def go_right(self):
        if self.change_x == 0:  # Prevent moving right if already moving left
            self.change_x = 25
            self.change_y = 0

    def go_down(self):
        if self.change_y == 0:  # Prevent moving down if already moving up
            self.change_y = 25
            self.change_x = 0

    def go_up(self):
        if self.change_y == 0:  # Prevent moving up if already moving down
            self.change_y = -25
            self.change_x = 0

    def body_grow(self):
        self.grow = True


class BodySegment(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((25, 25))
        self.image.fill(EMERALD)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Apple(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Making the apple
        self.image = pg.Surface((25, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # Spawning the apple
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
    global all_sprites
    all_sprites = pg.sprite.Group()
    apple_sprites = pg.sprite.Group()

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
            # Move the snake in a direction when a key is pressed
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    player.go_left()
                if event.key == pg.K_d:
                    player.go_right()
                if event.key == pg.K_w:
                    player.go_up()
                if event.key == pg.K_s:
                    player.go_down()

        # Check for apple and snake collision
        apples_collided = pg.sprite.spritecollide(player, apple_sprites, True)

        # Print the number of apples eaten and make the growing segment function true
        for apple in apples_collided:
            apples_eaten += 1
            player.body_grow()

        # Spawn apple after it's eaten
        if len(apple_sprites) <= 0:
            for _ in range(NUM_APPLES):
                apple = Apple()
                all_sprites.add(apple)
                apple_sprites.add(apple)

        # --- Draw items
        screen.fill(BLACK)
        score_image = font.render(f"Score: {apples_eaten}", True, WHITE)
        screen.blit(score_image, (5, 5))

        # --- Update the world state
        all_sprites.update()
        all_sprites.draw(screen)

        # Update the screen with anything new
        pg.display.flip()

        # How fast the game moves
        clock.tick(10)  # 10 fps

    pg.quit()


def main():
    start()


if __name__ == "__main__":
    main()
