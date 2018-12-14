import urllib
from urllib.request import Request, urlopen
from games.game import Game
from bs4 import BeautifulSoup as soup

class Rust(Game):

	def __init__(self, name):
		Game.__init__(self, name)
		self.color = 13517355
		self.thumbnail = "https://i.imgur.com/WWZIaE8.jpg"
			
	def get_patch_info(self):

		# Gets source of Facepunch's blog.
		try:
			request = Request("https://rust.facepunch.com/blog/", headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
		except:
			return "Couldn't connect to " + self.name + "'s website."
		
		# Gets divs in the monthgroup div
		try:
			div_monthgroup = soup(source, "html.parser").findAll("div",{"class":"columns monthgroup"})
			div_monthgroup_divs = div_monthgroup[1].findAll("div")
		except:
			return "Error retrieving div_monthgroup_divs"

		# Gets Rust's patch url.
		try:
			self.url = "https://rust.facepunch.com" + div_monthgroup_divs[2].a["href"]
			if self.url is None:
				return "Error retrieving " + self.name + " url."
		except:
			return "Error retrieving " + self.name + " url."

		# Gets Rust's patch title.
		try:
			self.title = div_monthgroup_divs[2].a.text
			if self.title is None:
				return "Error retrieving " + self.name + " title."
		except:
			return "Error retrieving " + self.name + " title."
		
		# Gets source of Rust's current patch page.
		try:
			request = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
		except urllib.error.URLError:
			return "Couldn't connect to patch's url"

		try:
			bsoup = soup(source, "html.parser")
			div_container = bsoup.findAll("div",{"class":"container content"})
		except:
			return "Error retrieving container"
		
		# Gets Rust's patch image.
		try:
			section_style_string = bsoup.findAll("div",{"id":"content"})[0].section["style"]
			self.image = self.find_between(section_style_string, "url('", "')")
			if self.image is None:
				return "Error retrieving " + self.name + " image."
		except:
			return "Error retrieving " + self.name + " image."

		# Gets Rust's patch description.
		try:
			self.desc = div_container[0].p.text
			if self.desc is None:
				return "Error retrieving " + self.name + " description."
		except:
			return "Error retrieving " + self.name + " description."

	def find_between(self, s, first, last):
		start = s.index(first) + len(first)
		end = s.index(last, start)
		return s[start:end]