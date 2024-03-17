import pygame, math, random
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.tilemap import Tilemap

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size): # asking for game so we can access the class game through this class too
        self.game = game
        self.type = e_type # entity type
        self.pos = list(pos) #you want to add to list so that we can keep every entity seperatley
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        #animation
        self.action = ''
        self.anim_offset = (-3, -3) # use offset beause a lot of the times the pictures have differnt paddings meaning empty space on the sides
        self.flip = False
        self.set_action('idle')

        self.last_movement = [0,0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action: #only doing the rest if the action changed
            self.action = action
            # i accessed a class property from another file by saying self.fileName (in this case game)
            self.animation = self.game.assets[self.type + '/' + self.action].copy() # making new instances of the animation


    def update(self, tilemap,movement =(0, 0)):

        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False} # resetting collisions every frame

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) # the reason we do this is because we want to add the current velocity of the entity to the new force in movement

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: #if moving right
                    entity_rect.right = rect.left # if collision, the entity's right edge snaps back to the left edge of the tile
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x #moving player's position to it's rect position

        self.pos[1] += frame_movement[1] # should do these in differnt places not in one line
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        #line below adds to velocity if it is less than 5 otherwise no as that is the terminal velocity
        self.velocity[1] = min(5, self.velocity[1]+0.1) # objects have terminal velocity which is the max acceleration it  can have you shouldn't constantly be accelerating when falling down
        # print(self.velocity[1])


        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0 #ressetting the velocity when hitting the ground because otherwise, once hitting ground and then jumping off again you will keep 5 velocity to start with

        self.animation.update()

    def render(self, surf, offset =(0,0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
        # surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class Enemy(PhysicsEntity):
    def __init__(self,  game, pos, size):
        super().__init__(game, 'enemy', pos, size)

        self.walking = 0 # timer like the self.dashing but won't include direction
        self.time = 0

    def update(self, tilemap, movement = (0,0)):
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)): # we use 7 because it is basicly saying that check 7 blocks to the left and right, for y axis we use + 23 to get the bottom of player
                if (self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement [1]) # remove 0.5 if left but add 0.5 if right
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking: # puttin this in the if self.walking if statement because the line above this reduces the the number by one so we will get one frame which will be the one when the enemy stops walking
                # print('stop')
                dist = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1]) # diff between player and enmy pos
                if (abs(dist[1]) < 16):
                    shootStop = False
                    tile_loc = str(int(self.pos[0] // self.game.tilemap.tile_size)) + ';' + str(int(self.pos[1] // self.game.tilemap.tile_size))
                    tile_dist = int(dist[0] // self.game.tilemap.tile_size)
                    if (self.flip and dist[0] < 0): # if player to the left and the self.flip is saying looking left
                        for x in range(abs(tile_dist)):
                            if self.game.tilemap.solid_check((self.pos[0] - (x * self.game.tilemap.tile_size), self.pos[1])):
                                shootStop = True
                        if not shootStop:
                            self.game.sfx['shoot'].play()
                            self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0]) # pos, direction/speed, timer
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dist[0] > 0): # if enemy looks right and we are in the right
                        for x in range(abs(tile_dist)):
                            if self.game.tilemap.solid_check((self.pos[0] + (x * self.game.tilemap.tile_size), self.pos[1])):
                                shootStop = True
                        if not shootStop:
                            self.game.sfx['shoot'].play()
                            self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))
                    
        elif random.random() < 0.01: # this is basicly 1/100 chance but we run at 60fps so it is good
            self.walking = random.randint(30,120) # random # between half sec to 2 sec
            self.time = 0
        else:
            self.time += 1
            if self.time % random.randint(15, 30) == 0 and self.time >= 60: # change the value that is 30 rn to increase probability of enemy shooting, decreasing it increases probability of enemy shooting
                dist = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1]) # diff between player and enmy pos
                if (abs(dist[1]) < 16):
                    shootStop = False
                    tile_loc = str(int(self.pos[0] // self.game.tilemap.tile_size)) + ';' + str(int(self.pos[1] // self.game.tilemap.tile_size))
                    tile_dist = int(dist[0] // self.game.tilemap.tile_size)
                    if (self.flip and dist[0] < 0): # if player to the left and the self.flip is saying looking left
                        for x in range(abs(tile_dist)):
                            if self.game.tilemap.solid_check((self.pos[0] - (x * self.game.tilemap.tile_size), self.pos[1])):
                                shootStop = True
                        if not shootStop:
                            self.game.sfx['shoot'].play()
                            self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0]) # pos, direction/speed, timer
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dist[0] > 0): # if enemy looks right and we are in the right
                        for x in range(abs(tile_dist)):
                            if self.game.tilemap.solid_check((self.pos[0] + (x * self.game.tilemap.tile_size), self.pos[1])):
                                shootStop = True
                        if not shootStop:
                            self.game.sfx['shoot'].play()
                            self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                            for i in range(4):
                                self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))
            if self.time >= 210:
                self.walking = random.randint(30,120)
                self.time = 0
        # print(self.time)
                

        super().update(tilemap, movement= movement)

        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
        
        if abs(self.game.player.dashing) >= 50: # if inframes of dash
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenShake = max(16, self.game.screenShake)
                self.game.sfx['hit'].play()
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity = [math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame = random.randint(0,7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True
    
    def render(self, surf, offset = (0,0)):
        super().render(surf, offset = offset)

        #enemy weapon
        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1])) # remember the offset is the offset of the camera
        else:
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))


class Player(PhysicsEntity): #inheriting from PhysicsEntity
    def __init__(self, game, pos, size): # we are seperating this part from the above class and putting in another because the animation logic is diff from other entities
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0 # stores how much we want to dash and which direction
    
    def update(self, tilemap, movement = (0,0), keyboard = True):
        super().update(tilemap, movement = movement)

        if not self.wall_slide:
            self.air_time += 1
        else:
            if keyboard:
                self.air_time = 5
            else:
                self.air_time = 13

        if self.air_time > 120 and not self.wall_slide:
            if not self.game.dead:
                self.game.screenShake = max(16, self.game.screenShake)
            self.game.dead += 1

        if self.collisions['down']: # if on ground
            self.air_time = 0
            self.jumps = 1

        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and ((self.air_time > 4 and keyboard) or (self.air_time>12 and keyboard == False)): # if in air and touching wall
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5) #maxing out velocity to 0.5 when on wall
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')
        
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump') # if in air for a while show jump animation
            elif movement[0] != 0: #if movement isn't 0 so it is moving horizontally, also we are using elif not if statment again because we are giving priortiy to jump as we don't want run to overwrite jump when in air
                self.set_action('run')
            else:
                self.set_action('idle')
        
        if abs(self.dashing) in {60,50}: # if at start or end of dash (fast part)
            for i in range(20): # making 20 particles
                #trignometry for particles of dashing ( we are trying to have a burst of particles in a circle shape)
                angle = random.random() * math.pi * 2 # taking random angle 
                speed = random.random() * 0.5 + 0.5 # taking random speed
                pveloctiy = [math.cos(angle) * speed, math.sin(angle) * speed] # generating velocity based on angle
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity = pveloctiy, frame = random.randint(0, 7))) # note: self.rect() is a function we made before in the physicsEntity class
                ####
        
        #note the if statement above comes before the one below because in the below we decrease the self.dashing by one so then teh value of we have used above (60) for the start will change to 59 when it reaches the if above and it won't give the start burst
        #you can also for the comment above this, instead of moving above, just decrease both values by 1

        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1) # basically this like used before makes it so that it slows down gradually and makes it to 0 eventually
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8 # if in first 10 frames of dash then making velocity to 8 or -8 because absolute of something divided by itself shows -1 or 1 which tells us the direction
            if abs(self.dashing) == 51: # this also acts as a cooldown because to start self.dashing the value has to be 0 (dash function) so after decreasing teh velocity by a lot then the very little left velocity graudally goes to 0 because of the if statements in the end of this function so once it reaches 0 then you can dash again
                self.velocity[0] *= 0.1 # the end of the first 10 frames of dash, severely cut down velocity
            pveloctiy = [abs(self.dashing)/ self.dashing * random.random() * 3, 0] # taking direction like we did above and taking random number between 0-3 in the correct direction and no movement on y axis
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity = pveloctiy, frame = random.randint(0, 7))) # note: self.rect() is a function we made before in the physicsEntity class

        # ###### This below enables infinite dash (for fun):
        # if self.dashing < 50 and self.dashing > -50:
        #     self.dashing = 0
        ####################################################

        # print(self.velocity[0])

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0) # reduce x velocity with it stopping at 0, we add this normalization for x-axis becasue in wall slide jumping we are forced to move up (see code below)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
        
        # print(self.last_movement)

    
    def render(self, surf, offset =(0,0)):
        if abs(self.dashing) <= 50: # if not in first 10 frames of dash
            super().render(surf, offset = offset) # using the render function of the class physicsentity above this class
            # the reason we are doing this in this class instead of just suing the render function from the class directly is so we can add the condition that we have in this function
            # this makes it so that when in the fast part of the dash or the first 10 frames, the player is invisible!
        
    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0: # we use last movement because we are trying to see if you are pushing against wall, so like even if you are next to a wall in the air are you trying to push and connect to the wall or just fall next to the wall
                self.velocity[0] =3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1) # making sure jumps don't go below 0
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps: # passes if value is 1 (true) and not when 0 (false)
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
            return True
    
    def dash(self):
        if not self.dashing: # if not 0 so if you are dashing
            self.game.sfx['dash'].play()
            if self.flip: # if facing left
                self.dashing = -60
            else:
                self.dashing = 60


#all you have to do to add more entity animations is to make another class like Player and change the stage logic like when is what stage
