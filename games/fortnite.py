import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

class Fortnite():

	def __init__(self):
		self.name = "Fortnite"
		self.names = ["fortnite"]
		self.patch = {"title": None, "url": None, "desc": None, "image": None}
		self.color = 6304630
		self.thumbnail = "https://i.imgur.com/YxrgI30.jpg"

	def get_patch_info(self):

		# Gets source of Fortnite's patch page.
		try:
			request = Request("https://www.epicgames.com/fortnite/en-US/patch-notes/", headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
			bsoup = soup(source, "html.parser")
		except:
			raise Exception("Couldn't connect to " + self.name + "'s website.")

		# Gets Fortnite's patch title.
		try:
			self.patch["title"] = bsoup.title.text
			if self.patch["title"] is None:
				raise Exception("Could not find " + self.name + " title.")
		except:
			raise Exception("Error retrieving " + self.name + " title.")

		# Gets Fortnite's patch URL.
		try:
			metas = bsoup.findAll("meta",{"data-react-helmet":"true"})
			self.patch["url"] = metas[1]["content"]
			if self.patch["url"] is None:
				raise Exception("Could not find " + self.name + " url.")
		except:
			raise Exception("Error retrieving " + self.name + " url.")

		# Gets Fortnite's patch image.
		try:
			image_divs = bsoup.findAll("div",{"class":"background-image"})
			self.patch["image"] = self.find_between(image_divs[0]["style"], "background:url(", ")")
			if self.patch["image"] is None:
				raise Exception("Could not find " + self.name + " image.")
		except:
			raise Exception("Error retrieving " + self.name + " image.")

		# Gets Fortnite's patch description.
		try:
			titles = bsoup.findAll("h1")
			descs = bsoup.findAll("div",{"class":"patch-notes-description"})
			self.patch["desc"] = titles[2].text + "\n\n" + descs[0].text
			if self.patch["desc"] is None:
				raise Exception("Could not find " + self.name + " description.")
		except:
			raise Exception("Error retrieving " + self.name + " description.")

	def find_between(self, s, first, last):
		start = s.index(first) + len(first)
		end = s.index(last, start)
		return s[start:end]
