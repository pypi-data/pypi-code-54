import click
    

@click.group()
def cli():
    """ Group of Commands """
    pass

@click.command()
def ping(sub):
    """ test cli """
    print("pong")
    return None

cli.add_command(ping)