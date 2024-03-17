import pygame,sys

class Button:
	def __init__(self,text,width,height,pos,elevation, font, display, game):
		#Core attributes 
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]
		
		self.font = font
		self.display = display
		self.game = game


		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = '#475F77'

		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#354B5E'
		#text
		self.text_surf = self.font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self, nameType = None):
		# elevation logic 
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center 

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		pygame.draw.rect(self.display,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(self.display,self.top_color, self.top_rect,border_radius = 12)
		self.display.blit(self.text_surf, self.text_rect)
		self.check_click(nameType)

	def check_click(self, nameType):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint((mouse_pos[0]/6, mouse_pos[1]/5.75)):
			self.top_color = '#D74B4B'
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					if nameType == 'game':
						self.game.run()
					elif nameType == 'option':
						self.game.options()
					elif nameType == 'resolution':
						pass
					elif nameType == 'controls':
						pass
					self.pressed = False
		else:
			self.dynamic_elecation = self.elevation
			self.top_color = '#475F77'