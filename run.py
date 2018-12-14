import discord
import asyncio
import time
import aiohttp
from aiohttp import errors
from patchbot import Patchbot

patchbot = Patchbot()

# Starts update timer.
async def push_game_updates():
	await patchbot.bot.wait_until_ready()
	while not patchbot.bot.is_closed:
		await asyncio.sleep(300)
		for game in patchbot.get_updated_games():
			for channel in patchbot.get_game_channels(game):
				await patchbot.bot.send_message(channel, embed=patchbot.get_patch_message(game))

@patchbot.bot.event
async def on_message(message):
	# Handles !patch command.
	if message.content == '!patch':
		channel_games = patchbot.get_channel_games(message.channel)
		if len(channel_games) is 0:
			await patchbot.bot.send_message(message.channel, message.channel.name + " is not subscribed to any games.")
		else:
			for game in channel_games:
				await patchbot.bot.send_message(message.channel, embed=patchbot.get_patch_message(game))

	#Handles !patch command for a specific game.
	#TODO Handle game names with spaces correctly. 
	if message.content.startswith('!patch '):
		for game in patchbot.game_list:
			if message.content.split(" ")[1].lower() == game.name.split(" ")[0].lower():
				await patchbot.bot.send_message(message.channel, embed=patchbot.get_patch_message(game))
				return
		await patchbot.bot.send_message(message.channel, "Could not find patch info for " + message.content.split(" ")[1])

	# Handles !patchbot command.
	if message.content == '!patchbot':
		await patchbot.bot.send_message(message.channel, embed=await patchbot.get_embed_message())

	# Handles !patchbot reload command.
	if message.content.startswith('!patchbot '):
		if 'reload' in message.content:
			patchbot.reinitialize_config()
			await patchbot.bot.send_message(message.channel, "Reinitialized config.json")

@patchbot.bot.event
async def on_ready():
	print(patchbot.bot.user.name + " is initialized.\n")
	await patchbot.bot.change_presence(game=discord.Game(name="Patchbot | !patchbot"))

# Initializes patch information and starts the bot
def start():
	if patchbot.data['token'] == "":
		print("Token: " + patchbot.data['token'])
		print("\nEnter bot token in \"config.json\", located in this script's directory\n")
	else:
		while not patchbot.bot.is_closed:
			try:
				push_game_updates_task = patchbot.bot.loop.create_task(push_game_updates())
				patchbot.bot.loop.run_until_complete(patchbot.bot.start(patchbot.data['token']))
			except aiohttp.errors.ClientOSError:
				print("Could not connect to Discord, reconnecting...")
				push_game_updates_task.cancel()
				time.sleep(10)
			except RuntimeError as e:
				print("RuntimeError occured:\n\n" + str(e) + "\n\n")
				push_game_updates_task.cancel()
				time.sleep(60)

start()
