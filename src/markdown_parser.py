"""
import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                if part:
                    new_nodes.append(TextNode(part, text_type))
        if node.text.endswith(delimiter):
            new_nodes.append(TextNode("", TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        matches = re.finditer(r"!\[(.*?)\]\((.*?)\)", text)
        last_end = 0
        temp_nodes = []
        for match in matches:
            start, end = match.span()
            alt_text = match.group(1)
            url = match.group(2)
            if last_end < start and text[last_end:start]:
                temp_nodes.append(TextNode(text[last_end:start], TextType.TEXT))
            if alt_text or url:
                temp_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_end = end
        if last_end < len(text):
            temp_nodes.append(TextNode(text[last_end:], TextType.TEXT))
        if not matches:
            new_nodes.append(node)
        else:
            new_nodes.extend(temp_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        matches = re.finditer(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
        last_end = 0
        temp_nodes = []
        for match in matches:
            start, end = match.span()
            link_text = match.group(1)
            url = match.group(2)
            if last_end < start and text[last_end:start]:
                temp_nodes.append(TextNode(text[last_end:start], TextType.TEXT))
            if link_text or url:
                temp_nodes.append(TextNode(link_text, TextType.LINK, url))
            last_end = end
        if last_end < len(text):
            temp_nodes.append(TextNode(text[last_end:], TextType.TEXT))
        if not matches:
            new_nodes.append(node)
        else:
            new_nodes.extend(temp_nodes)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return [node for node in nodes if node.text]

"""

import re
from textnode import TextNode, TextType
from dataclasses import dataclass

@dataclass
class SplitRule:
    text_type: TextType
    delimiter: str = None
    regex_pattern: str = None
    is_delimiter: bool = False

class NodeSplitter:
    def __init__(self):
        self.rules = [
            SplitRule(TextType.IMAGE, regex_pattern=r"!\[(.*?)\]\((.*?)\)", is_delimiter=False),
            SplitRule(TextType.LINK, regex_pattern=r"(?<!\!)\[(.*?)\]\((.*?)\)", is_delimiter=False),
            SplitRule(TextType.BOLD, delimiter="**", is_delimiter=True),
            SplitRule(TextType.ITALIC, delimiter="_", is_delimiter=True),
            SplitRule(TextType.CODE, delimiter="`", is_delimiter=True),
        ]

    def split_delimiter(self, nodes, delimiter, text_type):
        new_nodes = []
        for node in nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue
            if delimiter not in node.text:
                new_nodes.append(node)
                continue
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part:
                        new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    if part:
                        new_nodes.append(TextNode(part, text_type))
            if node.text.endswith(delimiter):
                new_nodes.append(TextNode("", TextType.TEXT))
        return new_nodes

    def split_regex(self, nodes, pattern, text_type):
        new_nodes = []
        for node in nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue
            text = node.text
            matches = re.finditer(pattern, text)
            last_end = 0
            temp_nodes = []
            for match in matches:
                start, end = match.span()
                content = match.group(1)
                url = match.group(2) if len(match.groups()) > 1 else None
                if last_end < start and text[last_end:start]:
                    temp_nodes.append(TextNode(text[last_end:start], TextType.TEXT))
                if content or url:
                    temp_nodes.append(TextNode(content, text_type, url))
                last_end = end
            if last_end < len(text):
                temp_nodes.append(TextNode(text[last_end:], TextType.TEXT))
            if not matches:
                new_nodes.append(node)
            else:
                new_nodes.extend(temp_nodes)
        return new_nodes

    def split_nodes(self, text):
        nodes = [TextNode(text, TextType.TEXT)]
        for rule in self.rules:
            if rule.is_delimiter:
                nodes = self.split_delimiter(nodes, rule.delimiter, rule.text_type)
            else:
                nodes = self.split_regex(nodes, rule.regex_pattern, rule.text_type)
        return [node for node in nodes if node.text]

def text_to_textnodes(text: str) -> list[TextNode]:
    splitter = NodeSplitter()
    return splitter.split_nodes(text)
