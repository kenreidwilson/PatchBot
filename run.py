import discord, asyncio, time, aiohttp, sys
from aiohttp import errors
from patchbot import Patchbot

patchbot = Patchbot()

'''
Initializes patch information and starts the bot.
'''
def main():
	while not patchbot.bot.is_closed:
		try:
			push_game_updates_task = patchbot.bot.loop.create_task(push_game_updates())
			patchbot.bot.loop.run_until_complete(patchbot.bot.start(sys.argv[1]))
		except aiohttp.errors.ClientOSError:
			print("Could not connect to Discord, reconnecting...")
			push_game_updates_task.cancel()
			time.sleep(10)
		except RuntimeError as e:
			print("RuntimeError occured:\n\n" + str(e) + "\n\n")
			push_game_updates_task.cancel()
			time.sleep(60)
		except IndexError:
			print("You must enter a bot token.\n")
			print("Usage: python3 run.py <bot-token>")
			push_game_updates_task.cancel()
			sys.exit(1)
		except discord.errors.LoginFailure:
			print("Invalid bot token.\n")
			push_game_updates_task.cancel()
			sys.exit(1)
		except Exception as e:
			print("Error Occured:\n\n" + str(e) + "\n\n")
			time.sleep(10)

'''
Checks if a patch has been released for all games in patchbot.game_list.
Every 5 minutes, all games update their patch information and games with new
patches have their embed patch message pushed to their subscribed channels.
'''
async def push_game_updates():
	await patchbot.bot.wait_until_ready()
	while not patchbot.bot.is_closed:
		await asyncio.sleep(300)
		for game in patchbot.get_updated_games():
			try:
				for channel in patchbot.get_game_channels(game):
					await patchbot.bot.send_message(channel, embed=patchbot.get_patch_message(game))
			except (discord.DiscordException, discord.ClientException, discord.HTTPException, discord.NotFound):
				print("Could not connect to Discord when displaying " + game.name + " new patch information.")

'''
Handles Patchbot commands sent as messages on a discord server.
'''
@patchbot.bot.event
async def on_message(message):
	'''
	Handles !patch command.
	Sends current patch information, for all games the channel is subscribed to,
	to the channel that the message came from.
	'''
	if message.content == '!patch':
		channel_games = patchbot.get_channel_games(message.channel)
		if len(channel_games) is 0:
			await patchbot.bot.send_message(message.channel, message.channel.name + " is not subscribed to any games.")
		else:
			for game in channel_games:
				await patchbot.bot.send_message(message.channel, embed=patchbot.get_patch_message(game))

	'''
	Handles !patch command for a specific game.
	Sends current patch information, for the game specified after !patch, to
	the channel that the message came from.
	'''
	# TODO: Handle game names with spaces correctly.
	if message.content.startswith('!patch '):
		for game in patchbot.game_list:
			if message.content.split(" ")[1].lower() == game.name.split(" ")[0].lower():
				await patchbot.bot.send_message(message.channel, embed=patchbot.get_patch_message(game))
				return
		await patchbot.bot.send_message(message.channel, "Could not find patch info for " + message.content.split(" ")[1])

	'''
	Handles !patchbot command.
	Sends patchbot's embed about message to the channel that the message came
	from.
	'''
	if message.content == '!patchbot':
		dev = await patchbot.bot.get_user_info(259624839604731906)
		await patchbot.bot.send_message(message.channel, embed=patchbot.get_embed_message(dev))

	'''
	Handles !patchbot reload command.
	Reloads patchbot.data with data from config.json.
	'''
	if message.content.startswith('!patchbot '):
		if 'reload' in message.content:
			patchbot.reinitialize_config()
			await patchbot.bot.send_message(message.channel, "Reinitialized config.json")

'''
Handles when Patchbot is ready.
'''
@patchbot.bot.event
async def on_ready():
	print(patchbot.bot.user.name + " is initialized.\n")
	await patchbot.bot.change_presence(game=discord.Game(name="Patchbot | !patchbot"))

if __name__ == '__main__':
	main()
