import os
import datetime
import discord
import aiohttp
import json
from pprint import pprint
from discord.ext import commands
from discord.ext.commands import Bot
from games.league_of_legends import League
from games.overwatch import Overwatch
from games.rust import Rust
from games.fortnite import Fortnite
from games.csgo import CSGO
from games.poe import Path_of_Exile

class Patchbot():

	def __init__(self):
		self.game_list = []
		self._add_games()
		self.data = self.get_config()
		self.bot = commands.Bot(command_prefix='!')
		self._initialize_patches()

	# Adds all games to self.game_list
	def _add_games(self):
		self.add_game(League("League of Legends"))
		self.add_game(Fortnite("Fortnite"))
		self.add_game(CSGO("CSGO"))
		self.add_game(Overwatch("Overwatch"))
		self.add_game(Rust("Rust"))
		self.add_game(Path_of_Exile("Path of Exile"))

	# Adds a game to self.game_list
	def add_game(self, game):
		self.game_list.append(game)

	# Initializes Config -> config.json.
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

	# Reinitializes Config -> config.json
	def reinitialize_config(self):
		with open("config.json", "r") as jsonFile:
			data = json.load(jsonFile)
		self.data = data

	# Generates config.json for first use of bot or if config.json is deleted.
	def _generate_config(self):
		data = {}
		data["games"] = {}
		for game in self.game_list:
			data["games"][game.name] = {}
			data["games"][game.name]["channels"] = [""]
		data["token"] = ""
		# TODO: Needs to handle permissions error
		with open(os.path.dirname(os.path.realpath(__file__)) +  os.sep + "config.json", "w") as jsonFile:
			json.dump(data, jsonFile, indent=4)

	# Returns a list of games that have updated patch info.
	def get_updated_games(self):
		updated_game_list = []
		for game in self.game_list:
			game_title = game.title
			patch_info = game.get_patch_info()
			print("[" + str(datetime.datetime.now()) + "]" + " Reinitializing " + game.name)
			# TODO: Change to use error catch/handle instead of checking if string
			if type(patch_info) is str:
				print("[" + str(datetime.datetime.now()) + "]" + " Error reinitializing " + game.name + ": " + patch_info)
			elif game.title != game_title:
				updated_game_list.append(game)
		print("[" + str(datetime.datetime.now()) + "]" + " Reinitialized Games\n")
		return updated_game_list

	# Returns a list of games that the specified channel is subscribed to.
	def get_channel_games(self, channel):
		channel_game_list = []
		for game in self.game_list:
			for channel_name in self.data['games'][game.name]['channels']:
				if channel_name == channel.name:
					channel_game_list.append(game)
		return channel_game_list

	# Returns a list of channels that are subscribed to a specified game.
	def get_game_channels(self, game):
		game_channel_list = []
		try:
			channel_list = self.bot.get_all_channels()
		except (discord.DiscordException, discord.ClientException, discord.HTTPException, discord.NotFound):
			print('get_game_channels: Error connecting to Discord')
			return game_channel_list

			for channel in channel_list:
				for channel_name in self.data['games'][game.name]['channels']:
					if channel_name == channel.name:
						game_channel_list.append(channel)
			return game_channel_list

	# Initializes Game objects by calling their get_patch_info function.
	def _initialize_patches(self):
		print("Initializing Games:\n")
		for game in self.game_list:
			patch_info = game.get_patch_info()
			if type(patch_info) is str:
				print (game.name + " error initializing: " + patch_info)
			else:
				print(game.name + " initialized.")
		print("\nDone Initializing\n")

	# Returns an embed patch message for a specified game.
	def get_patch_message(self, game):
		embed = discord.Embed()
		if game.title is None or game.url is None:
			embed.title = "Error occurred when retrieving " + game.name + " patch notes"
			return embed
		embed.title = game.name + " - " + game.title
		embed.url = game.url
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

	async def get_embed_message(self):
		embed_message = discord.Embed()
		embed_message.title = 'Wilsøn\'s PatchBot'
		embed_message.color = 16200039
		embed_message.description = 'PatchBot delivers game update patch notes on demand and when they release.'
		embed_message.add_field(name='Commands', value="!patch -> Displays game patch.\n!patchbot reload -> Reloads config.", inline=False)
		embed_message.add_field(name='Source', value='https://github.com/Wils0248n/Patchbot', inline=False)
		embed_message.set_image(url='https://i.imgur.com/DNFHDPr.png')
		embed_message.set_thumbnail(url='https://i.imgur.com/o74macK.png')
		dev = await self.bot.get_user_info(259624839604731906)
		embed_message.set_footer(text = 'Developer: ' + dev.name + "#" + dev.discriminator)
		return embed_message
