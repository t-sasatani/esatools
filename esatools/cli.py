"""
Command line interface for esatools package.
"""

import click

from esatools.Runner import fetch_md_posts


@click.group()
def cli():
    """
    Command line interface for esatools package.
    """
    pass


@cli.command()
def fetch():
    """
    Fetch all posts from the client and return them as a list of markdown strings.
    """
    fetch_md_posts()


if __name__ == "__main__":
    cli()
