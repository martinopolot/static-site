"""
from htmlnode import HTMLNode
from textnode import TextNode, TextType
from block_to_block_type import BlockType, block_to_block_type
from markdown_parser import text_to_textnodes
import re

def split_markdown_blocks(markdown: str) -> list[str]:
    if not markdown:
        return []
    blocks = [block.strip() for block in markdown.split('\n\n') if block.strip()]
    return blocks

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    if text_node.text_type == TextType.TEXT:
        return HTMLNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return HTMLNode(tag="b", children=[HTMLNode(tag=None, value=text_node.text)])
    elif text_node.text_type == TextType.ITALIC:
        return HTMLNode(tag="i", children=[HTMLNode(tag=None, value=text_node.text)])
    elif text_node.text_type == TextType.CODE:
        return HTMLNode(tag="code", children=[HTMLNode(tag=None, value=text_node.text)])
    elif text_node.text_type == TextType.LINK:
        return HTMLNode(tag="a", children=[HTMLNode(tag=None, value=text_node.text)], props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return HTMLNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unknown text type: {text_node.text_type}")

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def handle_heading_block(block: str) -> HTMLNode:
    match = re.match(r'^(#{1,6})\s(.+)$', block)
    if not match:
        raise ValueError("Invalid heading format")
    level = len(match.group(1))
    text = match.group(2)
    return HTMLNode(tag=f"h{level}", children=text_to_children(text))

def handle_code_block(block: str) -> HTMLNode:
    if not (block.startswith('```') and block.endswith('```')):
        raise ValueError("Invalid code block format")
    code_content = block[3:-3].strip()
    text_node = TextNode(code_content, TextType.TEXT)
    code_node = text_node_to_html_node(text_node)
    return HTMLNode(tag="pre", children=[HTMLNode(tag="code", children=[code_node])])

def handle_quote_block(block: str) -> HTMLNode:
    lines = [line[1:].strip() if line.startswith('>') else line for line in block.split('\n')]
    text = ' '.join(lines).strip()
    return HTMLNode(tag="blockquote", children=text_to_children(text))

def handle_unordered_list_block(block: str) -> HTMLNode:
    lines = block.split('\n')
    children = []
    for line in lines:
        if line == '-':
            children.append(HTMLNode(tag="li", children=[]))
        elif line.startswith('- '):
            children.append(HTMLNode(tag="li", children=text_to_children(line[2:])))
    return HTMLNode(tag="ul", children=children)

def handle_ordered_list_block(block: str) -> HTMLNode:
    lines = block.split('\n')
    children = []
    for line in lines:
        match = re.match(r'^(\d+)\.\s(.+)$', line)
        if match:
            children.append(HTMLNode(tag="li", children=text_to_children(match.group(2))))
    return HTMLNode(tag="ol", children=children)

def block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
    if block_type == BlockType.PARAGRAPH:
        return HTMLNode(tag="p", children=text_to_children(block))
    elif block_type == BlockType.HEADING:
        return handle_heading_block(block)
    elif block_type == BlockType.CODE:
        return handle_code_block(block)
    elif block_type == BlockType.QUOTE:
        return handle_quote_block(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return handle_unordered_list_block(block)
    elif block_type == BlockType.ORDERED_LIST:
        return handle_ordered_list_block(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = split_markdown_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block, block_type)
        block_nodes.append(block_node)
    return HTMLNode(tag="div", children=block_nodes)
"""

import re
from htmlnode import HTMLNode
from textnode import TextNode, TextType
from block_to_block_type import BlockType, block_to_block_type
from markdown_parser import text_to_textnodes

def split_markdown_blocks(markdown: str) -> list[str]:
    if not markdown:
        return []
    # Normalize newlines and strip leading/trailing whitespace
    markdown = markdown.strip().replace('\r\n', '\n')
    blocks = []
    current_block = []
    in_code_block = False
    lines = markdown.split('\n')

    for line in lines:
        stripped_line = line.strip()
        # Handle code block start/end
        if stripped_line.startswith('```'):
            if in_code_block:
                # End of code block
                current_block.append(stripped_line)
                blocks.append('\n'.join(current_block))
                current_block = []
                in_code_block = False
            else:
                # Start of code block
                if current_block:
                    # Check if current_block is a list
                    block_text = '\n'.join(current_block) if all(line.startswith('- ') or line == '-' or not line.strip() for line in current_block) else ' '.join(current_block).strip()
                    blocks.append(block_text)
                    current_block = []
                in_code_block = True
                current_block.append(stripped_line)
        elif in_code_block:
            # Preserve lines in code block
            current_block.append(line)
        elif not stripped_line and not current_block:
            # Skip empty lines at the start of a block
            continue
        elif not stripped_line:
            # End of a non-code block
            if current_block:
                # Check if current_block is a list
                block_text = '\n'.join(current_block) if all(line.startswith('- ') or line == '-' or line.startswith('\d+\.\s') or not line.strip() for line in current_block) else ' '.join(current_block).strip()
                blocks.append(block_text)
                current_block = []
        else:
            current_block.append(stripped_line)

    if current_block:
        # Check if final block is a list
        block_text = '\n'.join(current_block) if all(line.startswith('- ') or line == '-' or line.startswith('\d+\.\s') or not line.strip() for line in current_block) else ' '.join(current_block).strip()
        blocks.append(block_text)

    return [block for block in blocks if block]

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    if text_node.text_type == TextType.TEXT:
        return HTMLNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return HTMLNode(tag="b", children=[HTMLNode(tag=None, value=text_node.text)])
    elif text_node.text_type == TextType.ITALIC:
        return HTMLNode(tag="i", children=[HTMLNode(tag=None, value=text_node.text)])
    elif text_node.text_type == TextType.CODE:
        return HTMLNode(tag="code", children=[HTMLNode(tag=None, value=text_node.text)])
    elif text_node.text_type == TextType.LINK:
        return HTMLNode(tag="a", children=[HTMLNode(tag=None, value=text_node.text)], props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return HTMLNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unknown text type: {text_node.text_type}")

def text_to_children(text: str) -> list[HTMLNode]:
    # Collapse multiple spaces and newlines
    text = ' '.join(text.split())
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def handle_heading_block(block: str) -> HTMLNode:
    match = re.match(r'^(#{1,6})\s*(.*)$', block)
    if not match:
        raise ValueError("Invalid heading format")
    level = len(match.group(1))
    text = match.group(2).strip()
    return HTMLNode(tag=f"h{level}", children=text_to_children(text) if text else [])

def handle_code_block(block: str) -> HTMLNode:
    if not (block.startswith('```') and block.endswith('```')):
        raise ValueError("Invalid code block format")
    # Preserve internal newlines, remove only ``` markers
    code_content = block[3:-3]
    text_node = TextNode(code_content, TextType.TEXT)
    code_node = text_node_to_html_node(text_node)
    return HTMLNode(tag="pre", children=[HTMLNode(tag="code", children=[code_node])])

def handle_quote_block(block: str) -> HTMLNode:
    lines = [line[1:].strip() if line.startswith('>') else line.strip() for line in block.split('\n')]
    content = ' '.join(line for line in lines if line)
    return HTMLNode(tag="blockquote", children=text_to_children(content) if content else [])

def handle_unordered_list_block(block: str) -> HTMLNode:
    lines = block.split('\n')
    children = []
    for line in lines:
        if line == '-':
            children.append(HTMLNode(tag="li", children=[HTMLNode(tag=None, value="")]))
        elif line.startswith('- '):
            children.append(HTMLNode(tag="li", children=text_to_children(line[2:])))
    return HTMLNode(tag="ul", children=children)

def handle_ordered_list_block(block: str) -> HTMLNode:
    lines = block.split('\n')
    children = []
    for line in lines:
        match = re.match(r'^\d+\.\s(.+)$', line)
        if match:
            children.append(HTMLNode(tag="li", children=text_to_children(match.group(1))))
    return HTMLNode(tag="ol", children=children)

def block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
    if block_type == BlockType.PARAGRAPH:
        return HTMLNode(tag="p", children=text_to_children(block))
    elif block_type == BlockType.HEADING:
        return handle_heading_block(block)
    elif block_type == BlockType.CODE:
        return handle_code_block(block)
    elif block_type == BlockType.QUOTE:
        return handle_quote_block(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return handle_unordered_list_block(block)
    elif block_type == BlockType.ORDERED_LIST:
        return handle_ordered_list_block(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = split_markdown_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block, block_type)
        block_nodes.append(block_node)
    return HTMLNode(tag="div", children=block_nodes)