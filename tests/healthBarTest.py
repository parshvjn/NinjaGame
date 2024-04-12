import pygame, sys

class Player():
	def __init__(self):
		self.image = pygame.Surface((40,40))
		self.image.fill((200,30,30))
		self.rect = self.image.get_rect(center = (400,400))
		self.current_health = 200
		self.target_health = 500
		self.max_health = 1000
		self.health_bar_length = 400
		self.health_ratio = self.max_health / self.health_bar_length
		self.health_change_speed = 5

	def get_damage(self,amount):
		amount*=200
		if self.target_health > 0:
			self.target_health -= amount
		if self.target_health < 0:
			self.target_health = 0

	def get_health(self,amount):
		amount*=200
		if self.target_health < self.max_health:
			self.target_health += amount
		if self.target_health > self.max_health:
			self.target_health = self.max_health

	def update(self):
		self.basic_health()
		self.advanced_health()
		
	def basic_health(self):
		pygame.draw.rect(screen,(255,0,0),(10,10,self.target_health / self.health_ratio,25))
		pygame.draw.rect(screen,(255,255,255),(10,10,self.health_bar_length,25),4)

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

		health_bar = pygame.Rect(10, 45, self.current_health / self.health_ratio, 25)
		transition_bar = pygame.Rect(health_bar.right, 45, transition_width, 25)
		transition_bar.normalize()
		
		pygame.draw.rect(screen,(255,0,0),health_bar)
		pygame.draw.rect(screen,transition_color,transition_bar)	
		pygame.draw.rect(screen,(255,255,255),(10,45,self.health_bar_length,25),4)	



pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
player = Player()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player.get_health(1)
			if event.key == pygame.K_DOWN:
				player.get_damage(1)

	screen.fill((30,30,30))
	player.update()
	pygame.display.update()
	clock.tick(60)