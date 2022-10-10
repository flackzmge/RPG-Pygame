import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *
import csv
import pickle
import button
from scoreGui import *

'''
Defines the classes
'''

class platform(pygame.sprite.Sprite):
      def __init__(self,SizeX,SizeY,pos): #when intialised is given size in x and y and positon, these are the tile size and coordinates
            super().__init__()
            self.pos = vec(pos)
            self.surf = pygame.Surface((SizeX, SizeY))
            self.rect = self.surf.get_rect(center = (pos))

      def update(self):
          #updates the rect position to matcht the pos
            self.rect.topleft = self.pos.x, self.pos.y

class Entity(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.surf = pygame.Surface((60,60))
            self.rect = self.surf.get_rect()

            self.pos = vec((0,0))
            self.vel = vec(0,0)
            self.acc = vec(0,0)
            self.facing = 1
            self.type = 'Entity'

      def move(self,left=False,right=False):
            #acceleration due to gravity
            self.acc = vec(0,0.5)
            keyLeft = 0
            keyRight = 0
            keyDown = 0
            #if not in the scroll zones gets the key presses
            if self.pos.x < 3*(WIDTH//4) and entity.pos.x > (WIDTH//4) or scroll == 0:
                  pressedKeys = pygame.key.get_pressed()
                  keyLeft = pressedKeys[K_LEFT]
                  keyRight = pressedKeys[K_RIGHT]
                  keyDown = pressedKeys[K_DOWN]

            #if the entity is an enemy, ignores the key presses
            if self.type == 'Enemy':
                  keyLeft = 0
                  keyRight = 0
                  keyDown = 0
           #checks to see which key is pressed or which way the enemy should move
            if keyLeft == 1 or left != False:
                  self.acc.x = -ACC
                  #changes the way the entity is facing so it is moving forward
                  self.facing = -1
            if keyRight == 1 or right != False:
                  self.acc.x = ACC
                  self.facing = 1
            if keyDown == 1:
                 #if the crouch button pressed changes the surf image to show crouch
                  if self.facing == 1:
                        self.surf = pCrouchR
                  else:
                        self.surf = pCrouchL
            #physics of entity
            self.acc.x += self.vel.x*FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5*self.acc

            self.rect.midbottom = self.pos

      def update(self):
           #loops through all the tiles that are obstacles
            for obstac in obstacleList:
                #using the coordinates of the tile the tile are defined
                  top = obstac[1]-20
                  bottom = obstac[1]+20
                  left = obstac[0]-20
                  right = obstac[0]+20
                  #defines the top and bottom of a small are below the tile
                  undersideTop = bottom
                  undersideBottom = undersideTop+10
                  #checks to see if the bottom of the entity is coliding with the tile
                  if self.rect.bottom > top and self.rect.bottom < bottom and self.rect.left < right and self.rect.right >left:
                         #moves the entity just above the tile so it is able to stand on it
                        self.pos.y = top + 1
                        self.vel.y = 0
                        #checks to see if the top of the entity is in the area just below the tile
                  if self.rect.top < undersideBottom and self.rect.top > undersideTop and self.rect.left < right and self.rect.right >left and self.rect.bottom > bottom:
                        #makes the entity 'bounce of the tile' when it hits its head
                        self.vel.y = 8
                         #checks to see if the right side of the entity is colliding with the left side of the tile
                  if (self.rect.top < bottom and self.rect.top > top) or (self.rect.bottom > bottom and self.rect.bottom < top):
                        if self.rect.right > left and self.rect.right < right:
                              self.pos.x = left-20
                        #checks to see if the left side of the entity is colliding with the right side of the tile
                  if (self.rect.top < bottom and self.rect.top > top) or (self.rect.bottom > bottom and self.rect.bottom < top):
                        if self.rect.left > left and self.rect.left < right:
                              self.pos.x = right + 20

            #checks to see if the entity collides with a tile that can kill
            #it does the collision detection in the same way as for the obstacle list
            for obstac in deathList:
                  top = obstac[1]
                  bottom = obstac[1]+20
                  left = obstac[0]-20
                  right = obstac[0]+20
                  if self.rect.bottom > top and self.rect.bottom < bottom and self.rect.left < right and self.rect.right >left:
                        self.pos.y = top + 1
                        self.vel.y = 0
                        #if a player kills it
                        self.health = 0
                        if self.type == 'Enemy':
                              #if an enemy removes it from the enemy list Killing it
                              enemies.remove(self)

                  if self.rect.top > bottom and self.rect.top < top and self.rect.left < right and self.rect.right >left:
                        self.pos.y = bottom - 20
                        self.vel.y = 0
                        self.health = 0#self.lives -1
                        if self.type == 'Enemy':
                              enemies.remove(self)

                  if (self.rect.top < bottom and self.rect.top > top) or (self.rect.bottom > bottom and self.rect.bottom < top):
                        if self.rect.right > left and self.rect.right < right:
                              self.pos.x = left-20
                              self.health = 0#self.lives -1
                              if self.type == 'Enemy':
                                    enemies.remove(self)

                  if (self.rect.top < bottom and self.rect.top > top) or (self.rect.bottom > bottom and self.rect.bottom < top):
                        if self.rect.left > left and self.rect.left < right:
                              self.pos.x = right + 20
                              self.health = 0#self.lives -1
                              if self.type == 'Enemy':
                                    enemies.remove(self)

            #again the collisin detection is done the same
            if self.type == 'Player':
                  for obstac in portal:
                        top = obstac[1]
                        bottom = obstac[1]+20
                        left = obstac[0]-20
                        right = obstac[0]+20
                        if self.rect.bottom > top and self.rect.bottom < bottom and self.rect.left < right and self.rect.right >left:
                              #calls the function to do the highscore name entering and display
                              addScoreGui(score)
                              #ends the game
                              pygame.quit()
                              sys.exit()

                        if self.rect.top > bottom and self.rect.top < top and self.rect.left < right and self.rect.right >left:
                              addScoreGui(score)
                              pygame.quit()
                              sys.exit()

                        if (self.rect.top < bottom and self.rect.top > top) or (self.rect.bottom > bottom and self.rect.bottom < top):
                              if self.rect.right > left and self.rect.right < right:
                                    addScoreGui(score)
                                    pygame.quit()
                                    sys.exit()

                        if (self.rect.top < bottom and self.rect.top > top) or (self.rect.bottom > bottom and self.rect.bottom < top):
                              if self.rect.left > left and self.rect.left < right:
                                    addScoreGui(score)
                                    pygame.quit()
                                    sys.exit()

            #updates the rect of the entities to match the position
            self.rect.topleft = self.pos.x, self.pos.y

      def jump(self):
            #checks to see if the entity is colliding with a platform (this prevent double jumping)
            #the platforms are placed where the tiles that are obstacles are
            hits = pygame.sprite.spritecollide(self, platforms, False)
            #if the entity is colliding with a platform it must be on the ground
            if hits:
                 #change the velocity to make the entity move up (jump)
                  self.vel.y = -15

class Player(Entity):
      def __init__(self):
            super().__init__()
            self.health = 100
            self.max_health = self.health
            self.healthbarlength = 200
            self.healthratio = self.max_health / self.healthbarlength
            self.surf = pygame.Surface((30,30))
            self.rect = self.surf.get_rect()

            self.pos = vec((60,50))
            self.vel = vec(0,0)
            self.acc = vec(0,0)
            self.facing = 1
            self.crouch = 0
            self.sprint = 0
            self.type = 'Player'

      def shot(self):
            #check whether any of the bullets in enemyBullets list collide with player
            for bullet in enemyBullets:
                  if self.pos.y + 30 > bullet.pos.y and self.pos.y - 30 <= bullet.pos.y:
                        if self.pos.x + 10 >= bullet.pos.x and self.pos.x -10 <= bullet.pos.x:
                              #removes health if the bullet comes within the players hit box
                              self.health = self.health - 5
                              #removes the bullet from the game
                              enemyBullets.remove(bullet)

      def health_bar(self):
          pygame.draw.rect(displaysurface, (0,255,0), (15, 60, self.health/self.healthratio, 25))
          pygame.draw.rect(displaysurface, (255,255,255), (15, 60, self.healthbarlength, 25),4)

class projectile(Entity):
      def __init__(self,pos,facing):
            super().__init__()
            self.pos = vec(pos)
            self.pos.y = self.pos.y-20
            self.vel = vec(5*facing,0)
            self.acc = vec(0,0)

            self.surf = bulletPic
            self.rect = self.surf.get_rect()


class enemy(Entity):
      def __init__(self,pos):
            super().__init__()
            self.surf = pygame.Surface((30,30))
            self.rect = self.surf.get_rect()
            self.left = False
            self.right = True
            self.crouch = 0

            self.pos = vec(pos)
            self.vel = vec(0,0)
            self.acc = vec(0,0)
            self.type = 'Enemy'

      def AI(self):
            if COUNT % 50 == 0:
                  #every 50 game loops flips the way that the enemy is facing
                  if self.left == True:
                        self.left = False
                        self.right = True
                  else:
                        self.left = True
                        self.right = False
            #calls the move method with the direction that the enemy is facing
            self.move(self.left,self.right)

            facing = 1
            if self.left == True:
                  facing = -1
            #every 50 loops the an enemyBullet is added to the list at the pos of the enemy
            #this only happens when the enemy is on the screen to prevent too much noise and too many sprites loaded
            if COUNT % 50 == 0 and self.pos.x < WIDTH and self.pos.x > 0:
                  enemyBullets.add(projectile(self.pos+(0,20),facing))

      def shot(self):
          #checks that none of the bullets in player bullets are within the enemies hit box
            for bullet in bullets:
                  if self.pos.y + 30 > bullet.pos.y and self.pos.y - 30 <= bullet.pos.y:
                        if self.pos.x + 10 >= bullet.pos.x and self.pos.x -10 <= bullet.pos.x:
                              #if a bullet is in the hitbox a drop is added to the drop list
                              #and the enemy and bullet are removed
                              drops.add(drop(self.pos))
                              enemies.remove(self)
                              bullets.remove(bullet)
                              EnemyShot.play()

class asteroid(enemy):
      def __init__(self,pos):
            super().__init__(pos)
            self.surf = asteroidPic
            self.rect = self.surf.get_rect()
            self.left = False
            self.right = True
            self.type = 'Enemy'
            self.pos = vec(pos.x,-30)
            self.vel = vec(0,0)
            self.acc = vec(0,0)
            self.images = []
            

      def move(self):
            self.acc = vec(0,0.05)
            self.acc.x += self.vel.x*FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5*self.acc

      def collide(self):
            hits = pygame.sprite.spritecollide(self , platforms, False)
            if hits:
                 for num in range(1,6):
                   asteroid_explosion = pygame.image.load(f'exp{num}.png').convert_alpha()
                   displaysurface.blit(asteroid_explosion, (entity.pos))
                   self.images.append(asteroid_explosion)
                 asteroids.remove(self)
                 Explosion.play()
                 num = 0


            killed = pygame.sprite.spritecollide(self , players, False)
            if killed:
                  asteroids.remove(self)
                  for player in killed:
                        if player.health > 0:
                            player.health = player.health - 20

class drop(Entity):
      def __init__(self,pos):
            super().__init__()
            self.surf = heart
            self.rect = self.surf.get_rect()
            self.pos = vec(pos)
            self.vel = vec(0,0)
            self.acc = vec(0,0)

      def picked(self):
            pick = pygame.sprite.spritecollide(self , players, False)
            if pick:
                #if collides with player removes the drop
                  drops.remove(self)
                  for player in pick:
                      #adds health if collides with player
                      if player.health < player.max_health:
                          player.health = player.health + 20
                          KillConfirmed.play()
                      #restricts current health from going above max_health
                      if player.health >= player.max_health:
                          player.health = player.max_health

      def move(self):
            #makes sure the drop follow gravity
            self.acc = vec(0,0.05)

            self.acc.x += self.vel.x*FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5*self.acc

      def update(self):
           #checks to see if the drop has collided with a platform
            hits = pygame.sprite.spritecollide(self , platforms, False)
            if hits:
                  #makes sure the drop sits on top of the platform
                  self.pos.y = hits[0].rect.top + 1
                  self.vel.y = 0
            #updates the position of the drop
            self.rect.topleft = self.pos.x, self.pos.y

class Button():
      def __init__(self,x,y,image,scale):
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False

      def draw(self, surface):
            action = False

            #get mouse position
            pos = pygame.mouse.get_pos()

            #check mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                  if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                        action = True
                        self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                  self.clicked = False

            #draw button
            surface.blit(self.image, (self.rect.x, self.rect.y))

            return action

#Class for screen animations
class Fade():

    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        #when the player dies:
        pygame.draw.rect(displaysurface, self.colour, (0,0, WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= WIDTH:
            fade_complete = True

        return fade_complete

'''
Defines the functions
'''

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
          #we have to convert the text to an image and then blit that image onto the screen
      img = font.render(text, True, text_col)
      displaysurface.blit(img, (x, y))

#creates function for drawing a background (adding blocks)
def draw_bg():
          #gives the width of the background image
      width = Background.get_width()
          #how many times we want the image to repeat
      for x in range(10):
              #blit puts an image on to the screen
              #negative scroll means as we move right the background effectively moves left
            displaysurface.blit(Background,((x * width)-scroll,0))


# function for drawing the world tiles
def draw_world():
      # need enumerate as it counts where you are in the list, as this gives
      # your grid position
      for y, row in enumerate(world_data):
            for x, tile in enumerate(row):
                  if tile >= 0 and tile != 6:
                        #diplays the correct picture for the tile
                        displaysurface.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


def scrollCorrection(entity,scroll,prevScroll):
      #move the coordinates of the entities in the game so they move with the scroll
      if scroll_left == True and scroll != 0:
            entity.pos.x = entity.pos.x - (scroll-prevScroll)
      elif scroll_right == True and scroll != 0:
            entity.pos.x = entity.pos.x - (scroll-prevScroll)

def pause():
      Paused = True
      while Paused == True:
            displaysurface.blit(game_paused, (0,0))
            pygame.display.update()
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                  if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                              pygame.quit()
                              sys.exit()
                        if event.key == pygame.K_SPACE:
                              Paused = False

def main_menu():
    while True:

        select_level_button = button.Button(WIDTH // 4.5 , HEIGHT - 400, level_select, 1)
        instruction_button = button.Button(WIDTH // 3.6, HEIGHT - 100, instruction_image, 1)
        start_button = button.Button(WIDTH // 2.5 , HEIGHT - 250, start_image, 1)

        displaysurface.blit(Background, (0, 0))
        displaysurface.blit(menu, (WIDTH // 8.8 , 10))

        select_level_button.draw(displaysurface)
        instruction_button.draw(displaysurface)
        start_button.draw(displaysurface)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        select_level_button = pygame.Rect(((WIDTH // 2) - 150, 200), (300, 100))
        instruction_button = pygame.Rect(((WIDTH // 2) - 150, 500), (300, 100))
        start_button = pygame.Rect(((WIDTH // 2) - 150, 350), (300, 100))
        
        

        if select_level_button.collidepoint(mouse_x, mouse_y):
            if click:
                select()

        if instruction_button.collidepoint((mouse_x, mouse_y)):
            if click:
                options()
  
        if start_button.collidepoint((mouse_x, mouse_y)):
            if click:
                return
        
    

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


        pygame.display.update()
        FPS_CLOCK.tick(60)


def select():
    running = True
    while running:

        mouse_x, mouse_y = pygame.mouse.get_pos()
        displaysurface.blit(Background, (0,0))

        level1but = button.Button(WIDTH // 15 , HEIGHT - 570, level1, 1)
        level2but = button.Button(WIDTH // 1.9 , HEIGHT - 570, level2, 1)
        level3but = button.Button(WIDTH // 15 , HEIGHT - 380, level3, 1)
        level4but = button.Button(WIDTH // 1.9 , HEIGHT - 380, level4, 1)

        level1but.draw(displaysurface)
        level2but.draw(displaysurface)
        level3but.draw(displaysurface)
        level4but.draw(displaysurface)
        
        level1but = pygame.Rect(((WIDTH // 4) - 150, 30), (300, 100))
        level2but = pygame.Rect(((WIDTH // 1.2) - 150, 30), (300, 100))
        level3but = pygame.Rect(((WIDTH // 4) - 150, 200), (300, 100))
        level4but = pygame.Rect(((WIDTH // 1.2) - 150, 200), (300, 100))

        if level1but.collidepoint((mouse_x, mouse_y)):
            if click:
                global level
                level = 0 
                return
            
        elif level2but.collidepoint((mouse_x, mouse_y)):
            if click:
                # global level
                level = 0
                level = level + 1
                return
            
        elif level3but.collidepoint((mouse_x, mouse_y)):
            if click:
                # global level
                level = 0
                level = level + 2
                return
            
        elif level4but.collidepoint((mouse_x, mouse_y)):
            if click:
                # global level
                level - 0 
                level = level + 3
                return

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        FPS_CLOCK.tick(60)


def options():
    running = True
    while running:

        displaysurface.blit(Background, (0,0))
        displaysurface.blit(instruction_page, (0,0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        FPS_CLOCK.tick(60)

def draw_text1(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def createLevel(level):
      #before function, create empty tile list
      world_data = []
      for row in range(ROWS):
            #[-1] represents empty space on the background
            r = [-1] * MAX_COLUMNS
            world_data = world_data + [r]


      #load in level data and creating world
      with open(f'level{level}_data.csv', newline = '') as csvfile:
      #creating csv reader, the delimiter reads the commas, everytime there is a comma there is another tile
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                  for y,tile in enumerate(row):
                        world_data[x][y] = int(tile)

      # create ground, we want the very last row to be ground so change to zeros
      #for tile in range(0, MAX_COLUMNS):
            #world_data[ROWS - 1][tile] = 18
      for i in range(len(world_data)):
            for j in range(len(world_data[0])):
                  if world_data[i][j] != -1:
                        #gets the x and y coord of the tile
                        y = ((i+1)*TILE_SIZE)-(TILE_SIZE/2)
                        x = ((j+1)*TILE_SIZE)-(TILE_SIZE/2)
                        #appends the tiles coords that should kill to the deathlist
                        if world_data[i][j] == 25 or world_data[i][j] == 24 or world_data[i][j] == 14:
                              deathList.append([x,y])
                        #append the portal tile coords to portal list
                        elif world_data[i][j] == 26:
                              portal.append([x,y])
                        #adds an enemy at the coords of an enemy tile
                        elif  world_data[i][j] == 6:
                              enemies.add(enemy((x,y)))
                        #if not a special tile and not air,adds them to the obstacle list
                        else:
                              obstacleList.append([x,y])
                              #adds a platform for tile that are obstacles
                              platforms.add(platform(TILE_SIZE,TILE_SIZE,(j*TILE_SIZE+20,i*TILE_SIZE+20)))
      return world_data

if __name__ == "__main__":
      pygame.init()  # Begin pygame

      '''
      Define the variables to be used
      '''

      #screen parameters
      HEIGHT = 640
      WIDTH = 800

      #screen
      displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
      pygame.display.set_caption("Shooting Game")

      #set framerate
      FPS = 60
      FPS_CLOCK = pygame.time.Clock()

      #acceleration
      ACC = 0.3
      #friction
      FRIC = -0.10

      #other variables
      COUNT = 0
      ROWS = 16
      MAX_COLUMNS = 150
      TILE_SIZE = HEIGHT // ROWS
      TILE_TYPES = 27
      vec = pygame.math.Vector2
      level = 0

      obstacleList = []
      deathList = []
      portal = []

      #sprite groups
      P1 = Player()
      players = pygame.sprite.Group()
      platforms = pygame.sprite.Group()
      enemies = pygame.sprite.Group()
      asteroids = pygame.sprite.Group()
      drops = pygame.sprite.Group()
      players.add(P1)
      bullets = pygame.sprite.Group()
      enemyBullets = pygame.sprite.Group()

      #defining the images
      Background = pygame.image.load('game background.jpg').convert_alpha()
      Background = pygame.transform.scale(Background,(WIDTH,HEIGHT))
      level_select = pygame.image.load('select_level.png').convert_alpha()
      instruction_image = pygame.image.load('instructions.png').convert_alpha()
      instruction_page = pygame.image.load('instruction page.png').convert_alpha()
      instruction_page = pygame.transform.scale(instruction_page, (WIDTH, HEIGHT))
      level1 = pygame.image.load('level1.png').convert_alpha()
      level2 = pygame.image.load('level2.png').convert_alpha()
      level3 = pygame.image.load('level3.png').convert_alpha()
      level4 = pygame.image.load('level4.png').convert_alpha()
      start_image = pygame.image.load('start.png').convert_alpha()
      
      menu = pygame.image.load('main_menu.png').convert_alpha()
      game_paused = pygame.image.load('game_paused.png').convert_alpha()
      game_paused = pygame.transform.scale(game_paused,(WIDTH,HEIGHT))

      #Defining the characters
      pStandL = pygame.image.load("RFhero_standing.png").convert_alpha()
      pStandR = pygame.image.load("LFhero_standing.png").convert_alpha()
      pCrouchL = pygame.image.load("LFhero_crouch.png").convert_alpha()
      pCrouchR = pygame.image.load("RFhero_crouch.png").convert_alpha()
      pRunLL = pygame.image.load("LFhero_Lrun.png").convert_alpha()
      pRunRR = pygame.image.load("RFhero_Rrun.png").convert_alpha()
      pSprintLL = pygame.image.load("LFhero_Lsprint.png").convert_alpha()
      pSprintRR = pygame.image.load("RFhero_Rsprint.png").convert_alpha()
      pSprintLR = pygame.image.load("LFhero_Rsprint.png").convert_alpha()
      pSprintRL = pygame.image.load("RFhero_Lsprint.png").convert_alpha()
      pRunLR = pygame.image.load("LFhero_Rrun.png").convert_alpha()
      pRunRL = pygame.image.load("RFhero_Lrun.png").convert_alpha()
      bulletPic = pygame.image.load('beam.png').convert_alpha()
      enemybulletPic = pygame.image.load('Enemy1Bullet1.png').convert_alpha()
      asteroidPic = pygame.image.load('asteroid_s.png').convert_alpha()
      heart = pygame.image.load('heart.png').convert_alpha()
      heart = pygame.transform.scale(heart,(15,15))

      enemyStandL = pygame.image.load('Enemy1(1).png').convert_alpha()
      enemyStandR = pygame.transform.flip(enemyStandL, True, False)
      enemy11 = pygame.image.load('Enemy1(2).png').convert_alpha()
      enemy12 = pygame.image.load('Enemy1(3).png').convert_alpha()
      enemy13 = pygame.image.load('Enemy1(4).png').convert_alpha()
      enemy14 = pygame.image.load('Enemy1(5).png').convert_alpha()
      enemy15 = pygame.image.load('Enemy1(6).png').convert_alpha()
      enemy16 = pygame.image.load('Enemy1(7).png').convert_alpha()
      enemy17 = pygame.image.load('Enemy1(8).png').convert_alpha()
      enemy111 = pygame.transform.flip(enemy11, True, False)
      enemy112 = pygame.transform.flip(enemy12, True, False)
      enemy113 = pygame.transform.flip(enemy13, True, False)
      enemy114 = pygame.transform.flip(enemy14, True, False)
      enemy115 = pygame.transform.flip(enemy15, True, False)
      enemy116 = pygame.transform.flip(enemy16, True, False)
      enemy117 = pygame.transform.flip(enemy17, True, False)

      respawnbutton = Button(200,HEIGHT // 2 - 50,pygame.image.load("respawn.png").convert_alpha(),1)

      GREEN = (144, 201, 120)
      WHITE = (255, 255, 255)
      RED = (200, 25, 25)
      PINK = (235, 65, 54)

      #screen fading
      death_fade = Fade(2, PINK, 6)

      runningListR = [pRunRR,pRunRL]
      runningListL = [pRunLR,pRunLL]
      enemyrunningListR = [enemy11,enemy12,enemy13,enemy14,enemy15,enemy16]
      enemyrunningListL =  [enemy111,enemy112,enemy113,enemy114,enemy115,enemy116]
      sprintList = [pSprintLL,pSprintRR,pSprintLR,pSprintRL]
      erunIndex = 0 # enemy index
      runIndex = 0 # player index

      #defines the font
      font = pygame.font.SysFont('Futura', 40)

      #definng sounds
      Shooting = pygame.mixer.Sound('shot.wav')
      Shooting.set_volume(0.05)
      EnemyShot = pygame.mixer.Sound('EnemyDeath.wav')  #EnemyDeath.wav
      EnemyShot.set_volume(0.05)
      Explosion = pygame.mixer.Sound('explosion.wav')  #EnemyDeath.wav
      Explosion.set_volume(0.15)
      Jump = pygame.mixer.Sound('jump.wav')  #EnemyDeath.wav
      Jump.set_volume(0.05)
      KillConfirmed = pygame.mixer.Sound('KillConfirmed.wav')
      KillConfirmed.set_volume(0.02)

      main_menu()

      current_tile = 0
      scroll_left = False
      scroll_right = False
      scroll = 0
      prevScroll = 0
      scroll_speed = 0.5

      #storing tiles in a list
      img_list = []
      #start at 1 due to the naming of the files
      for x in range(1,TILE_TYPES + 1):
            img = pygame.image.load(f'{x}.png')
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            img_list.append(img)

      GREEN = (144, 201, 120)
      WHITE = (255, 255, 255)
      RED = (200, 25, 25)

      world_data = createLevel(level)

      score = 0
      enemyNo = len(enemies)
      enemyCount = 0
      pRunCount = 0
      eRunCount = 0

      '''
      Game Loop
      '''

      while True:
            draw_bg()
            draw_world()

          # Render Functions ------

            for event in pygame.event.get():
              # Will run when the close window button is clicked
                  if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

              # For events that occur upon clicking the mouse (left click)
                  if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                              if len(bullets) < 5:
                                    for entity in players:
                                          bullets.add(projectile(entity.pos,entity.facing))
                                          Shooting.play()

              # Event handling for a range of different key presses
                  if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                              for entity in players:
                                    entity.jump()
                                    Jump.play()


                  if event.type == pygame.KEYDOWN:
                      if event.key ==pygame.K_SPACE:
                          pause()

            #scrolling the map, scroll>0 stops scrolling off the left hand side of the screen
            if scroll_left == True and scroll>0:
              #reduce the variable by 5 pixels as we are moving left
                  scroll -= 5 * scroll_speed
                  #increase the variable by 5 pixels as we are moving right
            if scroll_right == True and scroll < (MAX_COLUMNS * TILE_SIZE) - WIDTH:
                  scroll += 5 * scroll_speed

            #loops through all the entities in platforms
            for entity in platforms:
                  #calls scroll correction to correct for scroll
                  scrollCorrection(entity,scroll,prevScroll)
                  #calls the update function to update the rect to match pos
                  entity.update()

            #loops through all the entities in bullets
            for entity in bullets:
                  #calls scroll correction to correct for scroll
                  scrollCorrection(entity,scroll,prevScroll)
                  #diplays the bullet surface
                  displaysurface.blit(entity.surf, entity.pos-(0,15))
                  #checks that the bullet has not collided with any of the tile in obstacle list
                  for obstac in obstacleList:
                        top = obstac[1]-20
                        bottom = obstac[1]+20
                        left = obstac[0]-20
                        right = obstac[0]+20
                        if (entity.pos.y < bottom and entity.pos.y > top) or (entity.pos.y > bottom and entity.pos.y < top):
                              if entity.pos.x+20 > left and entity.pos.x < right:
                                    #if collided the bullet is removed so the bullets cant go through walls
                                    bullets.remove(entity)
                        if (entity.pos.y < bottom and entity.pos.y > top) or (entity.pos.y > bottom and entity.pos.y < top):
                              if entity.pos.x+20 > left and entity.pos.x < right:
                                    bullets.remove(entity)
                  #changes th position due to the velocity of the bullet
                  entity.pos = entity.pos + entity.vel
                  #if the bullet goes of the screen it is removed
                  if entity.pos.x > WIDTH or entity.pos.x < 0:
                        bullets.remove(entity)

            #loops through all the entities in enemybullets following the exact same process as for bullets
            for entity in enemyBullets:
                  entity.surf = enemybulletPic
                  scrollCorrection(entity,scroll,prevScroll)
                  displaysurface.blit(entity.surf, entity.pos-(0,20))
                  for obstac in obstacleList:
                        top = obstac[1]-20
                        bottom = obstac[1]+20
                        left = obstac[0]-20
                        right = obstac[0]+20
                        if (entity.pos.y-20 < bottom and entity.pos.y-20 > top) or (entity.pos.y-20 > bottom and entity.pos.y-20 < top):
                              if entity.pos.x+20 > left and entity.pos.x < right:
                                    enemyBullets.remove(entity)
                        if (entity.pos.y-20 < bottom and entity.pos.y-20 > top) or (entity.pos.y-20 > bottom and entity.pos.y-20 < top):
                              if entity.pos.x+20 > left and entity.pos.x < right:
                                    enemyBullets.remove(entity)
                  entity.pos = entity.pos + entity.vel
                  if entity.pos.x > WIDTH or entity.pos.x < 0:
                        enemyBullets.remove(entity)
            #loops through all the entities in enemies
            for entity in enemies:
                  #if the enemy is not moving displays the standing image
                  if round(entity.vel.x) == 0:
                        if entity.facing == 1:
                              entity.surf = enemyStandL
                        else:
                              entity.surf = enemyStandR
                  else:
                       #else if it is moving cycles throught the images for running every 20 game loops to create an animation of moving
                        if entity.facing == 1: #for right
                              if eRunCount%20 == 0:
                                    entity.surf = enemyrunningListR[erunIndex]
                                    erunIndex = erunIndex+1
                                    if erunIndex == len(enemyrunningListR):
                                          erunIndex = 0
                        else: #for left
                              if eRunCount%20 == 0:
                                    entity.surf = enemyrunningListL[erunIndex]
                                    erunIndex = erunIndex+1
                                    if erunIndex == len(enemyrunningListL):
                                          erunIndex = 0
                  #corrects for scroll
                  scrollCorrection(entity,scroll,prevScroll)
                  #displays the surface
                  displaysurface.blit(entity.surf, entity.pos-(20,25))
                  #calls the AI method which allow the enmy to shoot and move
                  entity.AI()
                  #updates the rect to match pos and checks for collisions with the map
                  entity.update()
                  #checks to see if the enemy has been shot
                  entity.shot()

            for entity in asteroids:
                  #correct for scroll
                  scrollCorrection(entity,scroll,prevScroll)
                  #displays the surface
                  displaysurface.blit(entity.surf, entity.pos)
                  #moves the asteroid
                  entity.move()
                  #updates the rect to match pos
                  entity.update()
                  #check to see if the asteroid has been shot
                  entity.shot()
                  #checks to see if the asteroid has hit a player or the floor
                  entity.collide()

            #loops through all the entities in drops
            for entity in drops:
                  #corrects for scroll
                  scrollCorrection(entity,scroll,prevScroll)
                  entity.move()
                  entity.update()
                  entity.picked()
                  displaysurface.blit(entity.surf, entity.pos-(30,30))

            #loops through all the entities in players
            for entity in players:
                  #changes the surface similarly to enemy
                  if round(entity.vel.x) == 0:
                        if entity.facing == 1:
                              entity.surf = pStandL
                        else:
                              entity.surf = pStandR
                  else:
                        if entity.facing == 1:
                              if pRunCount%10 == 0:
                                    entity.surf = runningListR[runIndex]
                                    runIndex = runIndex+1
                                    if runIndex == len(runningListR):
                                          runIndex = 0
                        else:
                              if pRunCount%10 == 0:
                                    entity.surf = runningListL[runIndex]
                                    runIndex = runIndex+1
                                    if runIndex == len(runningListL):
                                          runIndex = 0
                
                  #corrects for scroll
                  if scroll_left == True and scroll != 0:
                        entity.pos.x = entity.pos.x - (scroll-prevScroll)
                  elif scroll_right == True and scroll != 0:
                        entity.pos.x = entity.pos.x - (scroll-prevScroll)
                  player = entity
                  healthLeft = entity.health
                  if entity.health <= 0:
                         #if the player health is zero or below removes the player
                        players.remove(entity)
                        #death_screen()
                  #calls the move method to allow the player to move
                  entity.move()
                  #displays the surface
                  displaysurface.blit(entity.surf, entity.pos-(20,45))
                  #updates the rect to matvh the pos and checks for collisions
                  entity.update()
                  #check to see of the player is shot
                  entity.shot()
                  entity.health_bar()
            #if the player goes in the right quarter the screen scrolls right
            if entity.pos.x > 3*(WIDTH//4):
                  scroll_right = True
                  scroll_left = False
            #if the player goes into the left quarter the screen scrolls left
            elif entity.pos.x < WIDTH//4:
                  scroll_right = False
                  scroll_left = True
            #if in the middel there is no need to scroll
            else:
                  scroll_right = False
                  scroll_left = False

            #adds an asteroid every ten seconds
            if (round(pygame.time.get_ticks()/1000))%10 == 0 and len(asteroids) == 0:
                  asteroids.add(asteroid(player.pos))

            #if there are no players shows the respawn screen and adds a new player if the respawn button is pressed
            if len(players) == 0:
                  if death_fade.fade():
                      if respawnbutton.draw(displaysurface) == True and len(players) == 0:
                            players.add(Player())
                            for entity in players:
                                  entity.pos.x = 205

            #updates the coordinates of the tile in the obstacle death and portal list to correct for scroll
            for obstac in obstacleList:
                  obstac[0] = obstac[0]-(scroll-prevScroll)

            for obstac in deathList:
                  obstac[0] = obstac[0]-(scroll-prevScroll)

            for obstac in portal:
                  obstac[0] = obstac[0]-(scroll-prevScroll)

            #calcultes the score as the difference between the initial number of enemies - enmies left
            score=(enemyNo-len(enemies))*100
            #diplays the score on the screen
            text = font.render('Score:'+str(score),True,'white')
            textRect = text.get_rect()
            textRect.center = (70,35)
            displaysurface.blit(text, textRect)

            highscore = 0
            
            #updates the display and increases the clock and count varialbes
            pygame.display.update()
            FPS_CLOCK.tick(FPS)
            COUNT = COUNT + 1
            pRunCount = pRunCount + 1
            prevScroll = scroll

