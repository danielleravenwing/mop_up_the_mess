#sprite classes for game
import pygame as pg
from settings import *
from random import choice, randrange
from math import ceil
vec = pg.math.Vector2 #used for vectors

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, kind = 'blue'):
        self.groups = game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        tilex = ceil(x / TILE_SIZE)
        tiley = ceil(y / TILE_SIZE)
        self.x = x
        self.y = y
        if self.game.tiles_filled[tiley][tilex] != 0:
            for i, px in enumerate(self.game.tiles_filled[tiley]):
                if px == 0:
                    self.x = px * TILE_SIZE
                    break
        self.kind = kind
        if self.kind == 'blue':
            self.image = self.game.blue_mop_image
            self.mop_rate = 500
            self.player_acc = PLAYER_ACC
        elif self.kind == 'red':
            self.image = self.game.red_mop_image
            self.mop_rate = 300
            self.player_acc = PLAYER_ACC + 0.25
        elif self.kind == 'yellow':
            self.image = self.game.yellow_mop_image
            self.mop_rate = 100
            self.player_acc = PLAYER_ACC + 0.5
        elif self.kind == 'green':
            self.image = self.game.green_mop_image
            self.mop_rate = 1
            self.player_acc = PLAYER_ACC + 1
        self.previous_mop_rate = self.mop_rate
        self.powerup_start_time = 0
        self.powerup_end_time = 0
        self.powerup_kind = None
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.pos = vec(self.rect.center)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.clicked = False
        self.kills = 0
        self.color_change_pending = False

    @property
    def kills(self):  # This is the method that is called whenever you access kills
        return self._kills
    @kills.setter # Runs whenever you set a value for kills
    def kills(self, value):
        self._kills = value
        if value > (10 + self.game.level) * 4:
            self.change_color()

    def change_color(self, color = None):
        if self.powerup_kind not in ['bleach', 'peroxide']:
            self.color_change_pending = False
            if color != None:
                self.kind = color
                if self.kind == 'blue':
                    self.image = self.game.blue_mop_image
                    self.mop_rate = 500
                    self.player_acc = PLAYER_ACC
                elif self.kind == 'red':
                    self.image = self.game.red_mop_image
                    self.mop_rate = 300
                    self.player_acc = PLAYER_ACC + 0.25
                elif self.kind == 'yellow':
                    self.image = self.game.yellow_mop_image
                    self.mop_rate = 100
                    self.player_acc = PLAYER_ACC + 0.5
                elif self.kind == 'green':
                    self.image = self.game.green_mop_image
                    self.mop_rate = 1
                    self.player_acc = PLAYER_ACC + 1

            elif self.kind == 'blue':
                self.kind = 'red'
                self.image = self.game.red_mop_image
                self.mop_rate = 300
                self.player_acc = PLAYER_ACC + 0.25
            elif self.kind == 'red':
                self.kind = 'yellow'
                self.image = self.game.yellow_mop_image
                self.mop_rate = 100
                self.player_acc = PLAYER_ACC + 0.5
            elif self.kind == 'yellow':
                self.kind = 'green'
                self.image = self.game.green_mop_image
                self.mop_rate = 10
                self.player_acc = PLAYER_ACC + 1

            self.rect = self.image.get_rect()
            self.rect.centerx = self.pos.x
            self.check_collide('x')
            self.rect.centery = self.pos.y
            self.check_collide('y')
            self.rect.center = self.pos
            self.kills = 0
        else:
            self.color_change_pending = True

    def get_powerup(self, kind):
        sound = None
        if kind in ['bleach', 'peroxide']:
            sound = 'invincible'
            self.powerup_start_time = pg.time.get_ticks()
            self.powerup_end_time = 10000
            self.powerup_kind = kind
            self.image = self.game.bleach_mop_image
            if kind == 'bleach':
                self.mop_rate = 0
            else:
                self.mop_rate = 1

        self.game.channel6.stop()
        self.game.channel6.play(self.game.effects_sounds[sound], -1)

    def end_powerup(self):
        if self.powerup_kind != None:
            now = pg.time.get_ticks()
            if now - self.powerup_start_time > self.powerup_end_time:
                self.game.channel6.stop()
                self.powerup_kind = None
                self.change_color(self.kind)
                self.mop_rate = self.previous_mop_rate
                if self.color_change_pending == True:
                    self.change_color()

    def check_collide(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            if dir == 'x':      
                if hits[0].rect.centerx > self.rect.centerx:
                    self.pos.x = hits[0].rect.left - self.rect.width / 2
                if hits[0].rect.centerx < self.rect.centerx:
                    self.pos.x = hits[0].rect.right + self.rect.width / 2
                self.vel.x = 0
                self.rect.centerx = self.pos.x           

            if dir == 'y':
                if hits[0].rect.centery > self.rect.centery:
                    self.pos.y = hits[0].rect.top - self.rect.height / 2
                if hits[0].rect.centery < self.rect.centery:
                    self.pos.y = hits[0].rect.bottom + self.rect.height / 2
                self.vel.y = 0
                self.rect.centery = self.pos.y
           
    def update(self):
        self.acc = vec(0, 0)
        if self.clicked:            
            mouse_movement = vec(pg.mouse.get_rel()).length()
            if mouse_movement > 0:
                self.mouse_pos = vec(pg.mouse.get_pos())
                self.mouse_direction = vec(self.mouse_pos.x - self.pos.x, self.mouse_pos.y - self.pos.y)
                if self.mouse_direction.length() > 0:
                    self.mouse_direction.scale_to_length(self.player_acc)
                    self.acc = self.mouse_direction
                    pg.mouse.set_pos(self.pos.x, self.pos.y)
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.acc.y += self.vel.y * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel #kinematic equation where t = 1

        # Keeps player on screen
        if self.pos.x < TILE_SIZE/2:
            self.pos.x = TILE_SIZE/2
        if self.pos.x > WIDTH - TILE_SIZE/2:
            self.pos.x = WIDTH - TILE_SIZE/2
        if self.pos.y < TILE_SIZE/2:
            self.pos.y = TILE_SIZE/2
        if self.pos.y > HEIGHT - TILE_SIZE/2 - TILE_SIZE:
            self.pos.y = HEIGHT - TILE_SIZE/2 - TILE_SIZE
        self.rect.centerx = self.pos.x
        self.check_collide('x')
        self.rect.centery = self.pos.y
        self.check_collide('y')
        self.rect.center = self.pos
        self.end_powerup()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, tile_image):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = tile_image
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

        self.tilex = x
        self.tiley = y
        # Adds walls to tiles_filed
        self.game.tiles_filled[self.tiley][self.tilex] = 1

    def death(self):
        self.game.tiles_filled[self.tiley][self.tilex] = 0
        self.kill()

class Princess(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.image = self.game.princess_image
        self.princess_win_images = self.game.happy_princess_images
        self.princess_images = [self.game.princess_image, self.game.princess_blink_image]
        self.frame = 0
        self.blink_speed = 100
        self.open_eyes = 2000
        self.last_animate = 0
        self.animate_speed = 1000
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_image = False
        self.tilex = ceil(x / TILE_SIZE)
        self.tiley = ceil(y / TILE_SIZE)
        if self.game.tiles_filled[self.tiley][self.tilex] == 0:
            self.game.tiles_filled[self.tiley][self.tilex] = 3
        else: # If the princess tries to spawn in a wall it finds the first 0 space in that row.
            for i, x in enumerate(self.game.tiles_filled[self.tiley]):
                if x == 0:
                    self.game.tiles_filled[self.tiley][i] = 3
                    self.x = i * TILE_SIZE
                    self.rect.x = self.x #Puts sprite in new location.
                    break

    def update(self):
        if self.game.princess_hit:
            self.animate_speed = 150
            if self.hit_image == False:
                now = pg.time.get_ticks()
                if now - self.last_animate > self.animate_speed:
                    self.animate(self.game.princess_hit_images)
                    self.last_animate = now

        elif self.game.level_won:
            self.animate_speed = 100
            now = pg.time.get_ticks()
            if now - self.last_animate > self.animate_speed:
                self.animate(self.princess_win_images)
                self.last_animate = now
        else:
            if self.frame == 1:
                self.animate_speed = self.open_eyes
            else:
                self.animate_speed = self.blink_speed
            now = pg.time.get_ticks()
            if now - self.last_animate > self.animate_speed:
                self.animate(self.princess_images)
                self.last_animate = now
                self.change_blink()

    def change_blink(self):
        self.blink_speed = randrange(100, 500)
        self.open_eyes = randrange(1000, 8000)

    def animate(self, images):
        if self.frame < len(images):
            self.image = images[self.frame]
            self.frame += 1
            if self.frame >= len(images):
                self.frame = 0
                if self.game.princess_hit:
                    self.hit_image = True
        else:
            self.frame = 0
            if self.game.princess_hit:
                self.hit_image = True
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def death(self):
        self.game.tiles_filled[self.tiley][self.tilex] = 0
        self.game.princess_hit = True
        self.game.princess_hit_time = pg.time.get_ticks()
        self.kill()


           
class Mess(pg.sprite.Sprite):
    def __init__(self, game, x, y, color = 'green', frame = 0):
        self.groups = game.all_sprites, game.messes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(x, y)
        self.color = color
        self.mutate_color = None
        self.frame = frame
        self.set_mess_props()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn_time = pg.time.get_ticks()
        self.mutate_frame = 0
        self.last_growth = randrange(0, 1000)        
        self.last_hit = 0
        self.bad_spawn = False
        self.living = True
        self.tilex = ceil(x / TILE_SIZE)
        self.tiley = ceil(y / TILE_SIZE)
        if self.game.tiles_filled[self.tiley][self.tilex] == 0:
            self.game.tiles_filled[self.tiley][self.tilex] = 2
        elif self.game.tiles_filled[self.tiley][self.tilex] == 3:
            if self.game.princess_hit:
                self.game.tiles_filled[self.tiley][self.tilex] = 2
            else: # Kills messes that spawn at level start on the princess
                self.living = False
                self.kill()

    def set_mess_props(self):
        self.defense = MESS_PROPS['defense'][self.color]
        self.growth_rate = MESS_PROPS['growth rate'][self.color]
        self.image = self.game.mess_images[self.color][self.frame]

    def update(self):
        if not self.living:
            self.death()
        now = pg.time.get_ticks()
        if now - self.spawn_time > randrange(10000, 20000): # Mutates when fully mature.
            if self.color in ['blue', 'black']:
                if self.frame == len(self.game.mess_images[self.color]) - 1:
                    if self.mutate_color != 'slime':
                        if randrange(0, 8) == 1:
                            self.mutate()
                        else:
                            self.spawn_time = now
                    else:
                        self.mutate()
            elif self.frame == len(self.game.mess_images[self.color]) - 1:
                self.mutate()
        if now - self.last_growth > (self.growth_rate + randrange(0, 1000)):
            if self.frame < len(self.game.mess_images) - 3:
                self.frame += 1
                self.image = self.game.mess_images[self.color][self.frame]
                self.rect = self.image.get_rect()
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
            elif self.frame < len(self.game.mess_images) - 2:
                self.frame += 1
                self.image = self.game.mess_images[self.color][self.frame]
                self.rect = self.image.get_rect()
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
                if randrange(0, 40) == 1:
                    self.multiply()
            elif self.frame < len(self.game.mess_images[self.color]) - 1:
                self.frame += 1
                self.image = self.game.mess_images[self.color][self.frame]
                self.rect = self.image.get_rect()
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
                if randrange(0, 10) == 1:
                    self.multiply()
            else:
                self.multiply()
                
            self.last_growth = now

    def gets_hit(self, player):
        now = pg.time.get_ticks()
        if player.powerup_kind == 'bleach':
            player.kills += 1
            self.death()
        if now - self.last_hit > (player.mop_rate + self.defense):
            self.spawn_time = pg.time.get_ticks() # resets the spawn time for mutations.
            self.frame -= 1
            if self.frame < 0:
                if self.color == 'green':
                    points = 1
                elif self.color == 'yellow':
                    points = 2
                elif self.color == 'red':
                    points = 3
                elif self.color == 'blue':
                    points = 4
                elif self.color == 'black':
                    points = 6
                elif self.color == 'pink':
                    points = 4
                elif self.color == 'brown':
                    points = 5
                self.game.score += points
                self.game.level_points += points
                self.living = False
                player.kills += 1
                self.death()
            else:
                self.frame -= 1
                if self.frame < 0:
                    self.frame = 0
            if randrange(0, 10) > 4:        
                sound = choice(['mop0', 'mop1'])
                if not self.game.channel5.get_busy():
                    self.game.channel5.play(self.game.effects_sounds[sound]) 
            self.last_hit = now

    def change_color(self, color):
        old_center = self.rect.center
        self.spawn_time = pg.time.get_ticks()
        self.color = color
        self.set_mess_props()
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def mutate(self):
        temp_surface = pg.Surface((TILE_SIZE, TILE_SIZE), pg.SRCALPHA).convert_alpha()
        if self.color == 'green':
            self.mutate_color = 'yellow'
        elif self.color == 'yellow':
            self.mutate_color = 'red'
        elif self.color == 'red':
            self.mutate_color = 'blue'
        if self.color in ['blue', 'black']:
            if self.game.level > SLIME_LEVEL:
                self.mutate_color = 'slime'
                if self.color == 'blue':
                    self.mutate_images = self.game.mutate_slime_images
                else:
                    self.mutate_images = self.game.black_mutate_slime_images
                if self.mutate_frame < len(self.mutate_images) - 1:
                    self.image = self.mutate_images[self.mutate_frame]
                    self.mutate_frame += 1
                    self.rect = self.image.get_rect()
                    self.rect.x = self.pos.x
                    self.rect.y = self.pos.y
                if self.mutate_frame >= len(self.mutate_images) - 1:
                    self.mutate_slime()
        else:
            self.mutate_images = self.game.mess_images[self.mutate_color]
            if self.mutate_frame < len(self.mutate_images) - 1:
                temp_surface.blit(self.game.mess_images[self.color][5], (0, 0))
                temp_surface.blit(self.mutate_images[self.mutate_frame], (0, 0))
                self.mutate_frame += 1
                self.image = temp_surface
                self.rect = self.image.get_rect()
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
            if self.mutate_frame >= len(self.mutate_images) - 1:
                self.mutate_frame = 0
                self.color = self.mutate_color
                self.set_mess_props()
                self.spawn_time = pg.time.get_ticks()
                self.mutate_color = None

    def mutate_slime(self):
        if self.color == 'black':
            color = 'black'
        else:
            color = 'green'
        Slime(self.game, self.pos.x, self.pos.y, color)
        self.living = False
        self.death()

    def multiply(self):
        growthx = choice([-1, 0, 1])
        growthy = choice([-1, 0, 1])
        if growthx + growthy == 0: #Used for the case that the mess tries to grow where it already is.
            randdig = choice([-1, 1])
            if randdig == -1:
                growthy = randdig
            else:
                growthx = randdig
        newmessx = self.tilex + growthx
        newmessy = self.tiley + growthy
        make_mess = True
        if newmessx < 0:
            make_mess = False
        if newmessy < 0:
            make_mess = False
        if newmessx >= self.game.xtiles:
            make_mess = False
        if newmessy >= self.game.ytiles:
            make_mess = False

        if make_mess:
            if self.game.tiles_filled[newmessy][newmessx] == 3: # Mess lands on princess.
                self.game.princess_hit = True
                self.game.princess_hit_time = pg.time.get_ticks()
                newmess = Mess(self.game, newmessx * TILE_SIZE, newmessy * TILE_SIZE, self.color)
                if not self.game.channel4.get_busy():
                    self.game.channel4.play(self.game.effects_sounds['multiply']) 
            elif self.game.tiles_filled[newmessy][newmessx] == 0:
                newmess = Mess(self.game, newmessx * TILE_SIZE, newmessy * TILE_SIZE, self.color)
                if not self.game.channel4.get_busy():
                    self.game.channel4.play(self.game.effects_sounds['multiply']) 
            elif self.game.tiles_filled[newmessy][newmessx] == 1:
                return            

    def death(self):
        if not self.game.channel3.get_busy():
            self.game.channel3.play(self.game.effects_sounds['death'])
        self.game.tiles_filled[self.tiley][self.tilex] = 0
        self.kill()


class Slime(pg.sprite.Sprite):
    def __init__(self, game, x, y, color='green'):
        self.groups = game.slimes, game.messes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.color = color
        self.mutate_color = None
        self.frame = 0
        self.set_props()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tilex = ceil(x / TILE_SIZE)
        self.tiley = ceil(y / TILE_SIZE)
        self.spawn_time = pg.time.get_ticks()
        self.last_growth = randrange(0, 1000)
        self.last_hit = 0
        self.last_move = 0
        self.animate_speed = 200
        self.last_animate = 0
        self.last_pos_change = 0
        self.bad_spawn = False
        self.living = True
        self.target = self.target_tile = self.pos
        self.prev_pos = 0

    def set_props(self):
        self.move_speed = SLIME_PROPS['move speed'][self.color]
        self.defense = SLIME_PROPS['defense'][self.color]
        self.hp = SLIME_PROPS['hp'][self.color]
        self.acceleration = SLIME_PROPS['acceleration'][self.color]
        self.image = self.game.slime_images[self.color][0]

    def update(self):
        if not self.living:
            self.death()
        now = pg.time.get_ticks()
        if self.color not in ['black', 'blue']:
            if now - self.spawn_time > randrange(10000, 20000):  # Mutates when a random amount of time has past.
                self.mutate()
        if now - self.last_animate > self.animate_speed:
            self.animate()
            self.last_animate = now
        if now - self.last_move > randrange(self.move_speed, 2*self.move_speed):
            if self.pos == self.target:
                self.move()
                self.last_move = now
        if now - self.last_pos_change > self.acceleration:
            if self.pos != self.target:
                if self.pos.x < self.target.x:
                    self.vel.x = 1
                elif self.pos.x > self.target.x:
                    self.vel.x = -1
                if self.pos.y < self.target.y:
                    self.vel.y = 1
                elif self.pos.y > self.target.y:
                    self.vel.y = -1
                self.pos += self.vel
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
                self.last_pos_change = now
            else:
                self.vel = vec(0, 0)

    def check_collide(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            if dir == 'x':
                if hits[0].rect.centerx > self.rect.centerx:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if hits[0].rect.centerx < self.rect.centerx:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.centerx = self.pos.x + self.rect.width / 2

            if dir == 'y':
                if hits[0].rect.centery > self.rect.centery:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if hits[0].rect.centery < self.rect.centery:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.centery = self.pos.y + self.rect.width / 2
            self.move(True)

    def choose_target(self, new = False):
        # This block sets the location of the tile the slime is trying to get to in the long run (self.target_tile).
        if ((self.target_tile - self.pos).length() <= TILE_SIZE) or new:
            # Randomly selects a target tile location if the slime has reached the target location, or is very close.
            xtarget = randrange(0, self.game.xtiles)
            ytarget = randrange(0, self.game.ytiles)
            if self.game.tiles_filled[ytarget][xtarget] == 1:
                # If the slime's target is a wall or the princess it picks first empty slot in row
                for i, x in enumerate(self.game.tiles_filled[ytarget]):
                    if x in [0, 2]:
                        xtarget = i
            self.target_tile = vec(xtarget * TILE_SIZE, ytarget * TILE_SIZE)

    def next_tile(self):
        # This method sets the next tiles to move to (self.target)
        if self.pos.x < self.target_tile.x:
            xdir = 1
        elif self.pos.x > self.target_tile.x:
            xdir = -1
        else:
            xdir = 0
        if self.pos.y < self.target_tile.y:
            ydir = 1
        elif self.pos.x > self.target_tile.y:
            ydir = -1
        else:
            ydir = 0
        dir_vec = vec(xdir * TILE_SIZE, ydir * TILE_SIZE)
        while dir_vec.length() == 0:
            self.choose_target(True)
            if self.pos.x < self.target_tile.x:
                xdir = 1
            elif self.pos.x > self.target_tile.x:
                xdir = -1
            else:
                xdir = 0
            if self.pos.y < self.target_tile.y:
                ydir = 1
            elif self.pos.x > self.target_tile.y:
                ydir = -1
            else:
                ydir = 0
            dir_vec = vec(xdir * TILE_SIZE, ydir * TILE_SIZE)
        self.target = self.pos + dir_vec
        #Keeps target on screen:
        if self.target.x < 0:
            self.target.x = 0
        if self.target.x > WIDTH - TILE_SIZE:
            self.target.x = WIDTH - TILE_SIZE
        if self.target.y < 0:
            self.target.y = 0
        if self.target.y > HEIGHT - (2 * TILE_SIZE):
            self.target.y = HEIGHT - (2 * TILE_SIZE)

    def move(self):
        self.choose_target()
        self.next_tile()
        #Prevents slime from going into walls:
        targety = int(self.target.y / TILE_SIZE)
        targetx = int(self.target.x / TILE_SIZE)
        while self.game.tiles_filled[targety][targetx] == 1:
            self.choose_target(True)
            self.next_tile()
            targety = int(self.target.y / TILE_SIZE)
            targetx = int(self.target.x / TILE_SIZE)

    def animate(self):
        if self.frame < len(self.game.slime_images[self.color]):
            self.image = self.game.slime_images[self.color][self.frame]
            self.frame += 1
            if self.frame >= len(self.game.slime_images[self.color]):
                self.frame = 0
        else:
            self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def gets_hit(self, player):
        if player.powerup_kind == 'peroxide':
            if self.color == 'green':
                points = 10
            elif self.color == 'yellow':
                points = 12
            elif self.color == 'red':
                points = 15
            elif self.color == 'blue':
                points = 20
            elif self.color == 'black':
                points = 30
            self.game.score += points
            self.game.level_points += points
            self.living = False
            self.death()
        else:
            now = pg.time.get_ticks()
            if now - self.last_hit > (player.mop_rate + self.defense):
                self.spawn_time = pg.time.get_ticks()  # resets the spawn time for mutations.
                self.hp -= 1
                if self.hp < 0:
                    if self.color == 'green':
                        points = 10
                    elif self.color == 'yellow':
                        points = 12
                    elif self.color == 'red':
                        points = 15
                    elif self.color == 'blue':
                        points = 20
                    elif self.color == 'black':
                        points = 30
                    self.game.score += points
                    self.game.level_points += points
                    self.living = False
                    self.death()
                else:
                    self.hp -= 1
                if randrange(0, 10) > 4:
                    sound = choice(['mop0', 'mop1'])
                    if not self.game.channel5.get_busy():
                        self.game.channel5.play(self.game.effects_sounds[sound])
                self.last_hit = now

    def mutate(self):
        self.spawn_time = pg.time.get_ticks()
        if self.color == 'green':
            self.color = 'yellow'
        elif self.color == 'yellow':
            self.color = 'red'
        elif self.color == 'red':
            self.color = 'blue'
        elif self.color in ['blue', 'black']:
            return
        self.set_props()

    def change_color(self, color):
        self.spawn_time = pg.time.get_ticks()
        self.color = color
        self.set_props()

    def death(self):
        target_tilex = int(self.rect.centerx / TILE_SIZE)
        targetx = target_tilex * TILE_SIZE
        target_tiley = int(self.rect.centery / TILE_SIZE)
        targety = target_tiley * TILE_SIZE
        target = vec(targetx, targety)
        if not self.game.channel3.get_busy():
            self.game.channel3.play(self.game.effects_sounds['death'])
        Mess(self.game, target.x, target.y, self.color, 3)
        if target.x - TILE_SIZE >= 0:
            newmessy = target_tiley
            newmessx = target_tilex - 1
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mess(self.game, target.x - TILE_SIZE, target.y, self.color, 3)
            elif self.game.tiles_filled[newmessy][newmessx] == 3:
                self.game.princess_hit = True
                self.game.princess_hit_time = self.princess_hit_time = pg.time.get_ticks()
        if target.x + TILE_SIZE <= WIDTH - TILE_SIZE:
            newmessy = target_tiley
            newmessx = target_tilex + 1
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mess(self.game, target.x + TILE_SIZE, target.y, self.color, 3)
            elif self.game.tiles_filled[newmessy][newmessx] == 3:
                self.game.princess_hit = True
                self.game.princess_hit_time = self.princess_hit_time = pg.time.get_ticks()
        if target.y - TILE_SIZE >= 0:
            newmessy = target_tiley - 1
            newmessx = target_tilex
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mess(self.game, target.x, target.y - TILE_SIZE, self.color, 3)
            elif self.game.tiles_filled[newmessy][newmessx] == 3:
                self.game.princess_hit = True
                self.game.princess_hit_time = self.princess_hit_time = pg.time.get_ticks()
        if target.y + TILE_SIZE <= HEIGHT - (2 * TILE_SIZE):
            newmessy = target_tiley + 1
            newmessx = target_tilex
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mess(self.game, target.x, target.y + TILE_SIZE, self.color, 3)
            elif self.game.tiles_filled[newmessy][newmessx] == 3:
                self.game.princess_hit = True
                self.game.princess_hit_time = self.princess_hit_time = pg.time.get_ticks()
        self.kill()



class Mushroom(Mess, pg.sprite.Sprite):
    def __init__(self, game, x, y, color='pink', frame=0):
        self.groups = game.all_sprites, game.messes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(x, y)
        self.color = color
        self.mutate_color = None
        self.frame = frame
        self.set_mess_props()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn_time = pg.time.get_ticks()
        self.mutate_frame = 0
        self.last_growth = randrange(0, 1000)
        self.last_hit = 0
        self.bad_spawn = False
        self.living = True
        self.tilex = ceil(x / TILE_SIZE)
        self.tiley = ceil(y / TILE_SIZE)
        if self.game.tiles_filled[self.tiley][self.tilex] == 0:
            self.game.tiles_filled[self.tiley][self.tilex] = 2
        elif self.game.tiles_filled[self.tiley][self.tilex] == 3:
            if self.game.princess_hit:
                self.game.tiles_filled[self.tiley][self.tilex] = 2
            else:  # Kills messes that spawn at level start on the princess
                self.living = False
                self.kill()

    def set_mess_props(self):
        self.defense = MUSHROOM_PROPS['defense'][self.color]
        self.growth_rate = MUSHROOM_PROPS['growth rate'][self.color]
        self.image = self.game.mushroom_images[self.color][self.frame]

    def update(self):
        if not self.living:
            self.death()
        now = pg.time.get_ticks()
        if now - self.spawn_time > randrange(10000, 20000):  # releases spores when fully mature.
            if self.frame == len(self.game.mushroom_images[self.color]) - 1:
                self.spore()
        if now - self.last_growth > (self.growth_rate + randrange(0, 1000)):
            if self.frame < len(self.game.mushroom_images) - 3:
                self.frame += 1
                self.image = self.game.mushroom_images[self.color][self.frame]
                self.rect = self.image.get_rect()
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
            elif self.frame < len(self.game.mushroom_images) - 2:
                self.frame += 1
                self.image = self.game.mushroom_images[self.color][self.frame]
                self.rect = self.image.get_rect()
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
                if randrange(0, 40) == 1:
                    self.multiply()
            elif self.frame < len(self.game.mushroom_images[self.color]) - 1:
                self.frame += 1
                self.image = self.game.mushroom_images[self.color][self.frame]
                self.rect = self.image.get_rect()
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
                if randrange(0, 10) == 1:
                    self.multiply()
            else:
                self.multiply()

            self.last_growth = now

    def spore(self):
        if len(self.game.spores) < 3:
            if randrange(0, 50 * MUSHROOM_PROPS['spore rate'][self.color]) == 1:
                Spore(self.game, self.rect.center, self.color)


    def multiply(self):
        growthx = choice([-1, 0, 1])
        growthy = choice([-1, 0, 1])
        if growthx + growthy == 0: #Used for the case that the mess tries to grow where it already is.
            randdig = choice([-1, 1])
            if randdig == -1:
                growthy = randdig
            else:
                growthx = randdig
        newmessx = self.tilex + growthx
        newmessy = self.tiley + growthy
        make_mess = True
        if newmessx < 0:
            make_mess = False
        if newmessy < 0:
            make_mess = False
        if newmessx >= self.game.xtiles:
            make_mess = False
        if newmessy >= self.game.ytiles:
            make_mess = False

        if make_mess:
            if self.game.tiles_filled[newmessy][newmessx] == 3: # Mess lands on princess.
                self.game.princess_hit = True
                self.game.princess_hit_time = pg.time.get_ticks()
                newmess = Mushroom(self.game, newmessx * TILE_SIZE, newmessy * TILE_SIZE, self.color)
                if not self.game.channel4.get_busy():
                    self.game.channel4.play(self.game.effects_sounds['multiply'])
            elif self.game.tiles_filled[newmessy][newmessx] == 0:
                newmess = Mushroom(self.game, newmessx * TILE_SIZE, newmessy * TILE_SIZE, self.color)
                if not self.game.channel4.get_busy():
                    self.game.channel4.play(self.game.effects_sounds['multiply'])
            elif self.game.tiles_filled[newmessy][newmessx] == 1:
                return

class Spore(pg.sprite.Sprite):
    def __init__(self, game, pos, color):
        self.groups = game.all_sprites, game.spores
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.color = color
        self.image = game.spore_images[self.color]
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
        self.lifetime = randrange(400, MUSHROOM_PROPS['spore lifetime'][self.color])

        self.rot = randrange(0, 360)
        dir = vec(1, 0).rotate(-self.rot)
        self.vel = dir * MUSHROOM_PROPS['spore speed'][self.color]

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > self.lifetime:
            x = int(self.pos.x / TILE_SIZE) * TILE_SIZE
            y = int(self.pos.y / TILE_SIZE) * TILE_SIZE
            if x < 0:
                x = 0
            if x > WIDTH - TILE_SIZE:
                x = WIDTH - TILE_SIZE
            if y < 0:
                y = 0
            if y > HEIGHT - (2 * TILE_SIZE):
                y = HEIGHT - (2 * TILE_SIZE)
            newmessy = int(y / TILE_SIZE)
            newmessx = int(x / TILE_SIZE)
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mushroom(self.game, x, y, self.color)
            self.kill()




class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y, kind = 'bleach'):
        if kind in ['bleach', 'peroxide']:
            self.groups = game.powerups, game.bleaches
        elif kind == 'bomb':
            self.groups = game.powerups, game.bombs
        else:
            self.groups = game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(x, y)
        self.kind = kind
        image_name = "self.game." + self.kind + "_image"
        self.image = eval(image_name)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn_time = pg.time.get_ticks()
        self.living = True
        if self.kind == "bleach":
            self.life_time = 8000
        elif self.kind == "peroxide":
            self.life_time = 9000
        elif self.kind == "bomb":
            self.life_time = 25000
        else:
            self.life_time = 5000
        self.tilex = ceil(x / TILE_SIZE)
        self.tiley = ceil(y / TILE_SIZE)

    def update(self):
        now = pg.time.get_ticks()
        if now - self.spawn_time > self.life_time:
            self.kill()

    def hit(self, player = None):
        if self.kind in ['bleach', 'peroxide']:
            player.get_powerup(self.kind)
            self.kill()
        elif self.kind == 'bomb':
            now = pg.time.get_ticks()
            if now - self.spawn_time > 1500: # Prevents bombs from exploding right when the spawn on top of you.
                Explosion(self.game, self.rect.center)
                self.kill()

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, center):
        self.groups = game.all_sprites, game.explosions
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 75
        self.game.channel4.play(self.game.effects_sounds['explode'])

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.game.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.game.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Beaker(pg.sprite.Sprite):
    def __init__(self, game, x, y, kind = 'green'):
        self.groups = game.beakers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(x, y)
        self.kind = kind
        self.image = self.game.beaker_images[self.kind]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawn_time = pg.time.get_ticks()
        self.living = True
        self.life_time = 300000
        self.tilex = ceil(x / TILE_SIZE)
        self.tiley = ceil(y / TILE_SIZE)

    def update(self):
        now = pg.time.get_ticks()
        if now - self.spawn_time > self.life_time:
            self.spill()

    def spill(self):
        Splat(self.game, self.rect.center, self.kind)
        self.kill()

class Splat(pg.sprite.Sprite):
    def __init__(self, game, center, color):
        self.groups = game.all_sprites, game.splats
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.color = color
        self.image = self.game.splat_images[self.color][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 75
        self.game.channel4.play(self.game.effects_sounds['shatter'])

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.game.splat_images[self.color]):
                self.splatter()
                self.kill()
            else:
                center = self.rect.center
                self.image = self.game.splat_images[self.color][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

    def splatter(self):
        self.target = vec(self.rect.centerx - TILE_SIZE/2, self.rect.centery - TILE_SIZE/2)
        Mess(self.game, self.target.x, self.target.y, self.color, 3)
        if self.target.x - TILE_SIZE >= 0:
            newmessy = int(self.target.y / TILE_SIZE)
            newmessx = int((self.target.x - TILE_SIZE) / TILE_SIZE)
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mess(self.game, self.target.x - TILE_SIZE, self.target.y, self.color, 3)
            elif self.game.tiles_filled[newmessy][newmessx] == 3:
                self.game.princess_hit = True
                self.game.princess_hit_time = self.princess_hit_time = pg.time.get_ticks()
        if self.target.x + TILE_SIZE <= WIDTH - TILE_SIZE:
            newmessy = int(self.target.y / TILE_SIZE)
            newmessx = int((self.target.x + TILE_SIZE) / TILE_SIZE)
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mess(self.game, self.target.x + TILE_SIZE, self.target.y, self.color, 3)
            elif self.game.tiles_filled[newmessy][newmessx] == 3:
                self.game.princess_hit = True
                self.game.princess_hit_time = self.princess_hit_time = pg.time.get_ticks()
        if self.target.y - TILE_SIZE >= 0:
            newmessy = int((self.target.y - TILE_SIZE) / TILE_SIZE)
            newmessx = int(self.target.x / TILE_SIZE)
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mess(self.game, self.target.x, self.target.y - TILE_SIZE, self.color, 3)
            elif self.game.tiles_filled[newmessy][newmessx] == 3:
                self.game.princess_hit = True
                self.game.princess_hit_time = self.princess_hit_time = pg.time.get_ticks()
        if self.target.y + TILE_SIZE <= HEIGHT - (2 * TILE_SIZE):
            newmessy = int((self.target.y + TILE_SIZE) / TILE_SIZE)
            newmessx = int(self.target.x / TILE_SIZE)
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mess(self.game, self.target.x, self.target.y + TILE_SIZE, self.color, 3)
            elif self.game.tiles_filled[newmessy][newmessx] == 3:
                self.game.princess_hit = True
                self.game.princess_hit_time = self.princess_hit_time = pg.time.get_ticks()
                
        
class GiantSlime(pg.sprite.Sprite):
    def __init__(self, game, x, y, color='green', size = 128):
        self.groups = game.giant_slimes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size = size
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.color = color
        self.mutate_color = None
        self.frame = 0
        self.move_speed = GIANT_SLIME_PROPS['move speed'][self.color]
        self.defense = GIANT_SLIME_PROPS['defense'][self.color]
        self.hp = self.max_hp = GIANT_SLIME_PROPS['hp'][self.color]
        self.acceleration = GIANT_SLIME_PROPS['acceleration'][self.color]
        self.set_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.tilex = ceil(x / TILE_SIZE)
        self.tiley = ceil(y / TILE_SIZE)
        self.spawn_time = pg.time.get_ticks()
        self.last_growth = randrange(0, 1000)
        self.last_hit = 0
        self.hit_count = 0
        self.last_move = 0
        self.animate_speed = 200
        self.last_animate = 0
        self.last_pos_change = 0
        self.bad_spawn = False
        self.living = True
        self.target = self.target_tile = self.pos
        self.jumping = False
        self.jump_up = False
        self.jump_target = None
        self.jump_speed = 3
        self.prev_pos = 0

    def set_images(self):
        self.images = []
        self.jump_images = []
        for i, image in enumerate(self.game.giant_slime_images[self.color]):
            temp_img = self.game.giant_slime_images[self.color][i]
            scaled_image = pg.transform.scale(temp_img, (self.size, self.size))
            self.images.append(scaled_image)
        for i, image in enumerate(self.game.giant_slime_jump_images[self.color]):
            temp_img = self.game.giant_slime_jump_images[self.color][i]
            scaled_image = pg.transform.scale(temp_img, (self.size, self.size))
            self.jump_images.append(scaled_image)

    def update(self):
        if not self.living:
            self.death()
        now = pg.time.get_ticks()
        if not self.jumping:
            if now - self.last_animate > self.animate_speed:
                self.animate()
                self.last_animate = now

            if now - self.last_move > randrange(self.move_speed, self.move_speed * 2):
                if self.pos == self.target:
                    self.move()
                    self.last_move = now

            if now - self.last_pos_change > self.acceleration:
                self.last_pos_change = now
                if self.pos != self.target:
                    if self.pos.x < self.target.x:
                        self.vel.x = 1
                    elif self.pos.x > self.target.x:
                        self.vel.x = -1
                    else:
                        self.vel.x = 0
                    if self.pos.y < self.target.y:
                        self.vel.y = 1
                    elif self.pos.y > self.target.y:
                        self.vel.y = -1
                    else:
                        self.vel.y = 0
                    # Keeps slime on screen
                    if self.pos.x < self.size/2:
                        self.pos.x = self.size/2
                    if self.pos.x > WIDTH - self.size/2:
                        self.pos.x = WIDTH - self.size/2
                    if self.pos.y < self.size/2:
                        self.pos.y = self.size/2
                    if self.pos.y > HEIGHT - 2 * self.size/2:
                        self.pos.y = HEIGHT - 2 * self.size/2
                    self.pos += self.vel
                    self.rect.center = self.pos
                    if self.prev_pos == self.pos:
                        self.move()
                    self.prev_pos == self.pos
                else:
                    self.vel = vec(0, 0)
                    self.move()
        else: #If jumping
            if now - self.last_animate > 100:
                self.animate_jump()
                self.last_animate = now
            if now - self.last_pos_change > 1:
                self.last_pos_change = now
                if (self.pos - self.jump_target).length() > 10:
                    if self.pos.x < self.jump_target.x:
                        self.vel.x = self.jump_speed
                    elif self.pos.x > self.jump_target.x:
                        self.vel.x = -self.jump_speed
                    else:
                        self.vel.x = 0
                    if self.pos.y < self.jump_target.y:
                        self.vel.y = self.jump_speed
                    elif self.pos.y > self.jump_target.y:
                        self.vel.y = -self.jump_speed
                    else:
                        self.vel.y = 0
                    self.pos += self.vel
                    self.rect.center = self.pos
                else:
                    self.vel = vec(0, 0)
                    self.jumping = False
                    if self.jump_up:
                        self.splatter()


    def move(self):
        if randrange(0, 2) == 1:
            self.jumping = True
            self.choose_jump_target()
        if (self.target_tile - self.pos).length() <= self.size:
            # Randomly selects a target tile location if the slime has reached the target location, or is very close.
            border = int(self.size / TILE_SIZE)
            xtarget = randrange(border, self.game.xtiles - border) * TILE_SIZE
            ytarget = randrange(border, self.game.ytiles - (2 * border)) * TILE_SIZE
            self.target_tile = vec(xtarget, ytarget)
        if self.pos.x < self.target_tile.x:
            xdir = 1
        elif self.pos.x > self.target_tile.x:
            xdir = -1
        else:
            xdir = 0
        if self.pos.y < self.target_tile.y:
            ydir = 1
        elif self.pos.x > self.target_tile.y:
            ydir = -1
        else:
            ydir = 0
        dir_vec = vec(xdir * TILE_SIZE, ydir * TILE_SIZE)
        self.target = self.pos + dir_vec

        #Keeps target on screen:
        if self.target.x < 0:
            self.target.x = 0
        if self.target.x > WIDTH - TILE_SIZE:
            self.target.x = WIDTH - TILE_SIZE
        if self.target.y < 0:
            self.target.y = 0
        if self.target.y > HEIGHT - (2 * TILE_SIZE):
            self.target.y = HEIGHT - (2 * TILE_SIZE)

    def choose_jump_target(self):
        if not self.jump_up:
            targetx = randrange(int(self.size/2), int(WIDTH - self.size/2))
            targety = randrange(int(HEIGHT/2), int(HEIGHT - self.size - (2 * TILE_SIZE)))
            self.jump_up = True
        else:
            targetx = randrange(int(self.size/2), int(WIDTH - self.size/2))
            targety = randrange(int(self.size/2), int(HEIGHT/2))
            self.jump_up = False
        self.jump_target = vec(targetx, targety)

    def animate_jump(self):
        if self.jumping:
            if self.frame < len(self.jump_images):
                self.image = self.jump_images[self.frame]
                self.frame += 1
                if self.frame >= len(self.jump_images):
                    self.frame = 0
            else:
                self.frame = 0

    def animate(self):
        if self.frame < len(self.images):
            self.image = self.images[self.frame]
            self.frame += 1
            if self.frame >= len(self.images):
                self.frame = 0
        else:
            self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def gets_hit(self, player = None):
        now = pg.time.get_ticks()
        mop_rate = 199
        if player != None:
            mop_rate = player.mop_rate
            if mop_rate < 100:
                mop_rate = 100
            elif mop_rate < 200:
                mop_rate = 120

        if now - self.last_hit > (mop_rate + self.defense):
            self.spawn_time = pg.time.get_ticks()  # resets the spawn time for mutations.
            self.hp -= 1
            if mop_rate == 199:
                self.hp -= 5
            if self.hp < 0:
                if self.color == 'green':
                    points = 1000
                elif self.color == 'yellow':
                    points = 1200
                elif self.color == 'red':
                    points = 1500
                elif self.color == 'blue':
                    points = 2000
                elif self.color == 'black':
                    points = 3000
                self.game.score += points
                self.game.level_points += points
                self.living = False
                self.death()
            else:
                self.hp -= 1
            if randrange(0, 10) > 4:
                sound = choice(['mop0', 'mop1'])
                if not self.game.channel5.get_busy():
                    self.game.channel5.play(self.game.effects_sounds[sound])
            self.last_hit = now
            self.hit_count += 1

        if self.hit_count == 2:
            self.jumping = True
            self.choose_jump_target()

        if self.hit_count >= 5:
            self.hit_count = 0
            self.size = int(self.size * self.hp/self.max_hp)
            if self.size < TILE_SIZE:
                self.death()
            self.shrink()

    def shrink(self):
        if self.size > 20:
            xs = choice([-1, 1])
            ys = choice([-1, 1])
            x = int((self.pos.x + randrange(0, int(self.size/2)) * xs - TILE_SIZE/2) / TILE_SIZE) * TILE_SIZE
            y = int((self.pos.y + randrange(0, int(self.size/2)) * ys - TILE_SIZE/2) / TILE_SIZE) * TILE_SIZE
            Slime(self.game, x, y, color = self.color)
        self.move_speed = int(self.move_speed * .90)
        self.defense = int(self.defense * .90)
        self.acceleration = int(self.acceleration * .90)
        self.set_images()
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def splatter(self):
        targetx = int(self.pos.x / TILE_SIZE) * TILE_SIZE
        targety = int(self.pos.y / TILE_SIZE) * TILE_SIZE
        target = vec(targetx, targety)
        Mess(self.game, target.x, target.y, self.color, 3)
        if target.x - TILE_SIZE >= 0:
            newmessy = int(target.y / TILE_SIZE)
            newmessx = int((target.x - TILE_SIZE) / TILE_SIZE)
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mess(self.game, target.x - TILE_SIZE, target.y, self.color, 3)
            elif self.game.tiles_filled[newmessy][newmessx] == 3:
                self.game.princess_hit = True
                self.game.princess_hit_time = self.princess_hit_time = pg.time.get_ticks()
        if target.x + TILE_SIZE <= WIDTH - TILE_SIZE:
            newmessy = int(target.y / TILE_SIZE)
            newmessx = int((target.x + TILE_SIZE) / TILE_SIZE)
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mess(self.game, target.x + TILE_SIZE, target.y, self.color, 3)
            elif self.game.tiles_filled[newmessy][newmessx] == 3:
                self.game.princess_hit = True
                self.game.princess_hit_time = self.princess_hit_time = pg.time.get_ticks()
        if target.y - TILE_SIZE >= 0:
            newmessy = int((target.y - TILE_SIZE) / TILE_SIZE)
            newmessx = int(target.x / TILE_SIZE)
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mess(self.game, target.x, target.y - TILE_SIZE, self.color, 3)
            elif self.game.tiles_filled[newmessy][newmessx] == 3:
                self.game.princess_hit = True
                self.game.princess_hit_time = self.princess_hit_time = pg.time.get_ticks()
        if target.y + TILE_SIZE <= HEIGHT - (2 * TILE_SIZE):
            newmessy = int((target.y + TILE_SIZE) / TILE_SIZE)
            newmessx = int(target.x / TILE_SIZE)
            if self.game.tiles_filled[newmessy][newmessx] == 0:
                Mess(self.game, target.x, target.y + TILE_SIZE, self.color, 3)
            elif self.game.tiles_filled[newmessy][newmessx] == 3:
                self.game.princess_hit = True
                self.game.princess_hit_time = self.princess_hit_time = pg.time.get_ticks()

    def death(self):
        x = int(self.pos.x / TILE_SIZE) * TILE_SIZE
        y = int(self.pos.y / TILE_SIZE) * TILE_SIZE
        Slime(self.game, x, y, color=self.color)
        self.kill()


