from pygame import *

#kelas induk untuk kelas lain
class GameSprite(sprite.Sprite):
 # konstruktor dari kelas tersebut
 def __init__(self, player_image, player_x, player_y, size_x, size_y):
     # memanggil konstruktor kelas (Sprite):
    sprite.Sprite.__init__(self)
     # setiap sprite harus memiliki gambar 
    self.image = transform.scale(image.load(player_image), (size_x, size_y))
     # setiap sprite harus menyimpan properti rect
     # persegi panjang yang berisi gambar
    self.rect = self.image.get_rect()
    self.rect.x = player_x
    self.rect.y = player_y
 
 # metode yang menggambar karakter utama di layar
 def reset(self):
    layar.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
 #metode yang mengimplementasikan kontrol sprite dengan tombol panah keyboard
 def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
     # memanggil konstruktor kelas (Sprite):
    GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
    self.x_speed = player_x_speed
    self.y_speed = player_y_speed
 def update(self):
    '''menggerakkan karakter menggunakan kecepatan horizontal dan vertikal saat ini'''
    # gerakan horizontal pertama
    if packman.rect.x <= layar_lebar-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
         self.rect.x += self.x_speed
    # jika tabrakan dengan tembok
    platforms_touched = sprite.spritecollide(self, barriers, False)
    # pergi ke kanan, tepi kanan karakter dekat dengan tepi kiri dinding
    if self.x_speed > 0: 
        for p in platforms_touched:
               # jika beberapa disentuh sekaligus, maka tepi kanan adalah yang paling minimum
               self.rect.right = min(self.rect.right, p.rect.left)
    # pergi ke kiri, letakkan tepi kiri karakter dekat dengan tepi kanan dinding 
    elif self.x_speed < 0: 
        for p in platforms_touched:
               # jika beberapa dinding telah disentuh, maka tepi kiri adalah maksimum
               self.rect.left = max(self.rect.left, p.rect.right) 
    if packman.rect.y <= layar_tinggi-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
        self.rect.y += self.y_speed
    # jika tabrakan dengan tembok
    platforms_touched = sprite.spritecollide(self, barriers, False)
    if self.y_speed > 0: # Turun
        for p in platforms_touched:
               self.y_speed = 0
               # We're checking which of the platforms is the highest from the ones below, aligning with it, and then take it as our support:
               if p.rect.top < self.rect.bottom:
                   self.rect.bottom = p.rect.top
    elif self.y_speed < 0: # naik
        for p in platforms_touched:
               # saat bertabrakan dengan dinding, kecepatan vertikal menjadi 0
               self.y_speed = 0 
               # sejajarkan tepi atas di sepanjang tepi bawah dinding yang tertabrak
               self.rect.top = max(self.rect.top, p.rect.bottom) 
 # metode "tembakan" (gunakan tempat pemain untuk membuat peluru di sana)
 def fire(self):
      bullet = Bullet('bullet.png', self.rect.centerx, self.rect.centery, 15, 20, 15)
      bullets.add(bullet)

#Kelas sprite-enemy
class Enemy(GameSprite):
  side = "left"
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
      # memanggil konstruktor kelas (Sprite):
      GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
      self.speed = player_speed

   #gerakan musuh
  def update(self):
      if self.rect.x <= 420: #w1.wall_x + w1.wall_width
          self.side = "right"
      if self.rect.x >= layar_lebar - 85:
          self.side = "left"
      if self.side == "left":
          self.rect.x -= self.speed
      else:
          self.rect.x += self.speed

# Kelas Peluru  
class Bullet(GameSprite):
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
      # memanggil konstruktor kelas (Sprite):
      GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
      self.speed = player_speed
  # gerakan musuh
  def update(self):
      self.rect.x += self.speed
      # menghilang ketika mencapai tepi layar
      if self.rect.x > layar_lebar+10:
        self.kill()

#membuat layar game
layar_lebar = 700
layar_tinggi = 500
layar = display.set_mode((layar_lebar,layar_tinggi))
warna_latar = (119,210,223)
#membuat judul bar
display.set_caption('Game Labirin')

#membuat grup untuk dinding
barriers = sprite.Group()

# membuat group untuk peluru
bullets = sprite.Group()

#membuat group for musuh
monsters = sprite.Group()

#membuat gambar dinding
w1 = GameSprite('platform2.png',layar_lebar / 2 - layar_lebar / 3, layar_tinggi / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)

#menambahkan dinding dalam group
barriers.add(w1)
barriers.add(w2)

#membuat karakter utama, musuh dan srite terakhir
packman = Player('hero.png', 5, layar_tinggi - 80, 80, 80, 0, 0)
monster = Enemy('cyborg.png', layar_lebar - 80, 180, 80, 80,5)
final_sprite = GameSprite('pac-1.png', layar_lebar - 85, layar_tinggi - 100, 80, 80)

#menambah musuh dalam group
monsters.add(monster)

#variabel yang bertanggung jawab atas bagaimana permainan berakhir
finish = False
#Loop Game
run = True
while run:
    time.delay(50)   
    for e in event.get():
        if e.type == QUIT:
            run = False
        #menggerakan karakter utama
        elif e.type == KEYDOWN:
          if e.key == K_LEFT:
              packman.x_speed = -5
          elif e.key == K_RIGHT:
              packman.x_speed = 5
          elif e.key == K_UP:
              packman.y_speed = -5
          elif e.key == K_DOWN:
              packman.y_speed = 5
        #menembak dengan spasi
          elif e.key == K_SPACE:
              packman.fire()
        
        elif e.type == KEYUP:
          if e.key == K_LEFT:
              packman.x_speed = 0
          elif e.key == K_RIGHT:
              packman.x_speed = 0
          elif e.key == K_UP:
              packman.y_speed = 0
          elif e.key == K_DOWN:
              packman.y_speed = 0
          
    if not finish:
        layar.fill(warna_latar)
        #memperbaharui koordinat karakter
        bullets.update()
        packman.update()
        #menggambar karakter utama
        packman.reset()
        bullets.draw(layar)
        barriers.draw(layar)
        final_sprite.reset()
        
        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(layar)
        sprite.groupcollide(bullets, barriers, True, False)
        
        
        #Memeriksa tabrakan karakter dengan musuh dan dinding
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            #menghitung rasio
            img = image.load('game-over_1.png')
            d = img.get_width() // img.get_height()
            layar.fill((255, 255, 255))
            layar.blit(transform.scale(img, (layar_tinggi * d, layar_tinggi)), (90, 0))

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thumb.jpg')
            layar.fill((255, 255, 255))
            layar.blit(transform.scale(img, (layar_lebar, layar_lebar)), (0, 0))
    
    
    display.update()