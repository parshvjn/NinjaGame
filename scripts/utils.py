import pygame, os

BASE_IMG_PATH = 'data/images/'

def load_image(path, scaleFactor = 1):
    img = pygame.image.load(BASE_IMG_PATH + path).convert() #.covert() makes it more efficient for rendering(performance)
    if scaleFactor != 1: img = pygame.transform.scale(img, (img.get_width()*scaleFactor, img.get_height()*scaleFactor))
    img.set_colorkey((0,0,0))
    return img

def load_images(path, scaleFactor = 1):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)): #takes a path and gives all files in there
        images.append(load_image(path + '/' + img_name, scaleFactor))
    return images

class Animation:
    def __init__(self, images, img_dur = 5, loop = True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0 #frame of game

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop) #making copies of the images

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration *len(self.images)) #looping images (normally when you loop things you use %)
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1) # don't loop and just in case the frame goes beyond what is should it will take other min value. also we use -1 here because if frame is ex 3 then the second value should give 3 but since indexing starts at 0 it won't
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True # ending animation once the current frame is the last frame it should have
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)] #used to know what img to use