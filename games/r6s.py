from games.game import Game

class Rainbow(Game):
	def __init__(self, name):
		Game.__init__(self, name)
			
	def get_patch_info(self):
		return "Rainbow Six Siege patch_message method is under maintenance"
