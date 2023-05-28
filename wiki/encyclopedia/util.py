import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import markdown2

# from django.conf import settings
# settings.configure(DEBUG=True)


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(
        sorted(re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md"))
    )


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title, to_html=True):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        markdown_content = f.read().decode("utf-8")
        if not to_html:
            return markdown_content
        html_content = markdown2.markdown(markdown_content)
        return html_content
    except FileNotFoundError:
        return None