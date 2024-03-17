import pygame,sys
from scripts.utils import load_images, load_image
from scripts.tilemap import Tilemap

RENDER_SCALE = 4.0 #multiplier for pixel

path = 'data/maps/0.json'

class Editor:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        pygame.display.set_caption("Editor")
        
        self.keyboard = True

        self.font_size = 10
        self.font = pygame.font.SysFont("Futura", self.font_size)

        self.screen = pygame.display.set_mode((1280, 960))
        #so now with the line below you can use display instead of screen too
        self.display = pygame.Surface((320,240)) # .surface() makes new black surface like window(like just a black img)

        self.clock = pygame.time.Clock()

        self.joysticks = []
        
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'spawners' : load_images('tiles/spawners'),
            'cloth': load_images('tiles/spawners/'),
            'grass1': load_images('tiles/decor/'),
        }

        self.movement = [False,False, False, False] # for camera (4 directions)

        self.tilemap = Tilemap(self, tile_size = 16)

        try:
            self.tilemap.load(path)
        except FileNotFoundError:
            pass

        self.scroll = [0,0]

        self.tile_list = list(self.assets) #using list function gives a list of just the keys
        self.tile_group = 0
        self.tile_variant = 0
        
        self.clicking = False
        self.right_clicking = False

        self.shift = False
        
        self.joystickIndex1 = 0
        self.joystickIndex2 = 0
        self.joystickIndex3 = 0
        self.joystickIndex4 = 0
        self.joystickIndex5 = 0

        self.jCursorX = 640
        self.jCursorY = 480

        self.ongrid = True


    def draw_text(self, text, font, text_col, x, y):
        img = self.font.render(text, True, text_col, )
        self.display.blit(img, (x, y))

    def run(self):
        while True:
            self.display.fill((0,0,0))

            #camera movement
            self.scroll[0] += (self.movement[1] - self.movement[0])*2
            self.scroll[1] += (self.movement[3] - self.movement[2])*2
            #
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset = render_scroll, editor=True)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100) #adding transparency

            #mouse position
            if self.keyboard:
                mpos = pygame.mouse.get_pos()
                mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE) # to match scale we do at the end of this function
                tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

                if self.ongrid:
                    self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1])) # showing where the next tile will be, this is convwerting the tilee_pos which was the tile location into pixels again. and we are not using previous mouse position because we want it being alighned in grid
                else:
                    self.display.blit(current_tile_img, mpos)

                if self.clicking and self.ongrid:
                    self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant' : self.tile_variant, 'pos': tile_pos}
                if self.right_clicking:
                    tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1]) # taking position of tile that cursor is on
                    if tile_loc in self.tilemap.tilemap: # checking if the tile location includes a tile
                        del self.tilemap.tilemap[tile_loc] # if yes it removes the tile from the dict so we don't see it
                    for tile in self.tilemap.offgrid_tiles.copy(): #making copy because if it is touching our cursor it will delete
                        tile_img = self.assets[tile['type']][tile['variant']]
                        tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height()) # geting hitbox of item because things like trees will take more space
                        if tile_r.collidepoint(mpos): #checks collisions with points instead of rects
                            self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5,5))

            #show number of connected joysticks
            if self.keyboard == False:
                for joystick in self.joysticks:
                    proportionedX, proportionedY = self.jCursorX/RENDER_SCALE, self.jCursorY/RENDER_SCALE
                    joyPos = (proportionedX, proportionedY)
                    self.draw_text("Controller ON", self.font, pygame.Color("azure"), 10, 10)
                    pygame.draw.circle(self.display, (255,255,255), joyPos, 2)
                    if self.ongrid:
                        tile_pos = (int((joyPos[0] + self.scroll[0]) // self.tilemap.tile_size), int((joyPos[1] + self.scroll[1]) // self.tilemap.tile_size))
                        self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
                        # print('ongrid')
                    else:
                        self.display.blit(current_tile_img, joyPos)

                    if joystick.get_button(4):
                        self.joystickIndex1 += 1
                        if self.joystickIndex1 >= 7:
                            if self.shift:
                                self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                            else:
                                self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                                self.tile_variant = 0
                            self.joystickIndex1 = 0
                    if joystick.get_button(5):
                        self.joystickIndex2 += 1
                        if self.joystickIndex2 >= 7:
                            if self.shift:
                                self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                            else:
                                self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                                self.tile_variant = 0
                            self.joystickIndex2 = 0
                    if joystick.get_button(3):
                        self.tilemap.autotile()
                    if joystick.get_button(1):
                        self.tilemap.save(path)
                    if joystick.get_button(2):
                        self.joystickIndex3 += 1
                        if self.joystickIndex3 >= 5:
                            self.shift = not self.shift
                            self.joystickIndex3 = 0
                    if joystick.get_button(0):
                        self.joystickIndex4 += 1
                        if self.joystickIndex4 >= 5:
                            self.ongrid = not self.ongrid
                            self.joystickIndex4 = 0
                    horiz_move = joystick.get_axis(0)
                    vertic_move = joystick.get_axis(1)
                    rTrigger = joystick.get_axis(5)
                    lTrigger = joystick.get_axis(2)
                    rhor_move = joystick.get_axis(3)
                    rver_move = joystick.get_axis(4)
                    
                    # print(self.clicking)
                    if rhor_move > 0.2:
                        self.jCursorX += 4
                    elif rhor_move < -0.2:
                        self.jCursorX -= 4
                    else:
                        pass
                    if rver_move > 0.2:
                        self.jCursorY += 4
                    elif rver_move < -0.2:
                        self.jCursorY -= 4
                    else:
                        pass
                    if rTrigger > 0.65:
                        self.joystickIndex5+=1
                        self.clicking = True
                        tile_pos = (int((joyPos[0] + self.scroll[0]) // self.tilemap.tile_size), int((joyPos[1] + self.scroll[1]) // self.tilemap.tile_size))
                        # print(self.jCursorX, self.jCursorY)
                        if self.joystickIndex5 >=5:
                            if self.ongrid:
                                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant' : self.tile_variant, 'pos': tile_pos}
                            else:
                                self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (joyPos[0] + self.scroll[0], joyPos[1]+ self.scroll[1])})
                            self.joystickIndex5 = 0
                    else:
                        self.clicking = False
                    if lTrigger > 0.65:
                        self.right_clicking = True
                        tile_pos = (int((joyPos[0] + self.scroll[0]) // self.tilemap.tile_size), int((joyPos[1] + self.scroll[1]) // self.tilemap.tile_size))
                        if self.right_clicking:
                            tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1]) # taking position of tile that cursor is on
                            if tile_loc in self.tilemap.tilemap: # checking if the tile location includes a tile
                                del self.tilemap.tilemap[tile_loc] # if yes it removes the tile from the dict so we don't see it
                            for tile in self.tilemap.offgrid_tiles.copy(): #making copy because if it is touching our cursor it will delete
                                tile_img = self.assets[tile['type']][tile['variant']]
                                tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height()) # geting hitbox of item because things like trees will take more space
                                if tile_r.collidepoint(joyPos): #checks collisions with points instead of rects
                                    self.tilemap.offgrid_tiles.remove(tile)
                    else:
                        self.right_clicking = False

                    if horiz_move < -0.2:
                        self.movement[0] = True
                    else:
                        self.movement[0] = False
                    if horiz_move > 0.2:
                        self.movement[1] = True
                    else:
                        self.movement[1] = False
                    
                    if vertic_move < -0.2:
                        self.movement[2] = True
                    else:
                        self.movement[2] = False
                    if vertic_move > 0.2:
                        self.movement[3] = True
                    else:
                        self.movement[3] = False
            else:
                # self.draw_text("Controller OFF", self.font, pygame.Color("azure"), 10, 10)
                pass

            for event in pygame.event.get():
                if event.type == pygame.JOYDEVICEADDED:
                    self.joy = pygame.joystick.Joystick(event.device_index)
                    self.joysticks.append(self.joy)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.keyboard:
                    if event.button == 1: #left click
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1]+ self.scroll[1])}) #putting the the tile in offgrid dict so we can display it when we have turned ongrid off
                    if event.button == 3: # right click
                        self.right_clicking = True

                    if self.shift:
                        if event.button == 4: #scroll down
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]]) #using modulo to loop the types, and we want to loop in self.tile_list
                        if event.button == 5: #scroll up
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4: #scroll down
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list) #using modulo to loop the types, and we want to loop in self.tile_list
                            self.tile_variant = 0
                        if event.button == 5: #scroll up
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP and self.keyboard:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN and self.keyboard:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid #switches values like true to false or other way
                    if event.key == pygame.K_LSHIFT:
                        self.shift = not self.shift
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        self.keyboard = not self.keyboard
                    if event.key == pygame.K_o:
                        self.tilemap.save(path)
                if event.type == pygame.KEYUP and self.keyboard:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0)) # displaying the surface which you put everything on, onto the original screen and scaling the surface to the scrren's size
            pygame.display.update()
            self.clock.tick(60)

Editor().run()