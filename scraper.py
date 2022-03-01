import requests
import re
from bs4 import BeautifulSoup
import sqlite3 as sql

#------------Start of general stuff (valid for all programs) ---------------#

webpage = requests.get("https://www.dr-chuck.com/")
#print(webpage.status_code)
#print(webpage.headers)

source = webpage.content
soup = BeautifulSoup(source,'html.parser')  #Returns a soup object
links = soup.find_all("a")
#print(links)

#--------------End of general stuff-----------------------------------------#

webpage_stuff = dict() #We will dump link.text as key and the link as value into the dictionary

for link in links :
    count = 1
    if re.search('^\s$',link.text) or len(link.text)<=1 or not (link.text.isprintable()) or "'" in link.text:     #If the link.text is not a pure text, we take care of it
        key_list = re.findall('^\S+?\.(\S+?)\.\S+$',link.attrs['href'])  #Generating key from the url using some serious RegEx
        if(len(key_list)==0):
            key_list.append("chuck_stuff"+str(count))
            count=count+1

    else:
        key_list[0] = link.text

    key_actual = key_list[0]
    webpage_stuff[key_actual] = link.attrs['href']  #Storing stuff into the dictionary with the text as keyprint(webpage_stuff)

#Time to store our hard-earned data into our "personal database"
conn = sql.connect('Chuck.db')
db_cursor = conn.cursor()

for key_iterative,url_iterative in webpage_stuff.items():
    cmd = "INSERT INTO chuck VALUES(\'" + key_iterative + "\',\'" + url_iterative + "\')"
    db_cursor.execute(cmd)
conn.commit()
conn.close()

