import click

from esa_tools.Runner import fetch_md_posts

@click.group()
def cli():
    pass


@cli.command()
def fetch():
    fetch_md_posts()

if __name__ == '__main__':
    cli()