import pygame as pg
from pygame.locals import *
import sys
import math

SCREEN = Rect(0,0,800,700)
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
    self.fire_interval = 0

  def update(self):
    # 移動
    self.move()
    # 弾を打つ
    self.fire()
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
  
  def move(self):
    keys = pg.key.get_pressed()
    if keys[K_w]:
      self.rect.centery -= self.v[1]
    if keys[K_s]:
      self.rect.centery += self.v[1]
    if keys[K_a]:
      self.rect.centerx -= self.v[0]
    if keys[K_d]:
      self.rect.centerx += self.v[0]
  
  def fire(self):
    if self.fire_interval<=0:
      if pg.mouse.get_pressed()[0]:
        self.fire_interval = 10
        angleV = pg.math.Vector2((math.sin(math.radians(self.theta))*-1, math.cos(math.radians(self.theta))*-1))
        muzzle_pos = self.rect.center + self.r * angleV
        self.groups()[0].add(Bullet(muzzle_pos, 10, (5,10), self.theta))
    else:
      self.fire_interval -= 1
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
    self.rect.center = pg.math.Vector2(self.rect.center) + self.v * angleV

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

if __name__ == "__main__":
  main()