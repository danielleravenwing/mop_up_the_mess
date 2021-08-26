# Mop Us the Mess by Raven Ironwing and Joshua D.

import pygame as pg #lets you rename pygame
import random, os
from settings import *
from sprites import *
from os import path, listdir
from random import choice, randrange, shuffle
from math import ceil

main_folder = path.dirname(__file__)
#main_folder = '' #Uncomment when using pyinstaller.
game_folder = path.join(main_folder, 'assets')
snd_folder = path.join(game_folder, 'snd')
music_folder = path.join(game_folder, 'music')
img_folder = path.join(game_folder, 'img')
walls_folder = path.join(img_folder, 'walls')
floors_folder = path.join(img_folder, 'floors')




class Game:
    def __init__(self):
        # initialize pygame and create window
        pg.mixer.pre_init(44100, -16, 4, 2048)  # reduces delay in sound playback.
        pg.init()
        pg.mixer.init()
        pg.joystick.init()  # Initializes all joysticks/controllers
        self.joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
        self.num_joysticks = len(self.joysticks)
        self.num_players_selected = False
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.flags = pg.SCALED | pg.RESIZABLE
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), self.flags)
        pg.display.set_caption(TITLE)
        icon_image = pg.image.load(path.join(img_folder, 'mopmessicon.png'))
        pg.display.set_icon(icon_image)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME) #finds the closest match on computer
        self.xtiles = ceil(WIDTH / TILE_SIZE)
        self.ytiles = ceil(HEIGHT / TILE_SIZE) - 1
        self.num_tiles = self.xtiles * self.ytiles
        self.channel3 = pg.mixer.Channel(2)
        self.channel4 = pg.mixer.Channel(3)
        self.channel5 = pg.mixer.Channel(4)
        self.channel6 = pg.mixer.Channel(5)
        self.mouse_player = False

        # Sprite groups
        self.all_sprites = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.group_cols = [[], [], [], []]
        self.unclicked_group_cols = []
        self.walls = pg.sprite.Group()
        self.messes = pg.sprite.Group()
        self.slimes = pg.sprite.Group()
        self.giant_slimes = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.bleaches = pg.sprite.Group()
        self.bombs = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.splats = pg.sprite.Group()
        self.beakers = pg.sprite.Group()
        self.spores = pg.sprite.Group()

        #loads images
        title = pg.image.load(path.join(img_folder, 'title.png')).convert()
        self.twidth = title.get_width()
        self.theight = title.get_height()
        scale = HEIGHT/self.theight
        self.twidth = self.twidth*scale
        self.theight = self.theight*scale
        self.title_image = pg.transform.scale(title, (int(self.twidth), int(self.theight)))
        logo = pg.image.load(path.join(img_folder, 'a two headed snick.png')).convert_alpha()
        self.logo_image = pg.transform.scale(logo, (128, 128))
        self.blue_mop_image = pg.image.load(path.join(img_folder, 'blue_mop.png')).convert_alpha()
        self.red_mop_image = pg.image.load(path.join(img_folder, 'red_mop.png')).convert_alpha()
        self.yellow_mop_image = pg.image.load(path.join(img_folder, 'yellow_mop.png')).convert_alpha()
        self.green_mop_image = pg.image.load(path.join(img_folder, 'green_mop.png')).convert_alpha()
        self.princess_image = pg.image.load(path.join(img_folder, 'princess.png')).convert_alpha()
        self.princess_blink_image = pg.image.load(path.join(img_folder, 'princess_blink.png')).convert_alpha()
        self.bleach_image = pg.image.load(path.join(img_folder, 'bleach.png')).convert_alpha()
        self.peroxide_image = pg.image.load(path.join(img_folder, 'peroxide.png')).convert_alpha()
        self.blink_image = pg.image.load(path.join(img_folder, 'blink.png')).convert_alpha()
        self.bombbox_image = pg.image.load(path.join(img_folder, 'bombbox.png')).convert_alpha()
        self.bomb_image = pg.image.load(path.join(img_folder, 'bomb.png')).convert_alpha()
        self.set_bomb_image = pg.image.load(path.join(img_folder, 'set_bomb.png')).convert_alpha()
        self.bleach_mop_image = pg.image.load(path.join(img_folder, 'bleach_mop.png')).convert_alpha()
        self.bow_image = pg.image.load(path.join(img_folder, 'bow.png')).convert_alpha()
        self.eyepatch_image = pg.image.load(path.join(img_folder, 'eyepatch.png')).convert_alpha()
        self.hat_image = pg.image.load(path.join(img_folder, 'hat.png')).convert_alpha()
        self.babs_image = pg.image.load(path.join(img_folder, 'babs.png')).convert_alpha()
        self.mustache_image = pg.image.load(path.join(img_folder, 'mustache.png')).convert_alpha()
        self.accessorys = [self.bow_image, self.hat_image, self.eyepatch_image, self.babs_image, self.mustache_image]
        self.wall_images = []
        number_of_files = len([name for name in listdir(walls_folder) if path.isfile(path.join(walls_folder, name))])
        for i in range(0, number_of_files):
            filename = 'wall{}.png'.format(i)
            img = pg.image.load(path.join(walls_folder, filename)).convert()
            self.wall_images.append(img)
        self.floor_images = []
        number_of_files = len([name for name in listdir(floors_folder) if path.isfile(path.join(floors_folder, name))])
        for i in range(0, number_of_files):
            filename = 'floor{}.png'.format(i)
            img = pg.image.load(path.join(floors_folder, filename)).convert()
            self.floor_images.append(img)

        self.mutate_slime_images = []
        for i in range(0, 6):
            filename = 'mutate_slime{}.png'.format(i)
            img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
            self.mutate_slime_images.append(img)

        self.princess_hit_images = []
        for i in range(0, 14):
            filename = 'princess_hit{}.png'.format(i)
            img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
            self.princess_hit_images.append(img)

        self.happy_princess_images = []
        for i in range(0, 4):
            filename = 'happy_princess{}.png'.format(i)
            img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
            self.happy_princess_images.append(img)

        self.black_mutate_slime_images = []
        for i in range(0, 6):
            filename = 'black_mutate_slime{}.png'.format(i)
            img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
            self.black_mutate_slime_images.append(img)

        self.mess_images = {}
        for color in MESS_COLORS:
            self.mess_images[color] = []
            for i in range(0, 6):
                filename = color + '_mess{}.png'.format(i)
                img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
                self.mess_images[color].append(img)

        self.mushroom_images = {}
        for color in MUSHROOM_COLORS:
            self.mushroom_images[color] = []
            for i in range(0, 6):
                filename = color + '_mushroom{}.png'.format(i)
                img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
                self.mushroom_images[color].append(img)

        self.spore_images = {}
        for color in MUSHROOM_COLORS:
            filename = color + '_spore.png'
            img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
            self.spore_images[color] = img

        self.splat_images = {}
        for color in MESS_COLORS:
            self.splat_images[color] = []
            for i in range(0, 6):
                filename = color + '_splat.png'
                temp_img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
                img = pg.transform.scale(temp_img, ((20 * i) + 32, (20 * i) + 32))
                self.splat_images[color].append(img)

        self.beaker_images = {}
        for color in MESS_COLORS:
            filename = color + '_beaker.png'
            img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
            self.beaker_images[color] = img

        self.slime_images = {}
        for color in MESS_COLORS:
            self.slime_images[color] = []
            for i in range(0, 4):
                filename = color + '_slime{}.png'.format(i)
                img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
                self.slime_images[color].append(img)

        self.giant_slime_images = {}
        for color in GIANT_SLIME_COLORS:
            self.giant_slime_images[color] = []
            for i in range(0, 6):
                filename = 'giant_' + color + '_slime{}.png'.format(i)
                img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
                self.giant_slime_images[color].append(img)

        self.giant_slime_jump_images = {}
        for color in GIANT_SLIME_COLORS:
            self.giant_slime_jump_images[color] = []
            for i in range(0, 6):
                filename = 'giant_' + color + '_slime_jump{}.png'.format(i)
                img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
                self.giant_slime_jump_images[color].append(img)

        self.explosion_anim = []
        for i in range(8):
            filename = 'regularExplosion0{}.png'.format(i)
            temp_img = pg.image.load(path.join(img_folder, filename)).convert_alpha()
            img = pg.transform.scale(temp_img, (128, 128))
            self.explosion_anim.append(img)

        #Creates tiled floor background images
        self.floor_backgrounds = []
        for img in self.floor_images:
            floor = self.draw_floor(img)
            self.floor_backgrounds.append(floor)

        # Loads music
        self.music_list = []
        number_of_files = len([name for name in listdir(music_folder) if path.isfile(path.join(music_folder, name))])
        for i in range(0, number_of_files):
            filename = 'music{}.ogg'.format(i)
            song = path.join(music_folder, filename)
            self.music_list.append(song)
        self.end_music = path.join(game_folder, 'end_music.ogg')
        self.lose_music = path.join(game_folder, 'lose_music.ogg')
        self.boss_music = path.join(game_folder, 'boss_music.ogg')
        # Loads sound effects
        self.effects_sounds = {}
        for key in EFFECTS_SOUNDS:
            self.effects_sounds[key] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[key]))

    def draw_floor(self, floor_image):
        floor_surface = pg.Surface((WIDTH, HEIGHT))
        for y in range(0, self.ytiles):
            for x in range(0, self.xtiles):
                floor_surface.blit(floor_image, (x * TILE_SIZE, y * TILE_SIZE))
        return floor_surface

    def generage_walls(self):
        num_walls = int(self.level / 2) * 4
        if num_walls > 10:
            num_walls = 10
        
        wall_image = choice(self.wall_images)
        for i in range(0, num_walls):
            wallx = randrange(1, self.xtiles - 1)
            wally = randrange(1, self.ytiles - 1)
            wall_dir = choice([0, 1])
            if wall_dir == 0:
                wallw = randrange(0, int(self.xtiles/2))
                wallh = 1
            else:
                wallh = randrange(0, int(self.ytiles/2))
                wallw = 1
            if wallh == 1:
                for i in range (0, wallw):
                    if wallx + i < self.xtiles - 1:
                        wall = Wall(self, wallx + i, wally, wall_image)
                    else:
                        break
            if wallw == 1:
                for i in range (0, wallh):
                    if wally + i < self.ytiles - 1:
                        wall = Wall(self, wallx, wally + i, wall_image)
                    else:
                        break

    def spawn_mess(self):
        if self.level < 25:
            num_messes = 1 + ceil(self.level / 5)
        elif self.level < 50:
            num_messes = 1 + ceil(self.level / 7)
        elif self.level < 75:
            num_messes = 1 + ceil(self.level / 8)
        elif self.level < 100:
            num_messes = 1 + ceil(self.level / 9)

        i = 0
        prob = [1]
        if self.level < 25:
            prob = [1]
        elif self.level < 50:
            prob = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2]
        elif self.level < 75:
            prob = [1, 1, 1, 1, 1, 1, 2, 2, 2]
        elif self.level < 100:
            prob = [1, 1, 1, 1, 2, 2, 3]
        while i < num_messes:
            make_mess = choice(prob)
            messx = randrange(0, self.xtiles) * TILE_SIZE
            messy = randrange(0, self.ytiles) * TILE_SIZE
            if make_mess == 1:
                Mess(self, messx, messy)
            elif make_mess == 2:
                Mushroom(self, messx, messy)
            elif make_mess == 3:
                Mushroom(self, messx, messy, 'brown')
            # Kills messes that spawn on walls
            hits = pg.sprite.groupcollide(self.messes, self.walls, True, False)
            if not hits:
                i += 1


    def new(self):
        #start a new game
        shuffle(self.accessorys)
        self.won = False
        self.level_won = False
        self.princess_hit = False
        self.princess_hit_time = 0
        self.level = 1
        self.win_time = 0
        self.score = 0
        self.new_level()
        self.run()
        
    def new_level(self):
        pg.mouse.set_visible(True)
        for powerup in self.powerups:
            powerup.kill()
        for explosion in self.explosions:
            explosion.kill()
        for beaker in self.beakers:
            beaker.kill()
        for spore in self.spores:
            spore.kill()
        for giant_slime in self.giant_slimes:
            giant_slime.kill()
        self.channel6.stop()
        self.level_won = False
        self.level_points = 0
        self.tiles_filled = [] #Used to keep track of which tiles have things in.
        for y in range(0, self.ytiles):
            row = []
            for x in range(0, self.xtiles):
                row.append(0)
            self.tiles_filled.append(row)
        if self.level != 1:
            self.princess.kill()
            for player in self.players:
                player.kill()
        if self.level in [25, 50, 75, 100]:
            song = self.boss_music
        else:
            song = choice(self.music_list)
        pg.mixer.music.load(song)
        pg.mixer.music.play(loops=-1)
        self.background_img = choice(self.floor_backgrounds)
        for wall in self.walls:
            wall.kill()
        if self.level not in [25, 50, 75, 100]:
            self.generage_walls()
        x = randrange(0, self.xtiles) * TILE_SIZE
        if self.level in [25, 50, 75, 100]:
            y = (self.ytiles - 2) * TILE_SIZE
        else:
            y = randrange(0, self.ytiles) * TILE_SIZE
        self.princess = Princess(self, x, y)
        x = randrange(0, self.xtiles) * TILE_SIZE
        y = randrange(0, self.ytiles) * TILE_SIZE
        if self.level not in [25, 50, 75, 100]:
            self.spawn_mess()
            self.spawn_beakers()
        if self.num_joysticks == 0:
            player = Player(self, x, y, 'blue', 0)
            player.clicked = True
            pg.mouse.set_visible(False)
        elif not self.mouse_player:
            for i in range(0, self.num_joysticks):
                x = randrange(0, self.xtiles) * TILE_SIZE
                y = randrange(0, self.ytiles) * TILE_SIZE
                player = Player(self, x, y, 'blue', i)
                player.clicked = True
                pg.mouse.set_visible(False)
        else:
            for i in range(0, self.num_joysticks + 1):
                x = randrange(0, self.xtiles) * TILE_SIZE
                y = randrange(0, self.ytiles) * TILE_SIZE
                player = Player(self, x, y, 'blue', i)
                player.clicked = True
                pg.mouse.set_visible(False)

        pg.sprite.groupcollide(self.beakers, self.players, True, False) #kills beakers that the player spawns on top of.
        self.red_player = None
        self.yellow_player = None


        if self.level == 25:
            GiantSlime(self, WIDTH/2, 75, 'green')
        elif self.level == 50:
            GiantSlime(self, WIDTH / 2, 75, 'yellow')
        elif self.level == 75:
            GiantSlime(self, WIDTH / 2, 75, 'red')
        elif self.level == 100:
            GiantSlime(self, WIDTH / 2, 75, 'blue')

    def spawn_beakers(self):
        if self.level > 15:
            if self.level < 25:
                colors = ['green']
            elif self.level < 40:
                colors = ['green', 'yellow']
            elif self.level < 50:
                colors = ['green', 'yellow', 'red']
            elif self.level < 60:
                colors = ['green', 'yellow', 'red', 'blue']
            elif self.level < 75:
                colors = MESS_COLORS
            elif self.level < 85:
                colors = ['yellow', 'red', 'blue', 'black']
            else:
                colors = ['red', 'blue', 'black']

            if self.level < 25:
                num_beakers = ceil(self.level / 13)
            elif self.level < 50:
                num_beakers = ceil(self.level / 14)
            elif self.level < 75:
                num_beakers = ceil(self.level / 16)
            elif self.level < 100:
                num_beakers = ceil(self.level / 18)
            if num_beakers != 0:
                for i in range(0, num_beakers):
                    x = randrange(0, self.xtiles) * TILE_SIZE
                    y = randrange(0, self.ytiles) * TILE_SIZE
                    Beaker(self, x, y, choice(colors))
                    pg.sprite.groupcollide(self.beakers, self.walls, True, False)
                    pg.sprite.spritecollide(self.princess, self.beakers, True)
                    pg.sprite.groupcollide(self.beakers, self.powerups, False, True)
                    pg.sprite.groupcollide(self.beakers, self.messes, True, True)

    def update_unclicked_group_cols(self):
        self.unclicked_group_cols = [] # Makes a list of unclicked players.
        for group in self.group_cols:
            glist = []
            for player in group:
                if not player.clicked:
                    glist.append(player)
            self.unclicked_group_cols.append(glist)

    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #game loop - update
        self.all_sprites.update()
        self.slimes.update()
        self.powerups.update()
        self.beakers.update()
        self.giant_slimes.update()
        self.players.update()
        
        #check for collisions
        hits = pg.sprite.groupcollide(self.messes, self.players, False, False)
        for mess in hits:
            for player in hits[mess]:
                mess.gets_hit(player)
        hits = pg.sprite.groupcollide(self.giant_slimes, self.players, False, False)
        for mess in hits:
            for player in hits[mess]:
                mess.gets_hit(player)
        hits = pg.sprite.spritecollide(self.princess, self.slimes, False)
        for slime in hits:
            self.princess_hit = True
            self.princess_hit_time = pg.time.get_ticks()
            slime.death()
        hits = pg.sprite.groupcollide(self.powerups, self.players, False, False)
        for powerup in hits:
            for player in hits[powerup]:
                powerup.hit(player)

        hits = pg.sprite.groupcollide(self.beakers, self.players, False, False)
        for beaker in hits:
            self.score += 10
            beaker.spill()

        hits = pg.sprite.groupcollide(self.beakers, self.slimes, False, False)
        for beaker in hits:
            beaker.spill()

        hits = pg.sprite.groupcollide(self.beakers, self.messes, False, False)
        for beaker in hits:
            if randrange(0, 100) == 1:
                beaker.spill()

        hits = pg.sprite.groupcollide(self.explosions, self.beakers, False, False, pg.sprite.collide_circle_ratio(0.80))
        for exp in hits:
            for beaker in hits[exp]:
                beaker.spill()

        hits = pg.sprite.groupcollide(self.explosions, self.bombs, False, False, pg.sprite.collide_circle_ratio(0.80))
        for exp in hits:
            for bomb in hits[exp]:
                bomb.hit()

        hits = pg.sprite.groupcollide(self.slimes, self.bombs, False, False)
        for slime in hits:
            for bomb in hits[slime]:
                bomb.hit()

        hits = pg.sprite.groupcollide(self.giant_slimes, self.bombs, False, False)
        for slime in hits:
            for bomb in hits[slime]:
                bomb.hit()

        hits = pg.sprite.groupcollide(self.splats, self.slimes, False, False, pg.sprite.collide_circle_ratio(1))
        for splat in hits:
            for slime in hits[splat]:
                slime.change_color(splat.color)

        hits = pg.sprite.groupcollide(self.splats, self.messes, False, False, pg.sprite.collide_circle_ratio(1.2))
        for splat in hits:
            for mess in hits[splat]:
                mess.change_color(splat.color)
        hits = pg.sprite.groupcollide(self.explosions, self.walls, False, False, pg.sprite.collide_circle_ratio(0.80))
        for exp in hits:
            for wall in hits[exp]:
                wall.death()
        hits = pg.sprite.groupcollide(self.explosions, self.messes, False, False, pg.sprite.collide_circle_ratio(0.80))
        for exp in hits:
            for mess in hits[exp]:
                mess.death()
        hits = pg.sprite.groupcollide(self.explosions, self.giant_slimes, False, False, pg.sprite.collide_circle_ratio(0.80))
        for exp in hits:
            for mess in hits[exp]:
                mess.gets_hit()
        hits = pg.sprite.groupcollide(self.explosions, self.slimes, False, False, pg.sprite.collide_circle_ratio(0.70))
        for exp in hits:
            for slime in hits[exp]:
                slime.death()
        hits = pg.sprite.spritecollide(self.princess, self.explosions, False, pg.sprite.collide_circle_ratio(0.70))
        if hits:
            self.princess_hit = True
            self.princess_hit_time = pg.time.get_ticks()
        hits = pg.sprite.spritecollide(self.princess, self.splats, False, pg.sprite.collide_circle_ratio(1))
        if hits:
            self.princess_hit = True
            self.princess_hit_time = pg.time.get_ticks()

        hits = pg.sprite.groupcollide(self.players, self.explosions, False, False, pg.sprite.collide_circle_ratio(0.70))
        for hit in hits:
            if hit.powerup_kind in ["bleach", "peroxide"]:
                self.channel6.stop()
            if hit.clicked:
                pg.mouse.set_visible(True)
            hit.kill()

        if len(self.messes) < 1:
            if len(self.giant_slimes) < 1:
                now = pg.time.get_ticks()
                if not self.level_won:
                    self.level += 1
                    self.win_time = now
                    self.level_won = True
                    pg.mixer.music.stop()
                    self.effects_sounds['levelup'].play()
                if now - self.win_time > END_LEVEL_DELAY:
                    if self.level > 100:
                        if not self.won:
                            self.won = True
                            self.end_screen()
                    else:
                        self.new_level()
        # Ends the game if the mess grows to fill most of the screen
        #if len(self.messes) > self.num_tiles - 20:
        #    self.playing = False

        # Powerups
        if self.level_points > 50:
            if self.red_player == None:
                x = randrange(0, self.xtiles) * TILE_SIZE
                y = randrange(0, self.ytiles) * TILE_SIZE
                self.red_player = Player(self, x, y, 'red')
        if self.level_points > 100:
            if self.yellow_player == None:
                x = randrange(0, self.xtiles) * TILE_SIZE
                y = randrange(0, self.ytiles) * TILE_SIZE
                self.yellow_player = Player(self, x, y, 'yellow')

        if len(self.bleaches) == 0:
            if randrange(0, 3000) == 1:
                x = randrange(0, self.xtiles) * TILE_SIZE
                y = randrange(0, self.ytiles) * TILE_SIZE
                PowerUp(self, x, y, 'bleach')
                hits = pg.sprite.groupcollide(self.powerups, self.walls, True, False)
                hits = pg.sprite.spritecollide(self.princess, self.powerups, True)

        if len(self.bleaches) == 0:
            if randrange(0, 5000) == 1:
                x = randrange(0, self.xtiles) * TILE_SIZE
                y = randrange(0, self.ytiles) * TILE_SIZE
                PowerUp(self, x, y, 'peroxide')
                hits = pg.sprite.groupcollide(self.powerups, self.walls, True, False)
                hits = pg.sprite.spritecollide(self.princess, self.powerups, True)

        if len(self.bombs) < 6:
            if randrange(0, 1000) == 1:
                x = randrange(0, self.xtiles) * TILE_SIZE
                y = randrange(0, self.ytiles) * TILE_SIZE
                PowerUp(self, x, y, 'bomb')
                hits = pg.sprite.groupcollide(self.powerups, self.walls, True, False)
                hits = pg.sprite.spritecollide(self.princess, self.powerups, True)

        if len(self.bombs) < 2:
            if randrange(0, 2000) == 1:
                x = randrange(0, self.xtiles) * TILE_SIZE
                y = randrange(0, self.ytiles) * TILE_SIZE
                PowerUp(self, x, y, 'bombbox')
                hits = pg.sprite.groupcollide(self.powerups, self.walls, True, False)
                hits = pg.sprite.spritecollide(self.princess, self.powerups, True)

        if self.princess_hit == True:
            now = pg.time.get_ticks()
            if (now - self.princess_hit_time) > 5000:
                self.playing = False

        if len(self.players) < 1:
            now = pg.time.get_ticks()
            if (now - self.princess_hit_time) > 5000:
                self.playing = False
     
    def events(self):
        # gets state of hat for moving sponge.
        if pg.joystick.get_init:
            if self.num_joysticks > 0:
                for i in range(0, self.num_joysticks):
                    stick = self.joysticks[i]
                    for player in self.players:
                        if player.clicked and (player.player_num == i):
                            hat_state = stick.get_hat(0)
                            player.vel.x += hat_state[0] * player.player_acc
                            player.vel.y += hat_state[1] * -player.player_acc
                            stick_x = stick.get_axis(0)
                            stick_y = stick.get_axis(1)
                            deadzone = 0.2
                            if abs(stick_x) > deadzone:
                                player.vel.x += stick_x * player.player_acc
                            if abs(stick_y) > deadzone:
                                player.vel.y += stick_y * player.player_acc

        #game loop - events
        self.update_unclicked_group_cols()

        for event in pg.event.get():
        # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.JOYBUTTONDOWN:
                for i in range(0, self.num_joysticks):
                    stick = self.joysticks[i]
                    b0 = stick.get_button(0)
                    b1 = stick.get_button(1)
                    b2 = stick.get_button(2)
                    b3 = stick.get_button(3)
                    b5 = stick.get_button(5)
                    if b5:
                        for player in self.players:
                            if player.player_num == i:
                                player.drop_bomb()
                    butts = [b0, b1, b2, b3]
                    for color, group in enumerate(self.unclicked_group_cols):
                        if butts[color]:
                            if len(group) > 1:
                                player = choice(group) # Picks a random one in the color group
                                player.clicked = True
                                self.update_unclicked_group_cols()
                            elif len(group) == 1:
                                player = group[0]
                                player.clicked = True
                                self.update_unclicked_group_cols()
                            else:
                                break
                            for sponge in self.players: # deactivates the old sponge.
                                if sponge.player_num == i:
                                    sponge.clicked = False
                                    self.update_unclicked_group_cols()
                                    sponge.player_num = 10  # 10 indicates that no player is controlling the sponge.
                            player.player_num = i
                            if not self.mouse_player:
                                pg.mouse.set_visible(False)
                            break

                if event.button in [7, 9]:
                    self.draw_text("Paused", 100, RED, WIDTH/2, HEIGHT/3)
                    pg.display.flip()
                    self.wait_for_key()
                elif event.button in [8, 10]:
                    if self.playing:
                        self.playing = False
                    self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if pg.mouse.get_pressed(num_buttons=3) == (0, 0, 1):
                    for player in self.players:
                        if player.player_num == self.num_joysticks:
                            player.drop_bomb()
                elif pg.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                    # get a list of all sprites that are under the mouse cursor
                    self.clicked_sprites = [s for s in self.players if s.rect.collidepoint(pos)]
                    for sprite in self.clicked_sprites:
                        if sprite in self.players:
                            if not (sprite.player_num < self.num_joysticks):
                                sprite.clicked = not sprite.clicked
                                if sprite.clicked:
                                    sprite.player_num = self.num_joysticks
                                    pg.mouse.set_visible(False)
                                else:
                                    sprite.player_num = 10
                                    pg.mouse.set_visible(True)

                    self.clicked_sprites = [s for s in self.bombs if s.rect.collidepoint(pos)]
                    for sprite in self.clicked_sprites:
                        if sprite in self.bombs:
                            self.score += 10
                            sprite.hit(None)
                    self.clicked_sprites = [s for s in self.beakers if s.rect.collidepoint(pos)]
                    for sprite in self.clicked_sprites:
                        if sprite in self.beakers:
                            self.score += 50
                            sprite.spill()

            #if event.type == pg.MOUSEBUTTONUP:
            #    for sprite in self.players:
            #        sprite.clicked = False
            #    pg.mouse.set_visible(True)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.draw_text("Paused", 100, RED, WIDTH/2, HEIGHT/3)
                    pg.display.flip()
                    self.wait_for_key()
                if event.key == pg.K_EQUALS:
                    for mess in self.messes:
                        mess.kill()
                    if not self.level_won:
                        self.level += 1
                        self.win_time = pg.time.get_ticks()
                        self.level_won = True
                        pg.mixer.music.stop()
                        self.effects_sounds['levelup'].play()
                        if self.level > 100:
                            if not self.won:
                                self.won = True
                                self.end_screen()
                        else:
                            self.new_level()
                if event.key == pg.K_MINUS:
                    for mess in self.messes:
                        mess.kill()
                    if not self.level_won:
                        self.level += 10
                        self.win_time = pg.time.get_ticks()
                        self.level_won = True
                        pg.mixer.music.stop()
                        self.effects_sounds['levelup'].play()
                        if self.level > 100:
                            if not self.won:
                                self.won = True
                                self.end_screen()
                        else:
                            self.new_level()
    
    def draw(self):
        #game loop - draw
        self.screen.blit(self.background_img, (0, 0))
        self.all_sprites.draw(self.screen)
        self.slimes.draw(self.screen)
        self.powerups.draw(self.screen)
        self.beakers.draw(self.screen)
        self.giant_slimes.draw(self.screen)
        self.players.draw(self.screen)
        self.score_bar_bg = pg.Surface((WIDTH, TILE_SIZE))
        self.score_bar_bg.fill(BLACK)
        self.screen.blit(self.score_bar_bg, (0, HEIGHT - TILE_SIZE))
        self.draw_text("Level: " + str(self.level), 22, WHITE, 70, HEIGHT - TILE_SIZE + 3)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT - TILE_SIZE + 3)
        self.draw_text("Messes: " + str(len(self.messes)), 22, WHITE, WIDTH - 80, HEIGHT - TILE_SIZE + 3)
        pg.display.flip()

    def show_start_screen(self):
        song = self.music_list[2]
        pg.mixer.music.load(song)
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.title_image, (int(WIDTH/2 - self.twidth/2), 0))
        if self.num_joysticks == 0:
            self.draw_text("Press a button to play", 15, WHITE, WIDTH/2, HEIGHT - 30)
        elif self.num_joysticks == 1:
            self.draw_text("Press A for 1P", 15, WHITE, WIDTH / 2, HEIGHT - 40)
            self.draw_text("Press X for 2P+ Keyboard", 15, WHITE, WIDTH / 2, HEIGHT - 20)
        elif self.num_joysticks > 1:
            self.draw_text("Press A for 1 player", 15, WHITE, WIDTH / 2, HEIGHT - 50)
            self.draw_text("Press B for 2+ players", 15, WHITE, WIDTH / 2, HEIGHT - 32)
            self.draw_text("Press X for 2P+ Keyboard", 15, WHITE, WIDTH / 2, HEIGHT - 15)
        pg.display.flip()
        self.wait_for_key()
        

    def show_go_screen(self):
        self.channel6.stop()
        pg.mixer.music.load(self.lose_music)
        pg.mixer.music.play(loops=-1)
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 60, RED, WIDTH/2, HEIGHT/4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a button to play again", 22, WHITE, WIDTH/2, HEIGHT*3/4)
        pg.display.flip()
        self.princess.kill()
        for player in self.players:
            player.kill()
        for wall in self.walls:
            wall.kill()
        for mess in self.messes:
            mess.kill()
        for giant_slime in self.giant_slimes:
            giant_slime.kill()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = waiting = False
                if event.type == pg.JOYBUTTONDOWN:
                    if event.button in [0, 1, 2, 3, 6, 7, 9]:
                        if not self.num_players_selected:
                            if event.button == 0:
                                self.num_players_selected = True
                                self.num_joysticks = 1
                                self.mouse_player = False
                            elif event.button == 1:
                                self.num_players_selected = True
                                self.num_joysticks = len(self.joysticks)
                                self.mouse_player = False
                            elif event.button == 2:
                                self.num_players_selected = True
                                self.num_joysticks = len(self.joysticks)
                                print(self.num_joysticks)
                                self.mouse_player = True
                        waiting = False
                    elif event.button in [8, 10]:
                        self.running = waiting = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.num_joysticks == 0:
                        waiting = False
                elif event.type == pg.KEYDOWN:
                    if self.num_joysticks == 0:
                        waiting = False

    def draw_text(self, text, size, color, x, y, align = 'midtop'):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == 'midtop':
            text_rect.midtop = (x, y)
        if align == 'midleft':
            text_rect.midleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def end_screen(self):
        self.channel6.stop()
        pg.mixer.music.load(self.end_music)
        pg.mixer.music.play(loops=-1)
        if not self.running:
            return
        part1 = True
        part2 = True
        for player in self.players:
            player.kill()
        for wall in self.walls:
            wall.kill()
        for mess in self.messes:
            mess.kill()
        for giant_slime in self.giant_slimes:
            giant_slime.kill()
        self.princess.kill()
        self.princess = Princess(self, WIDTH / 2 - TILE_SIZE/2, 64)
        start_end = pg.time.get_ticks()
        while part1:
            now = pg.time.get_ticks()
            if now - start_end > 5000:
                part1 = False
            self.screen.fill(BLACK)
            self.draw_text('"My hero! You saved my kingdom from the mess!"', 15, YELLOW, WIDTH / 2, 45)
            self.draw_text("Congratulations", 40, BLUE, WIDTH/2, HEIGHT/4)
            self.draw_text("you won!", 40, BLUE, WIDTH / 2, HEIGHT / 4 + 50)
            self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/2)
            self.princess.update()
            self.all_sprites.draw(self.screen)
            pg.display.flip()

            for event in pg.event.get():
                # check for closing window
                if event.type == pg.QUIT:
                    self.running = part1 = part2 = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    part1 = False
                if event.type == pg.KEYDOWN:
                    part1 = False

        yscroll = 0
        space = 30
        indent = 10
        font_size = 18
        small_font_size = 12
        while part2:
            self.screen.fill(BLACK)
            self.draw_text('Credits:', 40, WHITE, WIDTH / 2,  HEIGHT - yscroll + space)
            self.draw_text("Executive Game Designer:   Raven Ironwing", font_size, WHITE, indent, HEIGHT - yscroll + 4*space, 'midleft')
            self.draw_text("Assistant Game Designer:   JED", font_size, WHITE, indent, HEIGHT - yscroll + 5*space, 'midleft')
            self.draw_text("Lead Programmer:   Raven Ironwing", font_size, WHITE, indent, HEIGHT - yscroll + 6*space, 'midleft')
            self.draw_text("Graphic Designers:   JED & Raven Ironwing", font_size, WHITE, indent, HEIGHT - yscroll + 7*space, 'midleft')
            self.draw_text("Special thanks to the folks at OpenGameArt.org:", font_size, WHITE, WIDTH/2, HEIGHT - yscroll + 10*space)
            self.draw_text("Level Music:   Snabisch, Clement Panchout, Hitctrl, BBandRage", small_font_size, WHITE, indent, HEIGHT - yscroll + 12* space, 'midleft')
            self.draw_text("Boss Music:   Locomule", small_font_size, WHITE, indent, HEIGHT - yscroll + 13 * space, 'midleft')
            self.draw_text("Game Over Music:   remaxim", small_font_size, WHITE, indent, HEIGHT - yscroll + 14 * space, 'midleft')
            self.draw_text("End Credits Music:   CleytonKauffman", small_font_size, WHITE, indent, HEIGHT - yscroll + 15 * space, 'midleft')
            self.draw_text("Sound Effects:   Raven D., Dizzy Crow, Independent.nu, qubodup, Mike Koenig", small_font_size, WHITE, indent, HEIGHT - yscroll + 16 * space, 'midleft')
            self.draw_text("Princess and small slimes adapted by Raven from art by GrafxKid", small_font_size, WHITE, indent, HEIGHT - yscroll + 17 * space, 'midleft')
            self.draw_text("Skeleton princess adapted by Raven from art by GrafxKid & AntumDeluge", small_font_size, WHITE, indent, HEIGHT - yscroll + 18 * space, 'midleft')
            self.draw_text("Bomb art adapted by Raven from art by Znevs", small_font_size, WHITE, indent, HEIGHT - yscroll + 19 * space, 'midleft')
            self.draw_text("Beakers art adapted by Raven from art by Cliipso", small_font_size, WHITE, indent, HEIGHT - yscroll + 20 * space, 'midleft')
            self.draw_text("Explosion animation from KidsCanCode.org", small_font_size, WHITE, indent, HEIGHT - yscroll + 21 * space, 'midleft')

            self.draw_text("Inspired by the original 1980s ASCII-based Mop of the Mess", font_size, WHITE, WIDTH/2, HEIGHT - yscroll + 24 * space)
            self.draw_text("by Joseph Dewey", font_size, WHITE, WIDTH/2, HEIGHT - yscroll + 25 * space)

            self.draw_text("Mutant Python Games™", 22, GREEN, WIDTH/2, HEIGHT - yscroll + 30 * space)
            self.screen.blit(self.logo_image, (WIDTH/2 - 64, HEIGHT - yscroll + 31*space))
            self.screen.blit(self.title_image, (int(WIDTH / 2 - self.twidth / 2), HEIGHT - yscroll + 57 * space))
            yscroll +=0.5
            pg.display.flip()
            if (HEIGHT - yscroll + 57 * space) <= 0: # Stops scrolling and ends credit scene.
                part2 = False

            for event in pg.event.get():
                # check for closing window
                if event.type == pg.QUIT:
                    self.running = part2 = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    part2 = False
                if event.type == pg.KEYDOWN:
                    part2 = False


g = Game()
while g.running:
    g.show_start_screen()
    if g.running:
        g.new()
        if not g.won:
            g.show_go_screen()
pg.quit()

    
