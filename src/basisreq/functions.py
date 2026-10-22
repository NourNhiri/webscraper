import requests
from bs4 import BeautifulSoup as b
BASE_URL = "http://localhost:3000/"
import click
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





