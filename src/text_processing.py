# text_processing.py
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    CODE = "code"
    BOLD = "bold"
    ITALIC = "italic"

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
            # Pass through non-text nodes unchanged
            new_nodes.append(node)
            continue
        
        text = node.text
        if text.count(delimiter) % 2 != 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {text}")
        
        parts = text.split(delimiter)
        for i, part in enumerate(parts):
            if not part:  # Skip empty parts
                continue
            if i % 2 == 0:
                # Even-indexed parts are outside delimiters (text)
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd-indexed parts are inside delimiters (code, bold, or italic)
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes