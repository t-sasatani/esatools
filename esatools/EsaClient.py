"""
Module to interact with the ESA API using the piyo library.
"""

import os
import re
from pathlib import Path

from dotenv import load_dotenv
from piyo import Client, PiyoHTTPException

from esatools.EsaUtilLogger import EsaUtilLogger
from esatools.Formatter import Formatter

logger = EsaUtilLogger().get_logger(__name__)

load_dotenv()


class EsaClient:
    """
    Class to interact with the ESA API using the piyo library.
    """

    def __init__(self):
        """
        Construct the EsaClient class.
        """
        self._access_token = None
        self._current_team = None
        self._total_posts = None
        self._temp_export_dir = None
        self._client = None

    @property
    def access_token(self) -> str:
        """
        Get the access token from the environment variables.
        """
        if self._access_token is None:
            self._access_token = os.environ.get("ESA_ACCESS_TOKEN")
        return self._access_token

    @property
    def current_team(self) -> str:
        """
        Get the current team from the environment variables.
        """
        if self._current_team is None:
            self._current_team = os.environ.get("ESA_CURRENT_TEAM")
        return self._current_team

    @property
    def temp_export_dir(self) -> Path:
        """
        Get the temporary export directory from the environment variables.
        """
        if self._temp_export_dir is None:
            self._temp_export_dir = Path(os.environ.get("ESATOOLS_EXPORT_DIR"))
            if not self._temp_export_dir.exists():
                self._temp_export_dir.mkdir(parents=True)
        return self._temp_export_dir

    @property
    def client(self) -> Client:
        """
        Get the esa client.
        """
        if self._client is None:
            self._client = Client(
                access_token=self.access_token, current_team=self.current_team
            )
        return self._client

    @property
    def total_posts(self):
        """
        Get the total number of posts in the current team.
        """
        if self._total_posts is None:
            try:
                response = self.client.posts(keywords=None, search_options={})
                self._total_posts = response.get("total_count", 0)
            except PiyoHTTPException as e:
                logger.error(f"HTTP error getting total posts: {e}")
                self._total_posts = 0
        return self._total_posts

    def export_md_posts(self, start_post_id, end_post_id):
        """
        Export posts from the current team to markdown files.
        """
        logger.info(
            f"Exporting posts from {self.current_team} to {self.temp_export_dir}"
        )
        logger.info(f"Exporting posts {start_post_id} to {end_post_id}")
        for post_id in range(start_post_id, end_post_id + 1):
            try:
                post = self.client.post(post_id)
                if not post:
                    logger.warning(f"Post ID {post_id} not found.")
                    continue

                post_md = Formatter.extract_md(post)
                post_title = post.get("name", "Untitled")
                sanitized_title = self._sanitize_filename(post_title)

                # Create nested directories based on category
                category = post.get("category", "")

                if not category:
                    category_path = self.temp_export_dir
                else:
                    category_path = self.temp_export_dir / self._sanitize_category_path(
                        category
                    )

                if not category_path.exists():
                    category_path.mkdir(parents=True)
                    logger.info(f"Created category directory: {category_path}")

                post_file_name = f"{sanitized_title}.md"
                post_file_path = category_path / post_file_name

                with open(post_file_path, "w", encoding="utf-8") as f:
                    f.write(post_md)
                logger.debug(f"Exported post {post_id} to {post_file_path}")

            except PiyoHTTPException as e:
                logger.warning(
                    f"Post ID {post_id} not found. This may be due to a deleted post or a permissions issue."
                )
                logger.debug(f"HTTP error getting post ID {post_id}: {e}")

            except Exception as e:
                logger.error(f"Unexpected error exporting post ID {post_id}: {e}")

    def _sanitize_filename(self, name):
        """
        Sanitize the post title for use as a filename.
        """
        # Replace spaces with underscores, remove invalid characters including colons
        if not name:
            return "Untitled"
        # Replace problematic characters: colons, slashes, etc.
        sanitized_name = re.sub(r'[:/\\<>*?"|]', "", name)
        return "_".join(sanitized_name.split())

    def _sanitize_category_path(self, category):
        """
        Sanitize the category for use as a directory path.
        """
        # Split category by '/', replace spaces with underscores, build the path
        # if category doesn't include '/', return the sanitized category
        if "/" not in category:
            return "_".join(category.split())
        valid_parts = ["_".join(part.split()) for part in category.split("/")]
        return Path(*valid_parts)
