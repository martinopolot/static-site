from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter
from markdown_utils import extract_markdown_images, extract_markdown_links

from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)

    def __repr__(self):
        return f"TextNode({repr(self.text)}, {self.text_type}, {repr(self.url)})"


"""
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    # Apply splitters in specific order
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # Now extract and replace links
    final_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            final_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)
        images = extract_markdown_images(text)

        # Skip if no links or images found
        if not links and not images:
            final_nodes.append(node)
            continue

        i = 0
        while i < len(text):
            matched = False

            # Images first
            for alt, url in images:
                markdown = f"![{alt}]({url})"
                if text[i:].startswith(markdown):
                    final_nodes.append(TextNode(alt, TextType.IMAGE, url))
                    i += len(markdown)
                    matched = True
                    break
            if matched:
                continue

            # Links next
            for anchor, url in links:
                markdown = f"[{anchor}]({url})"
                if text[i:].startswith(markdown):
                    final_nodes.append(TextNode(anchor, TextType.LINK, url))
                    i += len(markdown)
                    matched = True
                    break
            if matched:
                continue

            # Regular character
            j = i
            while j < len(text) and text[j] != "!" and text[j] != "[":
                j += 1
            if i != j:
                final_nodes.append(TextNode(text[i:j], TextType.TEXT))
            i = j

    return final_nodes

"""