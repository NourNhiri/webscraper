import requests
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
        r = requests.get(url, timeout=15)
        r.raise_for_status()
    except requests.Timeout as e:
        raise click.ClickException(f"time out error for {url} : {e}")
    except requests.exceptions.HTTPError as e:
        raise click.ClickException(f"server error: {e}")
    except requests.exceptions.RequestException as e:
        raise click.ClickException(f"could not reach {url}: {e}")
    
    return r
