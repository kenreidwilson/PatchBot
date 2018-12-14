from abc import ABC, abstractmethod

class Game(ABC):
	def __init__(self, name, title=None, url=None, desc=None, thumbnail=None, image=None, color=None):
		self.name = name
		self.title = title
		self.url = url
		self.desc = desc
		self.thumbnail = thumbnail
		self.image = image
		self.color = color
		super().__init__()

	#All game objects must have a get_patch_info method
	@abstractmethod
	def get_patch_info(self):
		pass
