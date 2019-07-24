import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

class Overwatch():

	def __init__(self):
		self.name = "Overwatch"
		self.names = ["overwatch"]
		self.patch = {"title": None, "url": None, "desc": None, "image": None}
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
			self.patch["title"] = side_div[0].ul.li.h3.text
			if self.patch["title"] is None:
				raise Exception("Could not find " + self.name + " title.")
		except:
			raise Exception("Error retrieving " + self.name + " title.")

		# Gets Overwatch's patch url.
		try:
			self.patch["url"] = "https://playoverwatch.com/en-us/news/patch-notes/pc/" + side_div[0].ul.li.a["href"]
			if self.patch["url"] is None:
				raise Exception("Could not find " + self.name + " url.")
		except:
			raise Exception("Error retrieving " + self.name + " url.")

		# Gets Overwatch's patch image.
		try:
			heading_image_div = bsoup.findAll("div",{"class":"HeadingBanner"})
			self.patch["image"] = self.find_between(heading_image_div[0]["style"], "url(", ")")
			if self.patch["image"] is None:
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
			self.patch["desc"] = desc
			if self.patch["desc"] is "":
				raise Exception("Could not find " + self.name + " description.")
		except:
			raise Exception("Error retrieving " + self.name + " description.")

	def find_between(self, s, first, last):
		start = s.index(first) + len(first)
		end = s.index(last, start)
		return s[start:end]
