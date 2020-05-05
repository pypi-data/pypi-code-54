"""
    This module contains the sub-commands of umbrella sites.
"""

import click
import requests
from requests.auth import HTTPBasicAuth

from umbrella_cli.services import ManagementApiService, ApiError
from umbrella_cli.models import Site

@click.group()
@click.pass_context
def sites(ctx):
    pass


@sites.command(name="get-all")
@click.pass_context
def get_all(ctx):
    """ Get the list of sites """
    api = ManagementApiService(
        access=ctx.obj["ACCESS"], 
        secret=ctx.obj["SECRET"], 
        org_id=ctx.obj["ORG"]
    )
    
    try:
        sites = api.get_sites()

        click.echo("""
+===============================================+
|+++ Umbrella Sites for Organization {org} +++|
|===============================================|
| Site ID | Name                                |
|-----------------------------------------------|""".format(org=ctx.obj['ORG'])
        )
        for site in sites:
            click.echo("| {:8}| {:36}|".format(str(site.site_id), site.name))
        
        click.echo("+===============================================+")

    except ApiError as error:
        click.secho(str(error), fg="red")

@sites.command()
@click.argument("name")
@click.pass_context
def create(ctx, name):
    """ Create a new site """
    api = ManagementApiService(
        access=ctx.obj["ACCESS"], 
        secret=ctx.obj["SECRET"], 
        org_id=ctx.obj["ORG"]
    )

    try:
        site = Site(name)

        result = api.create_site(site)

        click.secho("New site created with ID {id}".format(id=result.site_id),
                    fg="green")
    except ApiError as error:
        click.secho(str(error), fg="red")

    