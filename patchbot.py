import os, json, datetime, discord, aiohttp
from pprint import pprint
from discord.ext import commands
from discord.ext.commands import Bot
from games.league_of_legends import League
from games.overwatch import Overwatch
from games.rust import Rust
from games.fortnite import Fortnite
from games.csgo import CSGO
from games.poe import Path_of_Exile

'''
The Patchbot Class.
'''
class Patchbot():

	'''
	Initializes the Patchbot object.
	'''
	def __init__(self):
		self.game_list = []
		self._add_games()
		self.data = self.get_config()
		self.bot = commands.Bot(command_prefix='!')
		self._initialize_patches()

	'''
	Adds games objects to self.game_list.
	'''
	def _add_games(self):
		self.add_game(League("League of Legends"))
		self.add_game(Fortnite("Fortnite"))
		self.add_game(CSGO("CSGO"))
		self.add_game(Overwatch("Overwatch"))
		self.add_game(Rust("Rust"))
		self.add_game(Path_of_Exile("Path of Exile"))

	'''
	Adds a game to self.game_list.
	'''
	def add_game(self, game):
		# TODO: add a check to see if the game is a child class of a game object.
		self.game_list.append(game)

	'''
	Loads config data from config.json, located in the current working dir.
	If config.json doesn't exist, get_config generates a config.json file with
	data based on the games in self.game_list.
	'''
	def get_config(self):
		try:
			with open("config.json", "r") as jsonFile:
				data = json.load(jsonFile)
			return data
		except FileNotFoundError:
			self._generate_config()
			with open("config.json", "r") as jsonFile:
				data = json.load(jsonFile)
			return data

	'''
	Generates a config.json file for first use of bot or if config.json was
	deleted.
	'''
	def _generate_config(self):
		data = {}
		data["games"] = {}
		for game in self.game_list:
			data["games"][game.name] = {}
			data["games"][game.name]["channels"] = [""]
		data["token"] = ""
		# TODO: Needs to handle permissions error.
		with open(os.path.dirname(os.path.realpath(__file__)) +  os.sep + "config.json", "w") as jsonFile:
			json.dump(data, jsonFile, indent=4)

	'''
	Reloads config data from config.json.
	'''
	def reinitialize_config(self):
		with open("config.json", "r") as jsonFile:
			data = json.load(jsonFile)
		self.data = data

	'''
	Returns a list of game objects whos current patch title doesn't match their
	new patch title after updating their patch information.
	'''
	def get_updated_games(self):
		updated_game_list = []
		for game in self.game_list:
			print("[" + str(datetime.datetime.now()) + "]" + " Reinitializing " + game.name)
			current_patch_title = game.title
			try:
				game.get_patch_info()
			except Exception as e:
				print("[" + str(datetime.datetime.now()) + "]" + " Error reinitializing " + game.name + ": " + str(e))
			else:
				if current_patch_title != game.title:
					updated_game_list.append(game)
		print("[" + str(datetime.datetime.now()) + "]" + " Reinitialized Games\n")
		return updated_game_list

	'''
	Returns a list of games that the specified channel is subscribed to.
	"Subscribed" meaning the channel name is within a list of channel names
	under the game name in config.json.
	'''
	def get_channel_games(self, channel):
		game_list = []
		for game in self.game_list:
			for channel_name in self.data['games'][game.name]['channels']:
				if channel_name == channel.name:
					game_list.append(game)
		return game_list

	'''
	Returns a list of channels that are subscribed to a specified game.
	"Subscribed" meaning the channel name is within a list of channel names
	under the game name in config.json.
	'''
	def get_game_channels(self, game):
		channel_list = []
		for channel in self.bot.get_all_channels():
			for channel_name in self.data['games'][game.name]['channels']:
				if channel_name == channel.name:
					channel_list.append(channel)
		return channel_list

	'''
	Initializes all Game objects in self.game_list by calling their
	get_patch_info function.
	'''
	def _initialize_patches(self):
		print("Initializing Games:\n")
		for game in self.game_list:
			try:
				game.get_patch_info()
			except Exception as e:
				print (game.name + " error initializing: " + str(e))
			else:
				print(game.name + " initialized.")
		print("\nDone Initializing\n")

	'''
	Returns a discord embed object that contains the patch message for the
	specified game.
	'''
	def get_patch_message(self, game):
		embed = discord.Embed()
		# A patch message must at least have a title and a link.
		if game.title is None or game.url is None:
			embed.title = "Error occurred when retrieving " + game.name + " patch notes"
			return embed
		embed.title = game.name + " - " + game.title
		embed.url = game.url
		# The patch description should not exceed 400 characters.
		if game.desc is not None:
			desc = ""
			game_strings = game.desc.split("\n")
			for string in game_strings:
				desc = desc + string + "\n"
				if len(desc) > 400:
					desc = desc + "..."
					break
			embed.description = desc
		if game.color is not None:
			embed.color = game.color
		if game.thumbnail is not None:
			embed.set_thumbnail(url=game.thumbnail)
		if game.image is not None:
			embed.set_image(url=game.image)
		return embed

	'''
	Returns a discord embed object that contains about information about Patchbot.
	'''
	def get_embed_message(self, dev):
		embed_message = discord.Embed()
		embed_message.title = 'Wilsøn\'s PatchBot'
		embed_message.color = 16200039
		embed_message.description = 'PatchBot delivers game update patch notes on demand and when they release.'
		embed_message.add_field(name='Commands', value="!patch -> Displays game patch.\n!patchbot reload -> Reloads config.", inline=False)
		embed_message.add_field(name='Source', value='https://github.com/Wils0248n/Patchbot', inline=False)
		embed_message.set_image(url='https://i.imgur.com/DNFHDPr.png')
		embed_message.set_thumbnail(url='https://i.imgur.com/o74macK.png')
		embed_message.set_footer(text = 'Developer: ' + dev.name + "#" + dev.discriminator)
		return embed_message
