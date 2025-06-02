# text_processing.py
from enum import Enum
import re

class TextType(Enum):
    TEXT = "text"
    CODE = "code"
    BOLD = "bold"
    ITALIC = "italic"
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
        return f"TextNode({self.text!r}, {self.text_type!r}, {self.url!r})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        if not text:  # Handle empty text
            continue
        
        if text.count(delimiter) % 2 != 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {text}")
        
        parts = text.split(delimiter)
        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        if not text:  # Handle empty text
            continue
        
        # Regex: Matches ![alt](url), capturing alt and url
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        matches = list(re.finditer(pattern, text))
        if not matches:
            new_nodes.append(node)
            continue
        
        last_end = 0
        for match in matches:
            start, end = match.span()
            if last_end < start:
                new_nodes.append(TextNode(text[last_end:start], TextType.TEXT))
            alt_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_end = end
        
        if last_end < len(text):
            new_nodes.append(TextNode(text[last_end:], TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        if not text:  # Handle empty text
            continue
        
        # Regex: Matches [text](url), capturing text and url
        pattern = r'\[([^\]]*)\]\(([^)]+)\)'
        matches = list(re.finditer(pattern, text))
        if not matches:
            new_nodes.append(node)
            continue
        
        last_end = 0
        for match in matches:
            start, end = match.span()
            if last_end < start:
                new_nodes.append(TextNode(text[last_end:start], TextType.TEXT))
            link_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            last_end = end
        
        if last_end < len(text):
            new_nodes.append(TextNode(text[last_end:], TextType.TEXT))
    
    return new_nodes

def markdown_to_blocks(markdown):
    # Split on double newlines and strip whitespace
    blocks = [block.strip() for block in markdown.split('\n\n')]
    # Remove empty blocks
    return [block for block in blocks if block]