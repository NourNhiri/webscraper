import requests
from bs4 import BeautifulSoup as b
BASE_URL = "http://localhost:3000/"
from spellchecker import SpellChecker as s
from collections import Counter
import click
import re
from urllib.parse import urljoin, urlsplit
def getData(link=BASE_URL, route=""):
    """GET a url and return the JSON as Python data."""
    r = fetch(link + route)
    try:
        return r.json()
    except requests.exceptions.JSONDecodeError:
        raise click.ClickException(f"no valid JSON at {link + route}")



def fetch(url):
    """GET a url. Stop with a clean message if the request fails."""
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise click.ClickException(f"server error: {e}")
    except requests.exceptions.RequestException as e:
        raise click.ClickException(f"could not reach {url}: {e}")
    return r

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
    items=[]
    soup=b(t,"html.parser")
    if input("want a count of words?")=="y":
        
        text=re.findall(r"\w+",soup.getText(" "))
        count=Counter(text)
        items.append(count)
        print(count)
    if input("want all the links?")=="y":
        links=[]
        a=soup.find_all("a",href=True)
        for tag in a:
            
            l=urljoin(link,tag.get("href"))
            split=urlsplit(l)
            if split.scheme in ("http","https"):
                links.append(l)
        
                
        
        items.append(links)
    
    
    return items
    





