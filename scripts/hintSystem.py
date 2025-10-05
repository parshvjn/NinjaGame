from scripts.timer import Timer
import random

class hints:
    def __init__(self, surf, hints: list, game):
        self.surf = surf
        self.hints = hints
        self.game = game
        self.listIndex = random.randint(0, len(self.hints)-1)
        self.htime = Timer(3.5)
    
    def update(self):
        if self.htime.count():
            if self.listIndex != len(self.hints)-1:
                self.listIndex += 1
            else:
                self.listIndex = 0
            self.htime.redo()

    def render(self, pos):
        if type(self.hints[self.listIndex]) == list:
            for i, text in enumerate(self.hints[self.listIndex]):
                pos[1]+=(i*12)
                self.game.draw_text(f'Hint: {text}', self.game.font, (0,0,0), pos[0], pos[1], surf = self.surf, hint = True) if i ==0 else self.game.draw_text(text, self.game.font, (0,0,0), pos[0]+5, pos[1], surf = self.surf, hint = True)
        else:
            self.game.draw_text(f'Hint: {self.hints[self.listIndex]}', self.game.font, (0,0,0), pos[0], pos[1], surf = self.surf, hint = True)