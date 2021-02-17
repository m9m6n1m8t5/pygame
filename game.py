import pygame
from pygame.locals import *
import sys
import math

SCREEN = Rect(0,0,400,400)

class Player(pygame.sprite.Sprite):
  def __init__(self, pos, v, r, w):
    pygame.sprite.Sprite.__init__(self)
    self.image_data = pygame.transform.smoothscale(pygame.image.load("player.png").convert_alpha(), (2*r,2*r))
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
    mouseV = pygame.math.Vector2(pygame.mouse.get_pos())
    posV = pygame.math.Vector2(self.rect.center)
    angleV = pygame.math.Vector2((math.sin(math.radians(self.theta))*-1, math.cos(math.radians(self.theta))*-1))
    dtheta = (mouseV-posV).angle_to(angleV)
    print(dtheta)
    if (-180<dtheta and dtheta<0-self.w) or (180<dtheta and dtheta<360-self.w):
      self.theta -= self.w
    elif (-360+self.w<dtheta and dtheta<-180) or (self.w<dtheta and dtheta<180):
      self.theta += self.w
    center = self.rect.center
    self.image = pygame.transform.rotate(self.image_data, self.theta)
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
    

def main():
  pygame.init()
  screen = pygame.display.set_mode(SCREEN.size)
  pygame.display.set_caption("foo")
  player = Player(SCREEN.center, [5,5], 30, 5)
  group = pygame.sprite.Group()
  group.add(player)

  pygame.key.set_repeat(30, 30)

  clock = pygame.time.Clock()
  while True:
    clock.tick(30)
    screen.fill((155,155,155,0))
    group.update()
    group.draw(screen)
    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          pygame.quit()
          sys.exit()
        else:
          player.move(event.key)

if __name__ == "__main__":
  main()