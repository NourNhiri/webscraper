import click
import requests


@click.group()
def cli():
    pass



def getData(route):
    try:
        r=requests.get("http://localhost:3000/"+route)


        data=r.json()



    except requests.exceptions.JSONDecodeError as e:
        click.echo("file is leeg")
        click.echo(e)
        print(r.status_code,r.text)
        return None

    print(r.status_code,r.text)
    click.echo(data)
    return data




@click.command
@click.argument("post",type=str)
@click.argument("views",type=int)
def addPost(post,views):
    
    
    num=int(getData("volgendId")["value"])
    print(num)
    print("-----------------------")
    r=requests.post(f"http://localhost:3000/posts/",json={"id":str(num),"title":post,"views":views})

    r=requests.put("http://localhost:3000/volgendId",json={"value":str(num+1)})
    print(r.status_code)
    print(r.text)
                
              
            
           
        
    

        

  

   
    


cli.add_command(addPost) 
    



if __name__=="__main__":
    cli()