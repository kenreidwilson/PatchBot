import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

class League():

	def __init__(self):
		self.name = "League of Legends"
		self.names = ["league", "league of legends", "lol"]
		self.patch = {"title": None, "url": None, "desc": None, "image": None}
		self.color = 30070
		self.thumbnail = "https://i.imgur.com/45aABYm.png"

	def get_patch_info(self):

		# Gets source of League of Legends' patch page.
		try:
			request = Request("http://na.leagueoflegends.com/en/news/game-updates/patch", headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
		except:
			raise Exception("Couldn't connect to " + self.name + "' website.")

		try:
			patch_update_divs = soup(source, "html.parser").findAll("div",{"class":"field field-name-field-article-media field-type-file field-label-hidden"})
		except:
			raise Exception("Error retrieving patch_update_divs")

		# Gets League of Legends' patch url.
		try:
			self.patch["url"] = "https://leagueoflegends.com" + patch_update_divs[0].a["href"]
			if self.patch["url"] is None:
				raise Exception("Could not find " + self.name + " url.")
		except:
			raise Exception("Error retrieving " + self.name + " url.")

		# Gets League of Legends' patch title.
		try:
			self.patch["title"] = patch_update_divs[0].a["title"]
			if self.patch["url"] is None:
				raise Exception("Could not find " + self.name + " url.")
		except:
			raise Exception("Error retrieving " + self.name + " url.")

		# Gets League of Legends' patch image.
		try:
			self.patch["image"] = "https://leagueoflegends.com" + patch_update_divs[0].div.div.img["src"]
			if self.patch["image"] is None:
				raise Exception("Could not find " + self.name + " url.")
		except:
			raise Exception("Error retrieving " + self.name + " url.")

		# Gets source of League's current patch page.
		try:
			request = Request(self.patch["url"], headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
		except:
			raise Exception("Couldn't connect to patch's url")

		# Gets League of Legends' patch description.
		try:
			patch_desc_h2s = soup(source, "html.parser").findAll("blockquote",{"class":"blockquote context"})
			self.patch["desc"] = patch_desc_h2s[0].contents[0]
			if self.patch["desc"] is None:
				raise Exception("Could not find " + self.name + " description.")
		except:
			raise Exception("Error retrieving " + self.name + " description.")
