# test_text_processing.py

"""
import unittest
import re
from text_processing import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link, markdown_to_blocks, blocks_to_html

class TestTextProcessing(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    # Existing tests (abridged)
    def test_empty_text_link(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_link([node])
        expected = []
        self.assertEqual(result, expected)

    def test_empty_text_image(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_image([node])
        expected = []
        self.assertEqual(result, expected)

    def test_markdown_to_blocks(self):
        md = """
# This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line

# - This is a list
# - with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    # New tests for blocks_to_html
    def test_heading_blocks(self):
        blocks = [
            "# Heading 1",
            "## Heading 2",
            "###### Heading 6",
        ]
        result = blocks_to_html(blocks)
        expected = [
            "<h1>Heading 1</h1>",
            "<h2>Heading 2</h2>",
            "<h6>Heading 6</h6>",
        ]
        self.assertEqual(result, expected)

    def test_quote_block(self):
        blocks = [
            "> This is a quote\n> with multiple lines",
        ]
        result = blocks_to_html(blocks)
        expected = [
            "<blockquote>This is a quote with multiple lines</blockquote>",
        ]
        self.assertEqual(result, expected)

    def test_unordered_list_block(self):
        blocks = [
            "- Item 1\n- Item 2\n- Item 3",
            "* Star item\n* Another item",
        ]
        result = blocks_to_html(blocks)
        expected = [
            "<ul>\n<li>Item 1</li>\n<li>Item 2</li>\n<li>Item 3</li>\n</ul>",
            "<ul>\n<li>Star item</li>\n<li>Another item</li>\n</ul>",
        ]
        self.assertEqual(result, expected)

    def test_ordered_list_block(self):
        blocks = [
            "1. First item\n2. Second item\n3. Third item",
        ]
        result = blocks_to_html(blocks)
        expected = [
            "<ol>\n<li>First item</li>\n<li>Second item</li>\n<li>Third item</li>\n</ol>",
        ]
        self.assertEqual(result, expected)

    def test_code_block(self):
        blocks = [
            "```\nfunction example() {}\n```",
        ]
        result = blocks_to_html(blocks)
        expected = [
            "<pre><code>function example() {}</code></pre>",
        ]
        self.assertEqual(result, expected)

    def test_paragraph_block(self):
        blocks = [
            "This is a paragraph with **bold** text.",
        ]
        result = blocks_to_html(blocks)
        expected = [
            "<p>This is a paragraph with **bold** text.</p>",
        ]
        self.assertEqual(result, expected)

    def test_mixed_blocks(self):
        blocks = [
            "# Heading",
            "> Quote here",
            "- List item 1\n- List item 2",
            "```\nCode\n```",
            "Plain paragraph",
        ]
        result = blocks_to_html(blocks)
        expected = [
            "<h1>Heading</h1>",
            "<blockquote>Quote here</blockquote>",
            "<ul>\n<li>List item 1</li>\n<li>List item 2</li>\n</ul>",
            "<pre><code>Code</code></pre>",
            "<p>Plain paragraph</p>",
        ]
        self.assertEqual(result, expected)

    def test_empty_block(self):
        blocks = []
        result = blocks_to_html(blocks)
        expected = []
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
"""