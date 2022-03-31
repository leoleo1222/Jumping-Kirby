import pygame
import os
import random
import sys
pygame.init()


game_width = 1100
game_height = 600

pygame.init()
win = pygame.display.set_mode((game_width, game_height))

# Load Images of the Character (there are two popular ways)
look_right = pygame.image.load(os.path.join("kirby_right.png"))
kirby_jump = pygame.image.load(os.path.join("Kriby_jump.png"))
cloud = pygame.image.load(os.path.join("kirby_cloud.png"))
BG = pygame.image.load(os.path.join("Mario_track.png"))
kirby_enemy = [pygame.image.load(os.path.join("Kirby_enemy1.png")),pygame.image.load(os.path.join("kriby_enemy2.png            "))]
kirby_run = [None]*10
for picIndex in range(1,9):
    kirby_run[picIndex-1] = pygame.image.load(os.path.join("Kriby_right", "R" + str(picIndex) + ".png"))
    picIndex+=1

class Kirby:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 10

    def __init__(self, img= look_right):
        self.image = img
        self.kirby_run = True
        self.kirby_jump = False
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0

    def update(self):
        if self.kirby_run:
            self.run()
        if self.kirby_jump:
            self.jump()
        if self.step_index >= 9:
            self.step_index = 0


    def jump(self):
        self.image = kirby_jump
        if self.kirby_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.kirby_jump = False
            self.kirby_run = True
            self.jump_vel = self.JUMP_VEL

    def run(self):
        self.image = kirby_run[self.step_index//3]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

class Obstacle:
    def __init__(self, image, number_of_enemy):
        self.image = image
        self.type = number_of_enemy
        self.rect = self.image[self.type].get_rect()
        self.rect.x = game_width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, win):
        win.blit(self.image[self.type], self.rect)

class Enemy(Obstacle):
    def __init__(self, image, number_of_enemy):
        super().__init__(image, number_of_enemy)
        self.rect.y = 300

def remove(index):
    kirby.pop(index)

class Cloud:
    def __init__(self):
        self.x = game_width + random.randint(800,1000)
        self.y = random.randint(50,100)
        self.image = cloud
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = game_width + random.randint(2500,3000)
            self.y = random.randint(50,100)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, kirby, obstacles
    clock = pygame.time.Clock()
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    kirby = [Kirby()]
    obstacles = []
    cloud = Cloud()
    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 14
    death_count = 0
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        win.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        win.blit(BG, (x_pos_bg, y_pos_bg))
        win.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            win.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        win.fill((142,142,142))
        for i in kirby:
            i.update()
            i.draw(win)
        if len(kirby) == 0:
            break
        if len(obstacles) == 0:
            obstacles.append(Enemy(kirby_enemy, random.randint(0,1)))
        for obstacle in obstacles:
            obstacle.draw(win)
            obstacle.update()
            for i, k in enumerate(kirby):
                if k.rect .colliderect(obstacle.rect):
                    pygame.time.delay(500)
                    death_count += 1
                    menu(death_count)
        user_input = pygame.key.get_pressed()
        background()
        cloud.draw(win)
        cloud.update()
        score()
        for i, k in enumerate(kirby):
            if user_input[pygame.K_SPACE] and not (k.rect.y < 200):
                k.kirby_jump = True
                k.kirby_run = False
            if k.Y_POS < 0:
                k.kirby_jump = False
                k.kirby_run = True

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        win.fill((142, 142, 142))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (game_width // 2, game_height // 2 + 50)
            win.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (game_width // 2, game_height // 2)
        win.blit(text, textRect)
        win.blit(kirby_run[0], (game_width // 2 - 20, game_height // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)