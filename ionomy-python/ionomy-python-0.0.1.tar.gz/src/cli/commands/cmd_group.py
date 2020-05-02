import click
from controller import APP
from controller.reddit.classes import RedditScraper, RedditReDB
from controller.reddit.functions import get_subs_to_scrape
    

@click.group()
def cli():
    """ Run Reddit Related Scripts"""
    pass

@click.command()
def ping():
    """ Expand Reddit Meme Database for a Subreddit into the Future """

    print('pong')

    return None

cli.add_command(ping)
