from lxml import html
import requests
import re
import json

def calender_scrape():
  page = requests.get('http://www.gsctx.org/en/events/event-calendar.html')
  tree = html.fromstring(page.content)
  full_calender =  tree.xpath('//div[@id="fullcalendar"]/following-sibling::script/text()')
  m = re.search('calendarDisplay\(.+,(\[.*\])\);', str(full_calender))
  if m:
    st = m.group(1)
  json_data = json.load(st)
  print(json_data)


def eventscrape(page):
  pass

def main():
  calender_scrape()
main()
