# test_markdown_to_html_node.py
"""
import unittest
from text_processing import markdown_to_html_node
from textnode import TextType

class TestMarkdownToHTMLNode(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_quote(self):
        markdown = "> This is a quote with **bold** text"
        html = markdown_to_html_node(markdown)
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b> text</blockquote></div>",
        )

    def test_heading(self):
        markdown = "## Heading with _italic_ text"
        html = markdown_to_html_node(markdown)
        self.assertEqual(
            html,
            "<div><h2>Heading with <i>italic</i> text</h2></div>",
        )

    def test_unordered_list(self):
        markdown = "- Item 1 with `code`\n- Item 2"
        html = markdown_to_html_node(markdown)
        self.assertEqual(
            html,
            "<div><ul>\n<li>Item 1 with <code>code</code></li>\n<li>Item 2</li>\n</ul></div>",
        )

    def test_ordered_list(self):
        markdown = "1. First with [link](https://example.com)\n2. Second"
        html = markdown_to_html_node(markdown)
        self.assertEqual(
            html,
            "<div><ol>\n<li>First with <a href=\"https://example.com\">link</a></li>\n<li>Second</li>\n</ol></div>",
        )

    def test_code_block(self):
        markdown = "```\nfunction example() {}\n```"
        html = markdown_to_html_node(markdown)
        self.assertEqual(
            html,
            "<div><pre><code>function example() {}</code></pre></div>",
        )

    def test_paragraph(self):
        markdown = "Paragraph with ![image](https://example.com/img.png)"
        html = markdown_to_html_node(markdown)
        self.assertEqual(
            html,
            "<div><p>Paragraph with <img src=\"https://example.com/img.png\" alt=\"image\"></p></div>",
        )

    def test_mixed_blocks(self):
        markdown = """
# Heading
# > Quote with **bold**
# - List item
# """
#         html = markdown_to_html_node(markdown)
#         self.assertEqual(
#             html,
#             "<div><h1>Heading</h1><blockquote>Quote with <b>bold</b></blockquote><ul>\n<li>List item</li>\n</ul></div>",
#         )

#     def test_empty_markdown(self):
#         markdown = ""
#         html = markdown_to_html_node(markdown)
#         self.assertEqual(html, "<div></div>")

# if __name__ == "__main__":
#     unittest.main()
# """