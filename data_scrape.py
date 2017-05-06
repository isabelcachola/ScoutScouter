'''
This code currently takes in data from the GS calender. It still needs to
scrape individual events pages for levels and location
'''
from lxml import html
import requests
import re
import json
from bs4 import BeautifulSoup

# Scrapes the main calender
def calender_scrape():
  page = requests.get('http://www.gsctx.org/en/events/event-calendar.html')
  tree = html.fromstring(page.content)
  full_calender =  tree.xpath('//div[@id="fullcalendar"]/following-sibling::script/text()')
  p = re.compile('calendarDisplay\(.+,(\[.*\])\);')
  st = p.findall(str(full_calender))
  json_data = json.loads(st[0].decode("unicode_escape"))

  for event in json_data: # Convert the color code to a topic and add topic key
    topic = convert_color(event['color'])
    event['topic'] = topic
    #levels = event_scrape('http://www.gsctx.org' + event['path'])
  #pretty_print(json_data)

def convert_color(num):
  num_dic = {'#854400':'Camps',
            '#000000':'STEM',
            '#EC008B':'Girl Programs',
            '#00AE5':'Girl Programs/Outdoor',
            '#00AAE5':'Outdoors',
            '#004E99':'Service Unit Events',
            '#F36F27':'Training',
            '#EB008C':'Girl Programs',
            '#B2D234':'Travel and Destinations',
            '#FDDC00':'Awards',
            '#00AE58':'Council Events',
            '#EC008C':'Girl Programs',
            '#F36F21':'Training'}
  try:
    return(num_dic[num])
  except KeyError:
    print('Color code', num, 'not recognized.')
    return('Other')
# This function should return appropriate levels for each event and the
# description
def event_scrape(path):
  levels = ['Daisy', 'Brownie', 'Cadette', 'Senior', 'Ambassador']
  try:
    page = requests.get(path)
    tree = html.fromstring(page.content)
    content = tree.xpath('//meta.text()')
    content = tree.xpath('//div[@id="main"]/div[@class="eventListDetail"]/div[@class="small-24"][2]/div[@class="small-16"][2]/text()')
  except:
    print(path)


def pretty_print(lst):
    for event in lst:
        print(event)


calender_scrape()
