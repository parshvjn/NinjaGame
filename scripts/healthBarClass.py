import pygame

class HealthBar():
	def __init__(self, bar, x, y, screen, maxh, h): # bar: 0/False = basic_health; 1/True = advanced_health
		self.image = pygame.Surface((40,40))
		self.image.fill((200,30,30))
		self.rect = self.image.get_rect(center = (400,400))
		self.oneHealthWidth = 200
		self.current_health = 0
		self.target_health = h*self.oneHealthWidth
		self.max_health = maxh*self.oneHealthWidth
		self.health_bar_length = 400
		self.health_ratio = self.max_health / self.health_bar_length
		self.health_change_speed = 5
		self.screen = screen
		self.type = bar
		self.x, self.y = x, y

	def get_damage(self,amount):
		amount *= self.oneHealthWidth
		if self.target_health > 0:
			self.target_health -= amount
		if self.target_health < 0:
			self.target_health = 0

	def get_health(self,amount):
		amount *= self.oneHealthWidth
		if self.target_health < self.max_health:
			self.target_health += amount
		if self.target_health > self.max_health:
			self.target_health = self.max_health

	def update(self):
		if not self.type: self.basic_health()
		else: self.advanced_health()
		
	def basic_health(self):
		pygame.draw.rect(self.screen,(255,0,0),(self.x, self.y,self.target_health / self.health_ratio,25))
		pygame.draw.rect(self.screen,(255,255,255),(self.x, self.y,self.health_bar_length,25),4)

	def advanced_health(self):
		transition_width = 0
		transition_color = (255,0,0)

		if self.current_health < self.target_health:
			self.current_health += self.health_change_speed
			transition_width = int((self.target_health - self.current_health) / self.health_ratio)
			transition_color = (0,255,0)

		if self.current_health > self.target_health:
			self.current_health -= self.health_change_speed 
			transition_width = int((self.target_health - self.current_health) / self.health_ratio)
			transition_color = (255,255,0)

		health_bar = pygame.Rect(self.x, self.y, self.current_health / self.health_ratio, 25)
		transition_bar = pygame.Rect(health_bar.right, self.y, transition_width, 25)
		transition_bar.normalize()
		
		pygame.draw.rect(self.screen,(255,0,0),health_bar)
		pygame.draw.rect(self.screen,transition_color,transition_bar)	
		pygame.draw.rect(self.screen,(255,255,255),(self.x, self.y,self.health_bar_length,25),4)