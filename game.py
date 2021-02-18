import pygame as pg
from pygame.locals import *
import sys
import math

SCREEN = Rect(0,0,400,400)
SCREEN_COLOR = "#FFFFE0"

class Player(pg.sprite.Sprite):
  def __init__(self, pos, v, r, w):
    pg.sprite.Sprite.__init__(self)
    self.image_data = pg.transform.smoothscale(pg.image.load("player.png").convert_alpha(), (2*r,2*r))
    self.r = r
    self.image = self.image_data
    self.rect = self.image.get_rect()
    self.rect.center = pos
    self.v = v
    self.w = w
    self.theta = 60

  def update(self):
    # 衝突
    if self.rect.centerx-self.r<0:
      self.rect.centerx = self.r
    if self.rect.centerx+self.r>SCREEN.size[0]:
      self.rect.centerx = SCREEN.size[0]-self.r
    if self.rect.centery-self.r<0:
      self.rect.centery = self.r
    if self.rect.centery+self.r>SCREEN.size[1]:
      self.rect.centery = SCREEN.size[1]-self.r
    # 向き
    mouseV = pg.math.Vector2(pg.mouse.get_pos())
    posV = pg.math.Vector2(self.rect.center)
    angleV = pg.math.Vector2((math.sin(math.radians(self.theta))*-1, math.cos(math.radians(self.theta))*-1))
    dtheta = (mouseV-posV).angle_to(angleV)
    if (-180<dtheta and dtheta<0-self.w) or (180<dtheta and dtheta<360-self.w):
      self.theta -= self.w
    elif (-360+self.w<dtheta and dtheta<-180) or (self.w<dtheta and dtheta<180):
      self.theta += self.w
    center = self.rect.center
    self.image = pg.transform.rotate(self.image_data, self.theta)
    self.rect = self.image.get_rect()
    self.rect.center = center
  
  def move(self, key):
    if key == K_UP:
      self.rect.centery -= self.v[1]
    elif key == K_DOWN:
      self.rect.centery += self.v[1]
    elif key == K_LEFT:
      self.rect.centerx -= self.v[0]
    elif key == K_RIGHT:
      self.rect.centerx += self.v[0]
  
  def shoot(self):
    self.groups()[0].add(Bullet(self.rect.center, 5, (5,10), self.theta))
    
class Bullet(pg.sprite.Sprite):
  def __init__(self, pos, v, size, theta):
    pg.sprite.Sprite.__init__(self)
    self.image_data = pg.transform.smoothscale(pg.image.load("bullet.png").convert_alpha(), size)
    self.image = pg.transform.rotate(self.image_data, theta)
    self.rect = self.image.get_rect()
    self.rect.center = pos
    self.v = v
    self.theta = theta
    self.time = 0
  def update(self):
    self.time += 1
    if self.time>30:
      self.kill()
    self.move()
  def move(self):
    angleV = pg.math.Vector2((math.sin(math.radians(self.theta))*-1, math.cos(math.radians(self.theta))*-1))
    self.rect.center = (pg.math.Vector2(self.rect.center) + self.v * angleV)[:]

def main():
  pg.init()
  screen = pg.display.set_mode(SCREEN.size)
  pg.display.set_caption("foo")
  group = pg.sprite.Group()
  player = Player(SCREEN.center, [5,5], 30, 5)
  group.add(player)
  
  pg.key.set_repeat(30, 30)

  clock = pg.time.Clock()
  while True:
    clock.tick(30)
    screen.fill(SCREEN_COLOR)
    group.update()
    group.draw(screen)
    pg.display.flip()

    for event in pg.event.get():
      if event.type == QUIT:
        pg.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          pg.quit()
          sys.exit()
        elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
          player.move(event.key)
        elif event.key == K_SPACE:
          player.shoot()

if __name__ == "__main__":
  main()