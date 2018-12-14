import urllib
from urllib.request import Request, urlopen
from games.game import Game
from bs4 import BeautifulSoup as soup

class Path_of_Exile(Game):

	def __init__(self, name):
		Game.__init__(self, name)
		self.color = 16711680
		self.thumbnail = "https://i.imgur.com/UgpJHLQ.png"
			
	def get_patch_info(self):

		# Gets source of Path of Exile's patch page.
		try:
			request = Request("https://www.pathofexile.com/forum/view-forum/patch-notes", headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
			bsoup = soup(source, "html.parser")
		except:
			return "Couldn't connect to " + self.name + "'s website."
		
		# Gets Path of Exile's patch url.
		try:
			title_divs = bsoup.findAll("div",{"class":"title"})
			self.url = "https://www.pathofexile.com" + title_divs[0].a["href"]
			if self.url is None:
				return "Error retrieving " + self.name + " url."
		except:
			return "Error retrieving " + self.name + " url."
		
		# Gets source of Path of Exile's current patch page.
		try:
			request = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
			bsoup = soup(source, "html.parser")
		except:
			return "Couldn't connect to patch's url"
		
		# Gets Path of Exile's patch title.
		try:
			patch_title = bsoup.findAll("h1",{"class":"topBar last layoutBoxTitle"})
			self.title = patch_title[0].text
			if self.title is None:
				return "Error retrieving " + self.name + " title."
		except:
			return "Error retrieving " + self.name + " title."
		
		# Gets Path of Exile's patch description.
		try:
			content_divs = bsoup.findAll("div",{"class":"content"})
			if content_divs[0].ul is None:
				self.desc = content_divs[1].text
			else:
				content_lis = content_divs[0].ul.findAll("li")
				desc = ""
				for li in content_lis:
					desc = desc + li.text + "\n"
				self.desc = desc
				if self.desc is "":
					return "Error retrieving " + self.name + " description."
		except:
			return "Error retrieving " + self.name + " description."
