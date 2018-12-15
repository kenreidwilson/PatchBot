import urllib
from urllib.request import Request, urlopen
from games.game import Game
from bs4 import BeautifulSoup as soup

class Overwatch(Game):

	def __init__(self, name):
		Game.__init__(self, name)
		self.color = 16777215
		self.thumbnail = "https://i.imgur.com/NDhNeBj.png"

	def get_patch_info(self):

		# Gets source of Overwatch's patch page.
		try:
			request = Request("https://playoverwatch.com/en-us/news/patch-notes/pc/", headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
			bsoup = soup(source, "html.parser")
		except:
			raise Exception("Couldn't connect to " + self.name + "'s website.")

		try:
			side_div = bsoup.findAll("div",{"class":"PatchNotesSideNav"})
		except:
			raise Exception("Error retrieving side_div")

		# Gets Overwatch's patch title.
		try:
			self.title = side_div[0].ul.li.h3.text
			if self.title is None:
				raise Exception("Could not find " + self.name + " title.")
		except:
			raise Exception("Error retrieving " + self.name + " title.")

		# Gets Overwatch's patch url.
		try:
			self.url = "https://playoverwatch.com/en-us/news/patch-notes/pc/" + side_div[0].ul.li.a["href"]
			if self.url is None:
				raise Exception("Could not find " + self.name + " url.")
		except:
			raise Exception("Error retrieving " + self.name + " url.")

		# Gets Overwatch's patch image.
		try:
			heading_image_div = bsoup.findAll("div",{"class":"HeadingBanner"})
			self.image = self.find_between(heading_image_div[0]["style"], "url(", ")")
			if self.image is None:
				raise Exception("Could not find " + self.name + " image.")
		except:
			raise Exception("Error retrieving " + self.name + " image.")

		# Gets Overwatch's patch description.
		try:
			calloutbox_div = bsoup.findAll("div",{"class":"CalloutBox"})
			desc = ""
			for div in calloutbox_div:
				try:
					desc = desc + div.p.text + "\n"
				except AttributeError:
					pass
			self.desc = desc
			if self.desc is "":
				raise Exception("Could not find " + self.name + " description.")
		except:
			raise Exception("Error retrieving " + self.name + " description.")

	def find_between(self, s, first, last):
		start = s.index(first) + len(first)
		end = s.index(last, start)
		return s[start:end]
