from esatools.EsaClient import EsaClient
from esatools.EsaUtilLogger import EsaUtilLogger

logger = EsaUtilLogger().get_logger(name=__name__)

def fetch_md_posts():
    """
    Fetches all posts from the client and returns them as a list of markdown strings.
    """
    client = EsaClient()
    end_post_id = client.total_posts
    logger.info(f"Fetching posts from {client.current_team}")
    client.export_md_posts(
        start_post_id=1, end_post_id=end_post_id
    )