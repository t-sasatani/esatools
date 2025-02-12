import os
import logging

from dotenv import load_dotenv
from pathlib import Path

import re
from piyo import Client
from piyo import PiyoHTTPException

from esatools.EsaUtilLogger import EsaUtilLogger
from esatools.Formatter import Formatter

logger = EsaUtilLogger(name=__name__).get_logger()

load_dotenv()
class EsaClient:
    def __init__(self):
        self._access_token = None
        self._current_team = None
        self._total_posts = None
        self._temp_export_dir = None
        self._client = None

    @property
    def access_token(self)->str:
        if self._access_token is None:
            self._access_token = os.environ.get('ESA_ACCESS_TOKEN')
        return self._access_token
    
    @property
    def current_team(self)->str:
        if self._current_team is None:
            self._current_team = os.environ.get('ESA_CURRENT_TEAM')
        return self._current_team
    
    @property
    def temp_export_dir(self)->Path:
        if self._temp_export_dir is None:
            self._temp_export_dir = Path(os.environ.get('ESATOOLS_EXPORT_DIR'))
            if not self._temp_export_dir.exists():
                self._temp_export_dir.mkdir(parents=True)
        return self._temp_export_dir
    
    @property
    def client(self)->Client:
        if self._client is None:
            self._client = Client(
                access_token=self.access_token,
                current_team=self.current_team)
        return self._client
    
    @property
    def total_posts(self):
        if self._total_posts is None:
            response = self.client.posts(keywords=None, search_options={})
            self._total_posts = response.get('total_count', 0)
        return self._total_posts
    
    def export_md_posts(self):
        logging.info(f"Exporting {self.total_posts} posts...")
        for post_id in range(1, self.total_posts+1):
            try:
                post = self.client.post(post_id)
                if not post:
                    logging.warning(f"Post ID {post_id} not found.")
                    continue

                post_md = Formatter.extract_md(post)
                post_title = post.get('name', 'Untitled')
                sanitized_title = self._sanitize_filename(post_title)

                # Create nested directories based on category
                category = post.get('category', '')
                category_path = self.temp_export_dir / self._sanitize_category_path(category)

                if not category_path.exists():
                    category_path.mkdir(parents=True)
                    logging.info(f"Created category directory: {category_path}")

                post_file_name = f"{post_id}_{sanitized_title}.md"
                post_file_path = category_path / post_file_name

                with open(post_file_path, 'w', encoding='utf-8') as f:
                    f.write(post_md)
                logging.info(f"Exported post {post_id} to {post_file_path}")

            except PiyoHTTPException as e:
                logging.error(f"HTTP error exporting post ID {post_id}: {e}")

            except Exception as e:
                logging.error(f"Unexpected error exporting post ID {post_id}: {e}")

    def _sanitize_filename(self, name):
        # Replace spaces with underscores, remove invalid characters including colons
        if not name:
            return "Untitled"
        # Replace problematic characters: colons, slashes, etc.
        sanitized_name = re.sub(r'[:/\\<>*?"|]', '', name)
        return "_".join(sanitized_name.split())

    def _sanitize_category_path(self, category):
        # Split category by '/', replace spaces with underscores, build the path
        valid_parts = ["_".join(part.split()) for part in category.split('/')]
        return Path(*valid_parts)
