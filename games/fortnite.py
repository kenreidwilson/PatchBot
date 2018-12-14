import urllib
from urllib.request import Request, urlopen
from games.game import Game
from bs4 import BeautifulSoup as soup

class Fortnite(Game):

	def __init__(self, name):
		Game.__init__(self, name)
		self.color = 6304630
		self.thumbnail = "https://i.imgur.com/YxrgI30.jpg"

	def get_patch_info(self):

		# Gets source of Fortnite's patch page.
		try:
			request = Request("https://www.epicgames.com/fortnite/en-US/patch-notes/", headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
			bsoup = soup(source, "html.parser")
		except:
			return "Couldn't connect to " + self.name + "'s website."
		
		# Gets Fortnite's patch title
		try:
			self.title = bsoup.title.text
			if self.title is None:
				return "Error retrieving " + self.name + " title."
		except:
			return "Error retrieving " + self.name + " title."
		
		# Gets Fortnite's patch URL
		try:
			metas = bsoup.findAll("meta",{"data-react-helmet":"true"})
			self.url = metas[1]["content"]
			if self.url is None:
					return "Error retrieving " + self.name + " url."
		except:
			return "Error retrieving " + self.name + " url."
		
		# Gets Fortnite's patch image
		try:
			image_divs = bsoup.findAll("div",{"class":"background-image"})
			self.image = self.find_between(image_divs[0]["style"], "background:url(", ")")
			if self.image is None:
				return "Error retrieving " + self.name + " image."
		except:
			return "Error retrieving " + self.name + " image."
		
		# Gets Fortnite's patch description
		try:
			titles = bsoup.findAll("h1")
			descs = bsoup.findAll("div",{"class":"patch-notes-description"})
			self.desc = titles[2].text + "\n\n" + descs[0].text
			if self.desc is None:
				return "Error retrieving " + self.name + " description."
		except:
			return "Error retrieving " + self.name + " description."

	def find_between(self, s, first, last):
		start = s.index(first) + len(first)
		end = s.index(last, start)
		return s[start:end]