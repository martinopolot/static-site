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
