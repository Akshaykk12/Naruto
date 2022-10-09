import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Realm of Warriors")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
P1 = (75, 0, 130)
P2 = (255, 69, 0)
BLACK = (41, 36, 33)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
VIOLET = (134, 1, 175)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
SASUKE_SIZE = 120
SASUKE_SCALE = 2
SASUKE_OFFSET = [72, 56]
SASUKE_DATA = [SASUKE_SIZE, SASUKE_SCALE, SASUKE_OFFSET]
NARUTO_SIZE = 104
NARUTO_SCALE = 2
NARUTO_OFFSET = [72, 54]
NARUTO_DATA = [NARUTO_SIZE, NARUTO_SCALE, NARUTO_OFFSET]

#load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.mp3")
sword_fx.set_volume(0.5)
punch_fx = pygame.mixer.Sound("assets/audio/punch.wav")
punch_fx.set_volume(0.75)


#load background image
bg_image = pygame.image.load("assets/images/background/background.png").convert_alpha()

#load spritesheets
sasuke_sheet = pygame.image.load("assets/images/sasuke/Sprites/sasuke.png").convert_alpha()
naruto_sheet = pygame.image.load("assets/images/naruto/Sprites/naruto.png").convert_alpha()

#load vicory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#define number of steps in each animation
SASUKE_ANIMATION_STEPS = [4, 6, 1, 4, 3, 2, 6]
NARUTO_ANIMATION_STEPS = [4, 6, 1, 6, 4, 2, 7]

#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar1(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, P1, (x, y, 400, 30))
  pygame.draw.rect(screen, VIOLET, (x, y, 400 * ratio, 30))
def draw_health_bar2(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, P2, (x, y, 400, 30))
  pygame.draw.rect(screen, ORANGE, (x, y, 400 * ratio, 30))


#create two instances of fighters
fighter_1 = Fighter(1, 350, 310, False, SASUKE_DATA, sasuke_sheet, SASUKE_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 670, 310, True, NARUTO_DATA, naruto_sheet, NARUTO_ANIMATION_STEPS, punch_fx)

#game loop
run = True
while run:

  clock.tick(FPS)

  #draw background
  draw_bg()

  #show player stats
  draw_health_bar1(fighter_1.health, 20, 20)
  draw_health_bar2(fighter_2.health, 580, 20)
  draw_text("P1: " + str(score[0]), score_font, VIOLET, 20, 60)
  draw_text("P2: " + str(score[1]), score_font, ORANGE, 915, 60)

  #update countdown
  if intro_count <= 0:
    #move fighters
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
  else:
    #display count timer
    draw_text(str(intro_count), count_font, BLACK, 480, 100)
    #update count timer
    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()

  #update fighters
  fighter_1.update()
  fighter_2.update()

  #draw fighters
  fighter_1.draw(screen)
  fighter_2.draw(screen)

  #check for player defeat
  if round_over == False:
    if fighter_1.alive == False:
      score[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    elif fighter_2.alive == False:
      score[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
  else:
    #display victory image
    screen.blit(victory_img, (280, 155))
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      round_over = False
      intro_count = 3
      fighter_1 = Fighter(1, 350, 310, False, SASUKE_DATA, sasuke_sheet, SASUKE_ANIMATION_STEPS, sword_fx)
      fighter_2 = Fighter(2, 670, 310, True, NARUTO_DATA, naruto_sheet, NARUTO_ANIMATION_STEPS, punch_fx)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False


  #update display
  pygame.display.update()

#exit pygame
pygame.quit()