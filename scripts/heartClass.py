import pygame, sys

class HeartSystem():
	def __init__(self, bar, h, maxH, screen, x, y): # bar: 0/False = full hearts; 1 = empty hearts; 2 = half hearts
		self.health = h
		self.max_health = maxH
		self.full_heart = pygame.image.load('../data/images/hearts/full_heart.png').convert_alpha()
		self.half_heart = pygame.image.load('../data/images/hearts/half_heart.png').convert_alpha()
		self.empty_heart = pygame.image.load('../data/images/hearts/empty_heart.png').convert_alpha()
		self.screen = screen
		self.type = bar
		self.x, self.y = x, y

	def get_damage(self):
		if self.health > 0:
			self.health -= 1

	def get_health(self):
		if self.health < self.max_health:
			self.health += 1

	def full_hearts(self):
		for heart in range(self.health):
			self.screen.blit(self.full_heart,(heart * 50 + self.x, self.y))

	def empty_hearts(self):
		for heart in range(self.max_health):
			if heart < self.health:
				self.screen.blit(self.full_heart,(heart * 50 + self.x, self.y))
			else:
				self.screen.blit(self.empty_heart,(heart * 50 + self.x, self.y))

	def half_hearts(self):
		self.half_hearts_total = self.health / 2
		self.half_heart_exists = self.half_hearts_total - int(self.half_hearts_total) != 0

		for heart in range(int(self.max_health / 2)):
			if int(self.half_hearts_total) > heart:
				self.screen.blit(self.full_heart,(heart * 50 + self.x, self.y))
			elif self.half_heart_exists and int(self.half_hearts_total) == heart:
				self.screen.blit(self.half_heart,(heart * 50 + self.x, self.y))
			else:
				self.screen.blit(self.empty_heart,(heart * 50 + self.x, self.y))

	def update(self):
		if not self.type: self.full_hearts()
		elif self.type == 1: self.empty_hearts()
		else: self.half_hearts()