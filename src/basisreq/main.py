import click
from bs4 import BeautifulSoup as b
from .functions import *
import requests
from .requests import getData


@click.group()
def cli():
    pass

@click.command
@click.argument("post", type=str)
@click.argument("views", type=int)
def addPost(post, views):
    """add post"""
    num = int(getData(route="volgendId")["value"])

    r = requests.post(BASE_URL + "posts", json={"id": str(num), "title": post, "views": views})
    r.raise_for_status()

    r = requests.put(BASE_URL + "volgendId", json={"value": str(num + 1)})
    r.raise_for_status()

    click.echo(f"post {num} added")


@click.command
@click.argument("link", type=str,required=False)
@click.option("--depth",type=int,default=2,required=False)
@click.option("--prettify",is_flag=True,help="prints it with beautifoul soup")
@click.option("--localfile",type=click.Path(dir_okay=False,file_okay=True,exists=True),help="this option enables you to open a locally saved html file with a path")
@click.option("--findimg",is_flag=True,help="prints all scr link of every jpg image")
@click.option("--mode",type=click.Choice(["async","sync"]),default="sync",help="searches asynchrounus or syncro...")

def search(link,prettify,localfile,findimg,depth,mode):
    """show the HTML of a page"""
    if bool(link)==bool(localfile):
        raise click.UsageError("either you gave link and local file path. or you gave none try running basisreq search --help")
    
    asyncMode=mode=="async"
    
        
    if localfile:
            with open(localfile,encoding='utf-8') as f:
                t=f.read()
    else:
        t=fetch(link).text

        
    if findimg:
        for img in findJPG(b(t,'html.parser')):
            click.echo(img)
    elif prettify:
        
        click.echo(b(t,'html.parser').prettify())
   

    else:
        
        getPages(t,link,depth,asyncMode)
            


cli.add_command(addPost)
cli.add_command(search)


if __name__ == "__main__":
    cli()
    
