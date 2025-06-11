# # text_processing.py
# import re
# import logging
# from textnode import TextNode, TextType
# # from htmlnode import text_node_to_html_node

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     new_nodes = []
#     for node in old_nodes:
#         if node.text_type != TextType.TEXT:
#             new_nodes.append(node)
#             continue
        
#         text = node.text
#         if not text:
#             continue
        
#         if text.count(delimiter) % 2 != 0:
#             raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {text}")
        
#         parts = text.split(delimiter)
#         for i, part in enumerate(parts):
#             if not part:
#                 continue
#             if i % 2 == 0:
#                 new_nodes.append(TextNode(part, TextType.TEXT))
#             else:
#                 new_nodes.append(TextNode(part, text_type))
    
#     return new_nodes

# def split_nodes_image(old_nodes):
#     new_nodes = []
#     for node in old_nodes:
#         if node.text_type != TextType.TEXT:
#             new_nodes.append(node)
#             continue
        
#         text = node.text
#         if not text:
#             continue
        
#         pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
#         matches = list(re.finditer(pattern, text))
#         if not matches:
#             new_nodes.append(node)
#             continue
        
#         last_end = 0
#         for match in matches:
#             start, end = match.span()
#             if last_end < start:
#                 new_nodes.append(TextNode(text[last_end:start], TextType.TEXT))
#             alt_text = match.group(1)
#             url = match.group(2)
#             new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
#             last_end = end
        
#         if last_end < len(text):
#             new_nodes.append(TextNode(text[last_end:], TextType.TEXT))
    
#     return new_nodes

# def split_nodes_link(old_nodes):
#     new_nodes = []
#     for node in old_nodes:
#         if node.text_type != TextType.TEXT:
#             new_nodes.append(node)
#             continue
        
#         text = node.text
#         if not text:
#             continue
        
#         pattern = r'\[([^\]]*)\]\(([^)]+)\)'
#         matches = list(re.finditer(pattern, text))
#         if not matches:
#             new_nodes.append(node)
#             continue
        
#         last_end = 0
#         for match in matches:
#             start, end = match.span()
#             if last_end < start:
#                 new_nodes.append(TextNode(text[last_end:start], TextType.TEXT))
#             link_text = match.group(1)
#             url = match.group(2)
#             new_nodes.append(TextNode(link_text, TextType.LINK, url))
#             last_end = end
        
#         if last_end < len(text):
#             new_nodes.append(TextNode(text[last_end:], TextType.TEXT))
    
#     return new_nodes

# def markdown_to_blocks(markdown):
#     # Normalize newlines
#     markdown = markdown.replace('\r\n', '\n').replace('\r', '\n').strip()
#     # Log raw input with newlines escaped
#     logging.debug(f"Raw input markdown: {repr(markdown.replace('\n', '\\n'))}")
#     # Split on two or more newlines, ignoring surrounding whitespace
#     blocks = [block.strip() for block in re.split(r'\n\s*\n', markdown) if block.strip()]
#     logging.debug(f"Blocks produced: {blocks}")
#     return blocks

# def block_to_text_nodes(block):
#     nodes = [TextNode(block, TextType.TEXT)]
#     nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
#     nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
#     nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
#     nodes = split_nodes_image(nodes)
#     nodes = split_nodes_link(nodes)
#     return nodes

# def markdown_to_html_node(markdown):
#     blocks = markdown_to_blocks(markdown)
#     html_blocks = []
    
#     for block in blocks:
#         logging.debug(f"Processing block: {block}")
#         if re.match(r'^#{1,6}\s+\S', block):
#             level = block.count('#', 0, block.find(' '))
#             content = block.lstrip('#').strip()
#             text_nodes = block_to_text_nodes(content)
#             html_content = ''.join(node.to_html() for node in map(text_node_to_html_node, text_nodes))
#             html_blocks.append(f"<h{level}>{html_content}</h{level}>")
#             continue
        
#         if re.match(r'^\s*>', block, re.MULTILINE):
#             lines = [line.strip().lstrip('>').strip() for line in block.splitlines()]
#             content = ' '.join(lines).strip()
#             text_nodes = block_to_text_nodes(content)
#             html_content = ''.join(node.to_html() for node in map(text_node_to_html_node, text_nodes))
#             html_blocks.append(f"<blockquote>{html_content}</blockquote>")
#             continue
        
#         if re.match(r'^[-*]\s+\S', block, re.MULTILINE):
#             items = []
#             for item in block.splitlines():
#                 item = item.strip().lstrip('-*').strip()
#                 if item:
#                     item_nodes = block_to_text_nodes(item)
#                     item_html = ''.join(node.to_html() for node in map(text_node_to_html_node, item_nodes))
#                     items.append(f"<li>{item_html}</li>")
#             html_blocks.append(f"<ul>\n{'\n'.join(items)}\n</ul>")
#             continue
        
#         if re.match(r'^\d+\.\s+\S', block, re.MULTILINE):
#             items = []
#             for item in block.splitlines():
#                 item = re.sub(r'^\d+\.\s*', '', item).strip()
#                 if item:
#                     item_nodes = block_to_text_nodes(item)
#                     item_html = ''.join(node.to_html() for node in map(text_node_to_html_node, item_nodes))
#                     items.append(f"<li>{item_html}</li>")
#             html_blocks.append(f"<ol>\n{'\n'.join(items)}\n</ol>")
#             continue
        
#         if block.startswith('```') and block.endswith('```'):
#             content = block[3:-3].strip()
#             html_blocks.append(f"<pre><code>{content}</code></pre>")
#             continue
        
#         text_nodes = block_to_text_nodes(block)
#         html_content = ''.join(node.to_html() for node in map(text_node_to_html_node, text_nodes))
#         html_blocks.append(f"<p>{html_content}</p>")
    
#     logging.debug(f"HTML blocks: {html_blocks}")
#     return f"<div>{''.join(html_blocks)}</div>"