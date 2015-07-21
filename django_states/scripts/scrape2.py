#!/usr/bin/env python
import urllib
import urllib2
import StringIO
import re, sys, os

from lxml import etree

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_states.settings")

from main.models import State
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

result = urllib.urlopen("http://www.50states.com/")
html = result.read()

parser = etree.HTMLParser()
tree   = etree.parse(StringIO.StringIO(html), parser)

href_xpath = "//*[@id='ar-full-homepage']/div/ul/li/a/@href"

filtered_html = tree.xpath(href_xpath)

links = [html for html in filtered_html if 'htm' in html]

for link in links:
	state_name_pattern = "(?<=\W).*(?=.htm)"
	state_name_search = re.search(state_name_pattern, link)
	state_name = "%s" % state_name_search.group()

	state_page = urllib.urlopen("http://www.50states.com%s" % link)
	state_page_html = state_page.read()
	tree = etree.parse(StringIO.StringIO(state_page_html), parser)

	state_population_xpath = '//*[@id="collapseQuick-Facts"]/div/ul/li[6]/div/text()'
	state_population_string = tree.xpath(state_population_xpath)

	state_population_pattern = "\d+,\d+,\d+"
	cleaned_pop_string = re.search(state_population_pattern, "%s" % state_population_string)

	try:
		state_object, created = State.objects.get_or_create(name__icontains=state_name.strip('new'))
		state_object.population = cleaned_pop_string.group()
	except Exception, e:
		print e
		print "ERROR AT %s" % state_name

	state_map_link_xpath = '//*[@id="collapseGovernment"]/div/ul/li[2]/div/a/@href'
	state_map_link = tree.xpath(state_map_link_xpath)

	state_page = urllib.urlopen(state_map_link[0])
	state_page_html = state_page.read()
	tree = etree.parse(StringIO.StringIO(state_page_html), parser)

	state_map_image_xpath = '/html/body/img/@src'
	state_map_image = tree.xpath(state_map_image_xpath)

	url = 'http://quickfacts.census.gov%s' % state_map_image[0]
	image_response = urllib2.urlopen(url).read()

	img_temp = NamedTemporaryFile(delete=True)

	img_temp.write(image_response)

	state_object.state_map.save('tmpimage.gif', File(img_temp))
