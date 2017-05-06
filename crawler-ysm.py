from bs4 import BeautifulSoup # documentation available at : #www.crummy.com/software/BeautifulSoup/bs4/doc/
from BeautifulSoup import NavigableString, Tag
import requests # To send http requests and access the page : docs.python-requests.org/en/latest/
import csv # To create the output csv file
import unicodedata # To work with the string encoding of the data

entries = []
entry = []
urlnumber = 0 # Give the page number to start with

while urlnumber<25: # Give the page number to end with

    #print type(urlnumber), urlnumber
    #Give the url of the forum, excluding the page number in the hyperlink
    recordNum = urlnumber * 12 #each page holds 12 rows of data, increment by this amount
    print recordNum
    url = 'http://ysm-austin.org/index.php?option=com_ysm&object=search&task=practitioner&type=search&f_type=geography%2Cservice_setting%2Ccounty%2CProgramandOrgBoth&filter_by_miles=10&filter_by_zip=78664&county_check_rem=-1&filter_by_county=1%2C2%2C4%2C+&filter_by_ssetting=1%2C2%2C3&filter_by_programtype=1%2C2%2C3&filter_by_semesteroffered=1%2C3%2C5&countyname1=1&countyname2=2&countyname4=4&searchtype=practitioner&stage_ids=-1&stage_id=-1&skill_id=-1&sm_id=-1&ProgramandOrgBoth=ProgramandOrgBoth&service_category=-1&search__=on&z_codes_=78664&sdistrict=---+Please+Select+---&showmiles=on&miles=10&searchnow=1&submits=Search&limitstart=%d' % (urlnumber,)
    print url


    try:
        r = requests.get(url, timeout = 10) #Sending a request to access the page
    except Exception,e:
        break

    data = r.text

    soup = BeautifulSoup(data, "html.parser") # Getting the page source into the soup

    for div in soup.find_all('div'):
        entry = []
        if(div.get('class') != None and div.get('class')[0] == 'Comment'): # A single post is referred to as a comment. Each comment is a block denoted in a div tag which has a class called comment.
            ps = div.find_all('p') #gets all the tags called p to a variable ps
            aas = div.find_all('a') # gets all the tags called a to a variable aas
            spans = div.find_all('span') #
            times = div.find_all('time') # used to extract the time tage which gives the iDate of the post

            concat_str = ''
            for str in aas[1].contents: # prints the contents that is between the tag start and end
                if str != "<br>" or str != "<br/>": # This denotes breaks in post which we need to work around.
                    concat_str = (concat_str + ' '+ str.encode('iso-8859-1')).strip() # The encoding is because the format exracted is a unicode. We need a uniform structure to work with the strings.
            entry.append(concat_str)

            concat_str = ''
            for str in times[0].contents:
                if str != "<br>" or str != "<br/>":
                    concat_str = (concat_str + ' '+ str.encode('iso-8859-1')).strip()
            entry.append(concat_str)

            #print "-------------------------"
            for div in div.find_all('div'):
                if (div != None and div.get('class') != None and div.get('class')[0] == 'Message'): # Extracting the div tag witht the class attribute as message.
                    blockqoutes = []
                    x = div.get_text()
                    #print "message: " + x

                    #remove any emojis in the text
                    #for img in div.find_all('img', {'class' : 'emoji'} ):
                      #  print "found emoji img: "
                        #img.decompose()
                        #print "---decomposed---"

                    for bl in div.find_all('blockquote'):
                        blockqoutes.append(bl.get_text()) #Block quote is used to get the quote made by a person. get text helps to elimiate the hyperlinks and pulls out only the data.
                        bl.decompose()


                    if  not x:
                        print "string is empty"
                    else:
                        #print "message: " + x
                        entry.append(x.replace("\n"," ").replace("<br/>","").encode('ascii','replace').encode('iso-8859-1'))


                    for bl in blockqoutes:
                        #print bl
                        entry.append(bl.replace("\n"," ").replace("<br/>","").encode('ascii','replace').encode('iso-8859-1'))

                #print entry
            entries.append(entry)

    urlnumber = urlnumber + 1 # increment so that we can extract the next page

with open('edmunds_extraction.csv', 'w') as output:
    writer = csv.writer(output, delimiter= ',', lineterminator = '\n')
    writer.writerows(entries)
print "Wrote to edmunds_extraction.csv"

