"""
Formatter class for extracting markdown content from post data.
"""


class Formatter:
    """
    Formatter class for extracting markdown content from post data.
    """

    @staticmethod
    def extract_md(post_data):
        """
        Extract markdown content from post data.

        Parameters
        ----------
        post_data : dict
            The post data dictionary.

        Returns
        -------
        str
            The markdown content.

        """
        markdown_content = post_data.get("body_md", None)

        if markdown_content is None:
            return "Markdown content not found."

        return markdown_content
