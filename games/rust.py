import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

class Rust():

	def __init__(self):
		self.name = "Rust"
		self.names = ["rust"]
		self.patch = {"title": None, "url": None, "desc": None, "image": None}
		self.color = 13517355
		self.thumbnail = "https://i.imgur.com/WWZIaE8.jpg"

	def get_patch_info(self):

		# Gets source of Facepunch's blog.
		try:
			request = Request("https://rust.facepunch.com/blog/", headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
		except:
			raise Exception("Couldn't connect to " + self.name + "'s website.")

		# Gets divs in the monthgroup div
		try:
			div_monthgroup = soup(source, "html.parser").findAll("div",{"class":"columns monthgroup"})
			div_monthgroup_divs = div_monthgroup[1].findAll("div")
		except:
			raise Exception("Error retrieving div_monthgroup_divs")

		# Gets Rust's patch url.
		try:
			self.patch["url"] = "https://rust.facepunch.com" + div_monthgroup_divs[2].a["href"]
			if self.patch["url"] is None:
				raise Exception("Could not find " + self.name + " url.")
		except:
			raise Exception("Error retrieving " + self.name + " url.")

		# Gets Rust's patch title.
		try:
			self.patch["title"] = div_monthgroup_divs[2].a.text
			if self.patch["title"] is None:
				raise Exception("Could not find " + self.name + " title.")
		except:
			raise Exception("Error retrieving " + self.name + " title.")

		# Gets source of Rust's current patch page.
		try:
			request = Request(self.patch["url"], headers={'User-Agent': 'Mozilla/5.0'})
			source = urlopen(request).read()
		except urllib.error.URLError:
			raise Exception("Couldn't connect to patch's url")

		try:
			bsoup = soup(source, "html.parser")
			div_container = bsoup.findAll("div",{"class":"container content"})
		except:
			raise Exception("Error retrieving container")

		# Gets Rust's patch image.
		try:
			section_style_string = bsoup.findAll("div",{"id":"content"})[0].section["style"]
			self.patch["image"] = self.find_between(section_style_string, "url('", "')")
			if self.patch["image"] is None:
				raise Exception("Could not find " + self.name + " image.")
		except:
			raise Exception("Error retrieving " + self.name + " image.")

		# Gets Rust's patch description.
		try:
			self.patch["desc"] = div_container[0].p.text
			if self.patch["desc"] is None:
				raise Exception("Could not find " + self.name + " description.")
		except:
			raise Exception("Error retrieving " + self.name + " description.")

	def find_between(self, s, first, last):
		start = s.index(first) + len(first)
		end = s.index(last, start)
		return s[start:end]
