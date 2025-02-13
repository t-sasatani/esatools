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
def backup():
    """
    Fetch all posts using the ESA API and save them as categorized markdown files.
    """
    fetch_md_posts()


if __name__ == "__main__":
    cli()
