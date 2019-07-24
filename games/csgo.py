import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

class CSGO():

	def __init__(self):
		self.name = "Counter Strike: Global Offensive"
		self.names = ["csgo", "cs"]
		self.patch = {"title": None, "url": None, "desc": None, "image": None}
		self.color = 16744448
		self.thumbnail = "https://i.imgur.com/OViQbBo.png"

	def get_patch_info(self):

		# Gets source of Counter-strike's blog.
		try:
			request = Request("http://blog.counter-strike.net/index.php/category/updates/", headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
			bsoup = soup(source, "html.parser")
			main_blog_div = bsoup.findAll("div",{"id":"main_blog"})
		except:
			raise Exception("Couldn't connect to " + self.name + "'s website.")

		# Gets CSGO's patch title.
		try:
			self.patch["title"] = main_blog_div[0].div.div.h2.a.contents[0]
			if self.patch["title"] is None:
				raise Exception("Could not find " + self.name + " title.")
		except:
			raise Exception("Error retrieving " + self.name + " title.")

		# Gets CSGO's patch url.
		try:
			self.patch["url"] = main_blog_div[0].div.div.h2.a["href"]
			if self.patch["url"] is None:
				raise Exception("Could not find " + self.name + " url.")
		except:
			raise Exception("Error retrieving " + self.name + " url.")

		# Gets CSGO's patch description.
		try:
			inner_post_ps = main_blog_div[0].div.div.findAll("p")
			self.patch["desc"] = inner_post_ps[1].text
			if self.patch["desc"] is None:
				raise Exception("Could not find " + self.name + " description.")
		except:
			raise Exception("Error retrieving " + self.name + " description.")
