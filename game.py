import pygame
import sys, time
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
import scripts.cloth as cloth1
import random, math, os
import scripts.grass as grass
from scripts.button import Button
from scripts.drop_down import DropDown

class Game:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        pygame.display.set_caption("Platformer")
        
        self.keyboard = True

        self.font_size = 10
        self.font = pygame.font.SysFont("Futura", self.font_size)

        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screenX = 1920
        self.screenY = 1380
        self.screen = pygame.display.set_mode((self.screenX, self.screenY)) # Keep proportion of sizes. Examples: (1280, 960), (640, 480), (1920, 1380)
        self.fullScreen = False
        #so now with the line below you can use display instead of screen too
        self.display = pygame.Surface((320,240), pygame.SRCALPHA) # .surface() makes new black surface like window(like just a black img), scralpha tells the surface to add a transparency channel so it can be transparent
        self.display2 = pygame.Surface((320,240))
         # display will be the one where we put outlines, so if you want ooutlines on something blit it in display if not then blit it in display2

        self.clock = pygame.time.Clock()

        self.joysticks = []

        # self.img = pygame.image.load("data/images/clouds/cloud_1.png")
        # self.img.set_colorkey((0,0,0)) #takes wherever the color is in the pic and makes it transparent

        # self.img_pos = [160,260]
        self.movement = [False,False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur = 6),
            'player/run': Animation(load_images('entities/player/run'), img_dur = 4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf', scaleFactor=1.5), img_dur=20, loop = False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop = False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }

        self.sfx = {
            'jump' : pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash' : pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit' : pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot' : pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience' : pygame.mixer.Sound('data/sfx/ambience.wav'),
        }

        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)

        self.clouds = Clouds(self.assets['clouds'], count = 16)

        # self.collision_area = pygame.Rect(50,50,300, 50)
        
        self.player = Player(self, (50,50), (8,15))

        self.tilemap = Tilemap(self, tile_size = 16)

        self.level = 0
        self.load_map(self.level)

        self.screenShake = 0

        #buttons
        self.button1 = Button('Game',70,25,(10,20),5, self.font, self.display, self)
        self.button2 = Button('Options',70,25,(10,55),5, self.font, self.display, self)
        self.button3 = Button('Resolution',70,25,(10,20),5, self.font, self.display, self)
        self.button4 = Button('Controls',70,25,(10,45),5, self.font, self.display, self)
        COLOR_INACTIVE = "#475F77"
        COLOR_ACTIVE = "#D74B4B"
        COLOR_LIST_INACTIVE = "#354B5E"
        COLOR_LIST_ACTIVE = "#D74B4B"
        self.list1 = DropDown(
            [COLOR_INACTIVE, COLOR_ACTIVE],
            [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
            10, 10, 70, 25, 
            self.font, 
            "1920x1380", ["1920x1380", "1280x960", "640x480"], self)
        


    def draw_text(self, text, font, text_col, x, y):
        img = self.font.render(text, True, text_col)
        self.display.blit(img, (x, y))

    def load_map(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep = True):
            self.leaf_spawners.append(pygame.Rect(4+tree['pos'][0], 4+ tree['pos'][1], 23, 13)) #making a hitbox of the trees
        # print(self.leaf_spawners)
            
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8,15)))
        
        self.projectiles = []
        self.particles = []
        self.sparks = []
        self.cloths = []
        self.wind = 0
        self.cloth_timer = 0
        self.wind_grad = random.randint(-5,5)/100
        self.changed = False

        self.scroll = [0,0]
        self.dead = 0
        self.transition = -90
        self.tilemap.load_cloths()
        self.grass_tile_size = 16
        self.gm = grass.GrassManager('data/images/grass', tile_size=self.grass_tile_size, stiffness=600, max_unique=5, place_range=[1, 1])
        # self.gm.enable_ground_shadows(shadow_radius=4, shadow_color=(0, 0, 1), shadow_shift=(1, 2))
        self.t = 0
        self.start = time.time()
        self.brush_size = 5
    
    def main_menu(self):
        while True:

            self.display.fill((0,0,0))
            self.button1.draw("game")
            self.button2.draw("option")
            # self.draw_text('main menu', self.font, (255, 255, 255), 20, 20)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_f:
                        self.fullScreen = not self.fullScreen
                        if self.fullScreen:
                            self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                            self.list1.main = "FullScreen"
                        else:
                            self.screen = pygame.display.set_mode((self.screenX, self.screenY))
                            self.list1.main = str(self.screenX) + "x" + str(self.screenY)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True


            self.display2.blit(self.display, (0,0)) # comment this for ninja mode :)
            screenShakeOffset = (random.random() * self.screenShake - self.screenShake*2, random.random() * self.screenShake - self.screenShake*2)
            self.screen.blit(pygame.transform.scale(self.display2, self.screen.get_size()), screenShakeOffset) # displaying the surface which you put everything on, onto the original screen and scaling the surface to the scrren's size
            pygame.display.update()
            self.clock.tick(60)

    def options(self):
        self.running = True
        while self.running:
            self.display.fill((0,0,0))
            # self.button3.draw("resolution", [self.list1])
            self.button4.draw("controls", [self.list1])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_f:
                        self.fullScreen = not self.fullScreen
                        if self.fullScreen:
                            self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                            self.list1.main = "FullScreen"
                        else:
                            self.screen = pygame.display.set_mode((self.screenX, self.screenY))
                            self.list1.main = str(self.screenX) + "x" + str(self.screenY)

                selectedOption = self.list1.update(event, (self.screenX, self.screenY))
                if selectedOption >= 0:
                    self.list1.main = self.list1.options[selectedOption]
                    if self.list1.options[selectedOption] == "1280x960": # (320,240)
                        self.screenX, self.screenY = 1280, 960
                        self.screen = pygame.display.set_mode((self.screenX, self.screenY))
                        self.fullScreen = False
                    elif self.list1.options[selectedOption] == "1920x1380":
                        self.screenX, self.screenY = 1920, 1380
                        self.screen = pygame.display.set_mode((self.screenX, self.screenY))
                        self.fullScreen = False
                    elif self.list1.options[selectedOption] == "640x480":
                        self.screenX, self.screenY = 640, 480
                        self.screen = pygame.display.set_mode((self.screenX, self.screenY))
                        self.fullScreen = False
                
            # print(eventList)
            # selectedOption = self.list1.update(eventList)
            
            self.list1.draw(self.display)

            self.display2.blit(self.display, (0,0)) # comment this for ninja mode :)
            screenShakeOffset = (random.random() * self.screenShake - self.screenShake*2, random.random() * self.screenShake - self.screenShake*2)
            self.screen.blit(pygame.transform.scale(self.display2, self.screen.get_size()), screenShakeOffset) # displaying the surface which you put everything on, onto the original screen and scaling the surface to the scrren's size
            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        self.running = True
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)# parameter is how many loops you want, -1 is forever

        self.sfx['ambience'].play(-1)

        while self.running:
            self.dt = time.time() - self.start
            self.start = time.time()
            self.display.fill((0,0,0, 0))
            self.display2.blit(self.assets['background'], (0,0))

            self.screenShake = max(0, self.screenShake - 1)
            
            if self.cloth_timer < 180:
                self.cloth_timer+=1
            elif not self.changed and self.cloth_timer == 180:
                self.wind_grad = random.randint(-5,5)/100
                self.changed = True
                # print('changed')
            # print(self.changed, self.cloth_timer)
            # print(round(self.wind, 2), self.wind_grad)
            # self.cloths = []
            if round(self.wind, 2) != self.wind_grad:
                if self.wind < self.wind_grad:
                    self.wind +=0.001
                else:
                    self.wind-=0.001
            elif round(self.wind, 2) == self.wind_grad and self.changed == True:
                self.cloth_timer = 0
                self.changed = False
            # print(self.wind)

            if not len(self.enemies): # if killed all enemies
                self.transition += 1
                if self.transition > 90:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_map(self.level)
            if self.transition < 0:
                self.transition += 1

            if self.dead:
                self.dead += 1
                if self.dead >= 0:
                    self.transition = min(90, self.transition + 1)
                if self.dead > 40:
                    self.load_map(self.level)
            
            #line below basicly checks how far away the camera is from what we want it to be and adds it to scroll
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0])/30 # normally if you put camera on player pos then player will be on top left but want it in the middle
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1])/30
            #in the lines above the /30 makes it so that the further the player goes the higher speed of camera and then it slows down as the player stops
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) # need to convert scroll to int because it is float currently and with those values the screen jitters a lot as they are decimal values

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height: # this basicly makes trees spawn properotional so if it is a bigger tree it will spawn more leaves, also 49999 is there so that leaves spawner rate is slower instead of 100 % of the time (every frame)
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height) # this takes a random position in the tree's rect
                    self.particles.append(Particle(self, 'leaf', pos, velocity = [-0.1-(self.wind*30), 0.3], frame = random.randint(0, 20)))

            self.clouds.update() #move clouds
            self.clouds.render(self.display, offset = render_scroll)  # display in display2 to remove its outlines and shadows

            self.tilemap.render_cloths(self.display, self.wind, offset= render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)

            self.tilemap.render_grass(self.display, self.dt, self.t, render_scroll, gm= self.gm)
            
            self.gm.apply_force((self.player.pos[0], self.player.pos[1]), 5, 25)

            self.t += self.dt * 100

            # self.cloths.append([cloth1.ClothObj(cloth1.load_rags('data/rags')['vine']), (random.randint(0,15)*16 - render_scroll[0], random.randint(0,10)*16 - render_scroll[1])])

            # self.my_cloth.move_grounded([21*16,10*16])
            # self.my_cloth.update(-self.wind)
            # self.my_cloth.update_sticks()
            # self.my_cloth.render_polygon(self.display, (255, 255, 255), offset=render_scroll)

            for enemy in self.enemies.copy(): # use copy because we will remove them later
                kill = enemy.update(self.tilemap, (0,0))
                enemy.render(self.display, offset = render_scroll)
                self.gm.apply_force((enemy.pos[0], enemy.pos[1]), 5, 25)
                if kill:
                    self.enemies.remove(enemy)

            if not self.dead:
                self.player.update(self.tilemap, ((self.movement[1]- self.movement[0]), 0), self.keyboard) # movement left/right, no y axis   
                self.player.render(self.display, offset = render_scroll)
            
            # [(x, y), direction, timer]
            for projectile in self.projectiles.copy(): # use copy because we will remove them later
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360: # if timer is geeater that 360 or 6 sec
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50: # if not in the fast part of the dash. This makes player invincible during dash
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.sfx['hit'].play()
                        self.screenShake = max(16, self.screenShake)
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity = [math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame = random.randint(0,7)))

            self.draw_text("FPS: " + str(round(self.clock.get_fps(), 2)), self.font, pygame.Color("azure"), 10, 20)

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset = render_scroll)
                if kill:
                    self.sparks.remove(spark)
            
            display_mask = pygame.mask.from_surface(self.display) # making mask from display
            display_sillhouette = display_mask.to_surface(setcolor = (0,0,0,180), unsetcolor=(0,0,0,0))  # set color will be the color of outlines
            #shadow
            self.display2.blit(display_sillhouette, (4,4))
            #ninja mode :) (you also need to remove the blitting of display on display2 at the bottom of this file
            # self.display2.blit(display_sillhouette, (0,0))
            #outlines: rendering the mask 4 times in all directions/offsets so it is all around all objects
            for offset in [(-1, 0), (1,0), (0, -1), (0, 1)]:
                self.display2.blit(display_sillhouette, offset)

            for particle in self.particles.copy():
                kill = particle.update()
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3 # just a math formula to add back and forth motion to the animation
                particle.render(self.display, offset = render_scroll)
                if kill:
                    self.particles.remove(particle)

            #show number of connected joysticks
            # self.draw_text("Controllers: " + str(pygame.joystick.get_count()), self.font, pygame.Color("azure"), 10, 35)
            if self.keyboard == False:
                for joystick in self.joysticks:
                    # self.draw_text("Battery Level: " + str(joystick.get_power_level()), self.font, pygame.Color("azure"), 10, 10)
                    self.draw_text("Controller ON", self.font, pygame.Color("azure"), 10, 10)
                    # self.draw_text("Controller Type: " + str(joystick.get_name()), self.font, pygame.Color("azure"), 10, 60)
                    # self.draw_text("Number of axes: " + str(joystick.get_numaxes()), self.font, pygame.Color("azure"), 10, 85)
                    

                    if joystick.get_button(0):
                        if self.player.jump():
                            self.sfx['jump'].play()
                    if joystick.get_button(2):
                        self.player.dash()
                    
                    horiz_move = joystick.get_axis(0)
                    
                    if horiz_move < -0.2:
                        self.movement[0] = True
                    else:
                        self.movement[0] = False
                    if horiz_move > 0.2:
                        self.movement[1] = True
                    else:
                        self. movement[1] = False
                    # print(horiz_move)
            else:
                self.draw_text("Controller OFF", self.font, pygame.Color("azure"), 10, 10)

            # print(self.tilemap.physics_rects_around(self.player.pos))

            # img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height()) # the rect that follows the cloud img
            # # this is a shortcut for the above: pygame.Rect(*self.img_pos, *self.img.get_size())
            # if img_r.colliderect(self.collision_area): #basicly if 2 rects are overlapping
            #     pygame.draw.rect(self.screen, (0,100,255), self.collision_area)
            # else:
            #     pygame.draw.rect(self.screen, (0,50,155), self.collision_area)
            
            # self.img_pos[1] += (self.movement[1] - self.movement[0])*3  # if bool is true it gives 1 otherwise 0
            # self.screen.blit(self.img, self.img_pos)

            for event in pygame.event.get():
                if event.type == pygame.JOYDEVICEADDED:
                    self.joy = pygame.joystick.Joystick(event.device_index)
                    self.joysticks.append(self.joy)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and self.keyboard:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        if self.player.jump():
                            self.sfx['jump'].play()
                    if event.key == pygame.K_x:
                        self.player.dash()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        if self.keyboard:
                            self.keyboard = False
                        else:
                            self.keyboard = True
                    if event.key == pygame.K_f:
                        self.fullScreen = not self.fullScreen
                        if self.fullScreen:
                            self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                            self.list1.main = "FullScreen"
                        else:
                            self.screen = pygame.display.set_mode((self.screenX, self.screenY))
                            self.list1.main = str(self.screenX) + "x" + str(self.screenY)
                if event.type == pygame.KEYUP and self.keyboard:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            
            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255,255,255), (self.display.get_width()//2, self.display.get_height()//2), (30 - abs(self.transition)) * 8) # changin the value (30) will change speed of transition
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0,0))
                self.draw_text("Loading...", self.font, pygame.Color('azure'), 20, 200)
            
            self.display2.blit(self.display, (0,0)) # comment this for ninja mode :)

            screenShakeOffset = (random.random() * self.screenShake - self.screenShake*2, random.random() * self.screenShake - self.screenShake*2)
            self.screen.blit(pygame.transform.scale(self.display2, self.screen.get_size()), screenShakeOffset) # displaying the surface which you put everything on, onto the original screen and scaling the surface to the scrren's size
            pygame.display.update()
            self.clock.tick(60)

Game().main_menu()