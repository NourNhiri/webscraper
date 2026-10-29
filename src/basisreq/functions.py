
from bs4 import BeautifulSoup as b
from spellchecker import SpellChecker as s
from collections import Counter
import re
from urllib.parse import urljoin, urlsplit, urldefrag
from .requests import getData, fetch
def findJPG(html:b):
    tags=[]
    for tag in html.find_all("img"):
        
        src=tag.get("src")
        
        if src:
            src=src.partition("?")[0]
            if src.lower().endswith(".jpg"):
                tags.append(src)

    return tags


def CountLinks(t,link):
    link=[link]
    if input("want all the links? + the count?")=="y":
        res=recursiveSearch(links=link)
        print(res[0])
        print(f"we visited {res[1]} total links excluding fetch errors")
       

def countWords(soup):
    text=re.findall(r"\w+",soup.getText(" "))
    count=Counter(text)
    return count
def absoluteLinks(soup,link):
    a=soup.find_all("a",href=True)
    links=[]
    for tag in a:
        
        l=urljoin(link,tag.get("href"))
        split=urlsplit(l)
        if split.scheme in ("http","https"):
            l=urldefrag(l)[0]
            links.append(l)
    return links
    


def recursiveSearch(links,counter=None,depth=0,seen=None,totalLinks=None):
    if depth==2:return [counter,totalLinks]
    if seen==None:seen=set()
    if counter==None:counter=Counter()
    if totalLinks is None: totalLinks=[0]
    for item in links:
        if not item in seen:
            seen.add(item)
            try:
                html=fetch(item).text 
            except Exception as e:
                print(e)
            else:
                totalLinks[0]+=1
                print(f"fetched {item}")
                soup=b(html,"html.parser")
                count=countWords(soup)
                counter.update(count)
                newlinks=absoluteLinks(soup,item)
                new_dept=depth+1
                recursiveSearch(newlinks,counter,new_dept,seen,totalLinks)
    return [counter,totalLinks[0]]







