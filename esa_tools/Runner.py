from esa_tools.EsaClient import EsaClient

def fetch_md_posts():
    """
    Fetches all posts from the client and returns them as a list of markdown strings.
    """
    client = EsaClient()
    client.export_md_posts()