import asyncio, aiohttp, datetime, discord, json, os, time, sys
from pprint import pprint
from discord.ext import commands
from discord.ext.commands import Bot
from games import *

class Patchbot():
	"""
	The Patchbot Class.
	"""

	def __init__(self):
		"""
		Initializes the Patchbot object.
		"""
		self.game_list = []
		self.add_games()
		self.data = self.get_config()
		self.bot = commands.Bot(command_prefix='!')

	def add_games(self):
		"""
		Adds games objects to self.game_list.
		"""
		self.game_list.append(League())
		self.game_list.append(Fortnite())
		self.game_list.append(CSGO())
		self.game_list.append(Overwatch())
		self.game_list.append(Rust())
		self.game_list.append(Path_of_Exile())

	def get_config(self):
		"""
		Loads config data from config.json, located in the current working dir.
		If config.json doesn't exist, get_config generates a config.json file with
		data based on the games in self.game_list.
		"""
		try:
			with open("config" + os.sep + "config.json", "r") as jsonFile:
				data = json.load(jsonFile)
			return data
		except FileNotFoundError:
			self.generate_config()
			with open("config" + os.sep + "config.json", "r") as jsonFile:
				data = json.load(jsonFile)
			return data

	def generate_config(self):
		"""
		Generates a config.json file for first use of bot or if config.json was
		deleted.
		"""
		data = {}
		data["games"] = {}
		for game in self.game_list:
			data["games"][game.name] = {}
			data["games"][game.name]["channels"] = [""]
		# TODO: Needs to handle permissions error.
		with open(os.path.dirname(os.path.realpath(__file__)) +  os.sep + "config" + os.sep + "config.json", "w") as jsonFile:
			json.dump(data, jsonFile, indent=4)

	def reinitialize_config(self):
		"""
		Reloads config data from config.json.
		"""
		with open("config" + os.sep + "config.json", "r") as jsonFile:
			data = json.load(jsonFile)
		self.data = data

	def get_updated_games(self):
		"""
		Returns a list of game objects whos current patch title doesn't match their
		new patch title after updating their patch information.
		"""
		updated_game_list = []
		for game in self.game_list:
			print("[" + str(datetime.datetime.now()) + "]" + " Reinitializing " + game.name)
			current_patch_title = game.patch["title"]
			try:
				game.get_patch_info()
			except Exception as e:
				print("[" + str(datetime.datetime.now()) + "]" + " Error reinitializing " + game.name + ": " + str(e))
			else:
				if current_patch_title != game.patch["title"]:
					updated_game_list.append(game)
		print("[" + str(datetime.datetime.now()) + "]" + " Reinitialized Games\n")
		return updated_game_list

	def get_channel_games(self, channel):
		"""
		Returns a list of games that the specified channel is subscribed to.
		"Subscribed" meaning the channel name is within a list of channel names
		under the game name in config.json.
		"""
		game_list = []
		for game in self.game_list:
			for channel_name in self.data['games'][game.name]['channels']:
				if channel_name == channel.name:
					game_list.append(game)
		return game_list

	def get_game_channels(self, game):
		"""
		Returns a list of channels that are subscribed to a specified game.
		"Subscribed" meaning the channel name is within a list of channel names
		under the game name in config.json.
		"""
		channel_list = []
		for channel in self.bot.get_all_channels():
			for channel_name in self.data['games'][game.name]['channels']:
				if channel_name == channel.name:
					channel_list.append(channel)
		return channel_list

	def initialize_patches(self):
		"""
		Initializes all Game objects in self.game_list by calling their
		get_patch_info function.
		"""
		print("Initializing Games:\n")
		for game in self.game_list:
			try:
				game.get_patch_info()
			except Exception as e:
				print (game.name + " error initializing: " + str(e))
			else:
				print(game.name + " initialized.")
		print("\nDone Initializing\n")

	def get_patch_message(self, game):
		"""
		Returns a discord embed object that contains the patch message for the
		specified game.
		"""
		embed = discord.Embed()
		# A patch message must at least have a title and a link.
		if game.patch["title"] is None or game.patch["url"] is None:
			embed.title = "Error occurred when retrieving " + game.name + " patch notes"
			return embed
		embed.title = game.name + " - " + game.patch["title"]
		embed.url = game.patch["url"]
		# The patch description should not exceed 400 characters.
		if game.patch["desc"] is not None:
			desc = ""
			game_strings = game.patch["desc"].split("\n")
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
		if game.patch["image"] is not None:
			embed.set_image(url=game.patch["image"])
		return embed

	def get_embed_message(self, dev):
		"""
		Returns a discord embed object that contains about information about Patchbot.
		"""
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

patchbot = Patchbot()

def main():
	"""
	Initializes patch information and starts the bot.
	"""
	while True:
		try:
			push_game_updates_task = patchbot.bot.loop.create_task(push_game_updates())
			patchbot.bot.loop.run_until_complete(patchbot.bot.start(sys.argv[1]))
		#except aiohttp.errors.ClientOSError:
			#print("Could not connect to Discord, reconnecting...")
			#push_game_updates_task.cancel()
			#time.sleep(10)
		#except RuntimeError as e:
			#print("RuntimeError occured:\n\n" + str(e) + "\n\n")
			#push_game_updates_task.cancel()
			#time.sleep(60)
		except IndexError:
			print("You must enter a bot token.")
			print("Usage: python3 patchbot.py <bot-token>")
			push_game_updates_task.cancel()
			sys.exit(1)
		except discord.errors.LoginFailure:
			print("Discord login failed: Invalid bot token.")
			push_game_updates_task.cancel()
			sys.exit(1)
		except KeyboardInterrupt:
			print("\nExitting Gracefully")
			push_game_updates_task.cancel()
			patchbot.bot.loop.run_until_complete(patchbot.bot.close())
			sys.exit(0)

async def push_game_updates():
	"""
	Checks if a patch has been released for all games in patchbot.game_list.
	Every 5 minutes, all games update their patch information and games with new
	patches have their embed patch message pushed to their subscribed channels.
	"""
	await patchbot.bot.wait_until_ready()
	while not patchbot.bot.is_closed:
		await asyncio.sleep(300)
		for game in patchbot.get_updated_games():
			try:
				for channel in patchbot.get_game_channels(game):
					await channel.send(embed=patchbot.get_patch_message(game))
			except (discord.DiscordException, discord.ClientException, discord.HTTPException, discord.NotFound):
				print("Could not connect to Discord when displaying " + game.name + " new patch information.")

@patchbot.bot.event
async def on_message(message):
	"""
	Handles Patchbot commands sent as messages on a discord server.
	"""

	if message.content == '!patch':
		"""
		Handles !patch command.
		Sends current patch information, for all games the channel is subscribed to,
		to the channel that the message came from.
		"""
		channel_games = patchbot.get_channel_games(message.channel)
		if len(channel_games) is 0:
			await message.channel.send(message.channel.name + " is not subscribed to any games.")
		else:
			for game in channel_games:
				await message.channel.send(embed=patchbot.get_patch_message(game))

	# TODO: Handle game names with spaces correctly.
	if message.content.startswith('!patch '):
		"""
		Handles !patch command for a specific game.
		Sends current patch information, for the game specified after !patch, to
		the channel that the message came from.
		"""
		for game in patchbot.game_list:
			if message.content.split(" ")[1].lower() in game.names:
				await message.channel.send(embed=patchbot.get_patch_message(game))
				return
		await message.channel.send("Could not find patch info for " + message.content.split(" ")[1])

	if message.content == '!patchbot':
		"""
		Handles !patchbot command.
		Sends patchbot's embed about message to the channel that the message came
		from.
		"""
		dev = patchbot.bot.get_user(259624839604731906)
		await message.channel.send(embed=patchbot.get_embed_message(dev))

	if message.content.startswith('!patchbot '):
		"""
		Handles !patchbot reload command.
		Reloads patchbot.data with data from config.json.
		"""
		if 'reload' in message.content:
			patchbot.reinitialize_config()
			await message.channel.send("Reinitialized config.json")

@patchbot.bot.event
async def on_ready():
	"""
	Handles when Patchbot is ready.
	"""
	print(patchbot.bot.user.name + " is online.\n")
	patchbot.initialize_patches()
	# TODO: Presence not showing.
	await patchbot.bot.change_presence(activity=discord.Activity(game=discord.Game(name="Patchbot | !patchbot")))

main()
