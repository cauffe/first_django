#!/usr/bin/env python
import urllib
import urllib2
from lxml import etree
import StringIO
import re, sys, os
import requests
from PIL import Image



sys.path.append("..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_states.settings")

from main.models import State, StateCapital
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
#result = urllib.urlopen("http://164.100.47.132/LssNew/Members/Alphabaticallist.aspx")

result = urllib.urlopen("http://www.50states.com/")

html = result.read()

parser = etree.HTMLParser()
tree   = etree.parse(StringIO.StringIO(html), parser)

# xpath = "//table[@id='ctl00_ContPlaceHolderMain_Alphabaticallist1_dg1']/tr/td/img/@src"  #/child::text()

# xpath1 = "//table[@id='Table2']/tr/td/a/child::text()"

# xpath2 = "////table[@id='Table2']/tr/td/a/@href"

xpath3 = "//*[@id='ar-full-homepage']/div/ul/li/a/@href"


filtered_html3 = tree.xpath(xpath3)


links = [html for html in filtered_html3 if 'htm' in html]

print links

for link in links:
	state_name_pattern = "(?<=/)[^}]*(?=.htm)"

	state_name_search = re.search(state_name_pattern, link)

	state_name = "%s" % state_name_search.group()


	print "#### %s #####" % state_name.strip('new')


	try:
		state_object, created = State.objects.get_or_create(name__icontains=state_name.strip('new'))
	except:
		state_object = State.objects.filter(name__icontains=state_name.strip('new')).first()

	print created

	#print "http://www.50states.com/%s" % link
	state_page = urllib.urlopen("http://www.50states.com%s" % link)

	state_page_html = state_page.read()

	tree   = etree.parse(StringIO.StringIO(state_page_html), parser)

	state_population_xpath = '//*[@id="collapseQuick-Facts"]/div/ul/li[6]/div/text()'

	state_population_string = tree.xpath(state_population_xpath)
	state_population_pattern = "([\d]+),([\d]+),([\d]+)"
	cleaned_pop_string = re.search(state_population_pattern, "%s" % state_population_string)

	try:
		print cleaned_pop_string.group()
		state_object.population = "%s" % cleaned_pop_string.group()
		try:
			state_object.save()
		except:
			print state_object.name
	except AttributeError:
		print "no groups"

	state_map_link_xpath = '//*[@id="collapseGovernment"]/div/ul/li[2]/div/a/@href'
	state_map_link = tree.xpath(state_map_link_xpath)


	state_page = urllib.urlopen(state_map_link[0])

	state_page_html = state_page.read()

	tree = etree.parse(StringIO.StringIO(state_page_html), parser)

	state_map_image_link = '/html/body/img/@src'

	state_map_image = tree.xpath(state_map_image_link)


	print "STATE MAP IMAGE LINK %s" % 'http://quickfacts.census.gov%s' % state_map_image[0]

	url = 'http://quickfacts.census.gov%s' % state_map_image[0]
	image_response = urllib2.urlopen(url).read()

	img_temp = NamedTemporaryFile(delete=True)

	img_temp.write(image_response)

	state_object.state_map.save('tmpimage.gif', File(img_temp))

		# img = StringIO.StringIO(image_response)
		#img = Image.open(StringIO.StringIO(image_response.content))

		# image_file = open('temp.gif', 'wb')

		# for block in image_response.iter_content(1024):
		# 	image_file.write(block)



	# image = urllib.URLopener()
	
	# 	f = open(StringIO.StringIO(), 'wb')
	#     f.write(chunk)
	
	# 	 = f
	# 	state_object.save()

# ([\d{0,2}])(,\d{0,3})

# ^([0-9]+,)*[0-9]+$



# state_page_result = state_page.read()
# for html in filtered_html3:
# 	# if '.html' in html:
# 	print html



# print filtered_html3




