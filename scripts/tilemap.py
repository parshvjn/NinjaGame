import pygame, json, math, random
import scripts.cloth as cloth
from scripts.extras import palette_swap

AUTOTILE_MAP = { # rules of the autotiling
    tuple(sorted([(1,0), (0,1)])) : 0, #this says if neighbors are on the left and bottom meaning blocks below or on the left of hte placed tile then change the variant to 0. we make it sorted so that the order is always right, otherwise sometimes the order is different and it won't count as a case. we use tuple becasue we can't hold lists as keys in dicts
    tuple(sorted([(1,0), (0,1), (-1, 0)])) : 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
    tuple(sorted([(-1,0)])) : 2,
    tuple(sorted([(-1,0), (1,0)])) : 1,
}

NEIGHBOR_OFFSETS = [(-1,0), (-1,-1), (0, -1), (1,-1), (1,0), (0,0), (-1, 1), (0,1), (1,1)]
PHYSICS_TILES = {'grass', 'stone'} #using set is more efficient than list
AUTOTILE_TYPES = {'grass', 'stone'} # tiles we want to autotile( meaning they will change variant depending on their surroundings)

class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} # all tiles in a square grid(using dict not list because in a list grid we normally have to fill in air or like very single place but in a dict you can just write the pos: item)
        self.offgrid_tiles = [] # things we place everywhere which might not align with grid
    
    #this function below extracts and returns all instances of a  specific type and variant of a tile(s). and if you put keep= false it will remove all the instances from the tilemap but if not then it keeps it
    def extract(self, id_pairs, keep = False): # id pairs are tile type and variant
        matches = []
        for tile in self.offgrid_tiles.copy(): #making copy becasue we might delete if we aren't keeping (parameter in function)
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy() #making new instance of tile
                #changing position because we want in pixel but the tilemap is in grid
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        return matches

    def tiles_around(self, pos): #just checking neighboring tiles for collisions with player because why would we need to check every tile
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)) # convert pixel position to grid position
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0]+offset[0]) + ';' + str(tile_loc[1]+offset[1])
            if check_loc in self.tilemap: # checking if there is a surface collision and not just air around player
                tiles.append(self.tilemap[check_loc])
        return tiles #return all tiles around player (not air)

    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f) #dump object in the file and converting in json
        f.close()
    
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
    
    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size)) # getting tile location
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES: #check if the tiles around it are the part of the ones we want collisions with
                rects.append(pygame.Rect(tile['pos'][0]*self.tile_size, tile['pos'][1]*self.tile_size, self.tile_size, self.tile_size))
        return rects

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1,0), (-1, 0), (0, -1), (0, 1)]: # these are the offsets like checking block below/above/right/ etc..
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1]) # this  gets the current tile and checks the tiles around it using the offsets, like checking the block above or below, etc..
                if check_loc in self.tilemap: # if tile in that offset
                    if self.tilemap[check_loc]['type'] == tile['type']: # if the block on the offset is the same type of block as you are placing next to it
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors)) # making it as the same order we put in the autotile rules
            if (tile['type'] in AUTOTILE_TYPES and (neighbors in AUTOTILE_MAP)):
                tile['variant'] = AUTOTILE_MAP[neighbors]
    
    def load_cloths(self):
        for tile in self.offgrid_tiles:
            if tile['type'] == 'cloth':
                self.game.cloths.append([cloth.ClothObj(cloth.load_rags('data/rags')['vine']), (tile['pos'][0], tile['pos'][1])])
        # print(self.game.cloths)
    
    def render_grass(self, surf, dt, t, offset, gm):
        for tile in self.offgrid_tiles:
            if tile['type'] == 'grass1':
                rot_function = lambda x, y: int(math.sin(t / 60 + x / 100) * 15)
                gm.update_render(surf, dt, offset=offset, rot_function=rot_function)
                gm.place_tile((((tile['pos'][0]) // gm.tile_size), ((tile['pos'][1]) // gm.tile_size)), int(random.random() * 12 * self.game.brush_size + 1), [self.game.brush_size])

    def render_cloths(self, surf, wind, offset = (0,0)):
            for cloth in self.game.cloths:
                # print(cloth[1][0], cloth[1][1])
                cloth[0].move_grounded([cloth[1][0], cloth[1][1]])
                cloth[0].update(-wind)
                cloth[0].update_sticks()
                cloth[0].render_polygon(surf, (0,164,120), offset)


    def render(self, surf, offset=(0,0), editor = False):
        if self.game.color =="Normal":
            for tile in self.offgrid_tiles:
                # if tile
                if tile['type'] == 'cloth' or tile['type'] == 'grass1':
                    if editor:
                        surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
                    else:
                        pass
                else:
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1])) # we subtract positions by offset because we are trying to make a camera following the player but instead we move all objects to show the illusion. we use subtraction not addition because if you move right everything  moves left not right

            for x in range(offset[0] // self.tile_size, (offset[0]+ surf.get_width()) // self.tile_size + 1): #first paramter of range has the value of the x position of the top left tile in the screen, 2nd one is the right edge of screen
                for y in range(offset[1] // self.tile_size, (offset[1]+ surf.get_height()) // self.tile_size + 1): #basicly these 2 lines are checking all tiles that we can see on the screen at the time
                    loc = str(x) + ';' + str(y) #getting the value of tile
                    if loc in self.tilemap: # check if tile value/pos in dict 
                        tile = self.tilemap[loc] # getting all data for the tile like ex. if it is grass or what and more.
                        surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]*self.tile_size - offset[0], tile['pos'][1]*self.tile_size - offset[1])) #rendering the tile
                        #so the tiles only show if they are on the screen instead of always loading every tile in the world for optimization
                        
        elif self.game.color == "Color1":
            for tile in self.offgrid_tiles:
                if tile['type'] == 'cloth' or tile['type'] == 'grass1':
                    if editor:
                        surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
                    else:
                        pass
                else:
                    if tile['type'] == 'large_decor' and tile['variant'] == 2:
                        surf.blit(palette_swap(surf, (135,77,62), (17, 11, 96), self.game.assets[tile['type']][tile['variant']]), (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
                    else:
                        surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1])) 

            for x in range(offset[0] // self.tile_size, (offset[0]+ surf.get_width()) // self.tile_size + 1): 
                for y in range(offset[1] // self.tile_size, (offset[1]+ surf.get_height()) // self.tile_size + 1):
                    loc = str(x) + ';' + str(y) 
                    if loc in self.tilemap: 
                        tile = self.tilemap[loc]
                        surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]*self.tile_size - offset[0], tile['pos'][1]*self.tile_size - offset[1])) #rendering the tile

        # for loc in self.tilemap:
            # tile = self.tilemap[loc]
            # surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]*self.tile_size - offset[0], tile['pos'][1]*self.tile_size - offset[1]))