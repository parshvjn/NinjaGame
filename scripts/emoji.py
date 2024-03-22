import pygame

class EmojiMain:
    def __init__(self, files, surf, game):
        self.emojies = files
        self.current_emoji = None
        self.timer = 0
        self.surf = surf
        self.game = game
    
    def addOrRemoveEmoji(self, action, index = None):
        if action == 1 and self.current_emoji == None: self.current_emoji = index
        elif action == 0: self.current_emoji = None

    def update(self, offset = (0,0)):
        self.timer += 1
        if self.current_emoji != None and self.timer < 210:
            self.surf.blit(self.emojies[self.current_emoji], (self.game.player.pos[0]-2-offset[0], self.game.player.pos[1] - 4-offset[1]))
        if self.timer >=270:
            self.addOrRemoveEmoji(0)
            self.timer = 0