
from bs4 import BeautifulSoup as b
from spellchecker import SpellChecker as s
from collections import Counter
import re
from urllib.parse import urljoin, urlsplit, urldefrag
from .requests import getData, fetch
import asyncio
import aiohttp
from click import ClickException
def findJPG(html:b):
    """Return the src of every .jpg image in the soup, without the query string."""
    tags=[]
    for tag in html.find_all("img"):
        
        src=tag.get("src")
        
        if src:
            src=src.partition("?")[0]
            if src.lower().endswith(".jpg"):
                tags.append(src)

    return tags


            

        
    
def handleSoup(totalLinks,counter,t,depth,link):
    """Process the HTML of one page: update the page total and word counter, return its links and the next depth."""
    totalLinks[0]+=1
    print(f"fetched {link}")
    soup=b(t,"html.parser")
    count=countWords(soup)
    counter.update(count)
    newlinks=absoluteLinks(soup,link)
    new_dept=depth+1
    return newlinks,new_dept


def getPages(t,link,depth,mode):
    """Crawl from link and print the result: async if mode is True, otherwise sync after asking the user."""
    link=[link]
    if mode:
       count=asyncio.run(asSearch(link,Max=depth))
       print(count)
       return
    if input("want all the links? + the count?")=="y":
        res=recursiveSearch(links=link,Max=depth)
        print(res[0])
        print(f"we visited {res[1]} total links excluding fetch errors")
       

def countWords(soup):
    """Return a Counter of all words in the text of the soup."""
    text=re.findall(r"\w+",soup.getText(" "))
    count=Counter(text)
    return count
def absoluteLinks(soup,link):
    """Return the http and https links in the soup as absolute urls without fragment, skipping invalid ones."""
    a=soup.find_all("a",href=True)
    links=[]
    for tag in a:
        try:
            l=urljoin(link,tag.get("href"))
        except ValueError as e:
            print(f"could not join links {e}")
            continue
            
        split=urlsplit(l)
        if split.scheme in ("http","https"):
            l=urldefrag(l)[0]
            links.append(l)
    return links
    
async def runLinks(link,totalLinks,counter,depth,seen,Max):
    """Fetch one link with aiohttp, process the page and crawl its links; on a failed fetch print the error and skip it."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(link) as r:
                r.raise_for_status()
                t=await r.text()
                newlinks,new_dept=handleSoup(totalLinks,counter,t,depth,link)
                await asSearch(newlinks,counter,new_dept,seen,totalLinks,Max)
        except aiohttp.ClientError as e:
            print(e)
        except TimeoutError as e:
            print(e)
        except UnicodeError as e:
            print(f"geen inhoud gekregen {e}")

def recursiveSearch(links,counter=None,depth=0,seen=None,totalLinks=None,Max=2):
    """Crawl links one by one, recursively up to depth Max, and return the word counter and the page total."""
    if depth==Max:return [counter,totalLinks]
    if seen==None:seen=set()
    if counter==None:counter=Counter()
    if totalLinks is None: totalLinks=[0]
    for item in links:
        if not item in seen:
            seen.add(item)
            try:
                html=fetch(item).text 
            except ClickException as e:
                print(e)
            else:
                newlinks,new_dept=handleSoup(totalLinks,counter,html,depth,item)
                recursiveSearch(newlinks,counter,new_dept,seen,totalLinks,Max)
    return [counter,totalLinks[0]]



async def asSearch(links,counter=None,depth=0,seen=None,totalLinks=None,Max=2):
    """Crawl links concurrently with asyncio.gather, recursively up to depth Max, and return the word counter and the page total."""
    if depth==Max:return [counter,totalLinks]
    if seen==None:seen=set()
    if counter==None:counter=Counter()
    if totalLinks is None: totalLinks=[0]
    tasks=[]
    for link in links:
        if link not in seen:
            seen.add(link)
            tasks.append(runLinks(link,totalLinks,counter,depth,seen,Max))
    await asyncio.gather(*tasks)

    return [counter,totalLinks[0]]



