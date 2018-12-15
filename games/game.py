from abc import ABC, abstractmethod

'''
The Game Class.
This class is not meant to be instantiated.
It is meant to be abstract and the parent class of all the game objects used
in the Patchbot class.
The child of a game object only requires a name to be instantiated, and must
have a get_patch_info method.
'''
class Game(ABC):
	'''
	Initializes a Game object.
	A Game object must have a name.
	'''
	def __init__(self, name, title=None, url=None, desc=None, thumbnail=None, image=None, color=None):
		self.name = name
		self.title = title
		self.url = url
		self.desc = desc
		self.thumbnail = thumbnail
		self.image = image
		self.color = color
		super().__init__()

	'''
	All game objects must have a get_patch_info method.
	'''
	@abstractmethod
	def get_patch_info(self):
		pass
