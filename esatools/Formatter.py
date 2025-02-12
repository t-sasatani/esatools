"""
Formatter class for extracting markdown content from post data.
"""

class Formatter:
    @staticmethod
    def extract_md(post_data):
        markdown_content = post_data.get('body_md', None)
        
        if markdown_content is None:
            return "Markdown content not found."
        
        return markdown_content
