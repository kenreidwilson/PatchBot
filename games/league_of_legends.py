import urllib
from urllib.request import Request, urlopen
from games.game import Game
from bs4 import BeautifulSoup as soup

class League(Game):

	def __init__(self, name):
		Game.__init__(self, name)
		self.color = 30070
		self.thumbnail = "https://i.imgur.com/45aABYm.png"

	def get_patch_info(self):

		# Gets source of League of Legends' patch page.
		try:
			request = Request("http://na.leagueoflegends.com/en/news/game-updates/patch", headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
		except:
			raise Exception("Couldn't connect to " + self.name + "'s website.")

		try:
			patch_update_divs = soup(source, "html.parser").findAll("div",{"class":"field field-name-field-article-media field-type-file field-label-hidden"})
		except:
			raise Exception("Error retrieving patch_update_divs")

		# Gets League of Legends' patch url.
		try:
			self.url = "https://leagueoflegends.com" + patch_update_divs[0].a["href"]
			if self.url is None:
				raise Exception("Could not find " + self.name + " url.")
		except:
			raise Exception("Error retrieving " + self.name + " url.")

		# Gets League of Legends' patch title.
		try:
			self.title = patch_update_divs[0].a["title"]
			if self.url is None:
				raise Exception("Could not find " + self.name + " url.")
		except:
			raise Exception("Error retrieving " + self.name + " url.")

		# Gets League of Legends' patch image.
		try:
			self.image = "https://leagueoflegends.com" + patch_update_divs[0].div.div.img["src"]
			if self.image is None:
				raise Exception("Could not find " + self.name + " url.")
		except:
			raise Exception("Error retrieving " + self.name + " url.")

		# Gets source of League's current patch page.
		try:
			request = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
		except:
			raise Exception("Couldn't connect to patch's url")

		# Gets League of Legends' patch description.
		try:
			patch_desc_h2s = soup(source, "html.parser").findAll("blockquote",{"class":"blockquote context"})
			self.desc = patch_desc_h2s[0].contents[0]
			if self.desc is None:
				raise Exception("Could not find " + self.name + " description.")
		except:
			raise Exception("Error retrieving " + self.name + " description.")
