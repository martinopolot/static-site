# test_text_processing.py
import unittest
from text_processing import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link, markdown_to_blocks

class TestSplitNodesDelimiter(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # Show full diff in test failures

    def test_single_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_italic_delimiter(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = TextNode("Text with `code1` and `code2` blocks", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" blocks", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_non_text_node(self):
        node = TextNode("Code block", TextType.CODE)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("Code block", TextType.CODE)]
        self.assertEqual(result, expected)

    def test_mixed_nodes(self):
        nodes = [
            TextNode("This is `code` here", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More **bold** text", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is `code` here", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = []
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("Plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("Plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter(self):
        node = TextNode("Text with `unclosed code", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(cm.exception), "Unmatched delimiter '`' in text: Text with `unclosed code")

    def test_delimiter_at_start(self):
        node = TextNode("`code` at start", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_delimiter_at_end(self):
        node = TextNode("Text with `code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiter_types(self):
        node = TextNode("This is `code` and **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        result = split_nodes_delimiter(result, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_single_image(self):
        node = TextNode("An ![image](https://i.imgur.com/zjjcJKZ.png) only", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("An ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" only", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_at_start(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) text", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_at_end(self):
        node = TextNode("Text with ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(result, expected)

    def test_no_images(self):
        node = TextNode("Plain text", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("Plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_non_text_node_image(self):
        node = TextNode("Code block", TextType.CODE)
        result = split_nodes_image([node])
        expected = [TextNode("Code block", TextType.CODE)]
        self.assertEqual(result, expected)

    def test_empty_text_image(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_image([node])
        expected = []
        self.assertEqual(result, expected)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(result, expected)

    def test_single_link(self):
        node = TextNode("A [link](https://www.example.com) only", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(" only", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_link_at_start(self):
        node = TextNode("[link](https://www.example.com) text", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_link_at_end(self):
        node = TextNode("Text with [link](https://www.example.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
        ]
        self.assertEqual(result, expected)

    def test_no_links(self):
        node = TextNode("Plain text", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("Plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_non_text_node_link(self):
        node = TextNode("Code block", TextType.CODE)
        result = split_nodes_link([node])
        expected = [TextNode("Code block", TextType.CODE)]
        self.assertEqual(result, expected)

    def test_empty_text_link(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_link([node])
        expected = []
        self.assertEqual(result, expected)

    def test_mixed_nodes_image_and_link(self):
        nodes = [
            TextNode("Text with ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            TextNode("Code", TextType.CODE),
            TextNode("Text with [link](https://www.example.com)", TextType.TEXT),
        ]
        result = split_nodes_image(nodes)
        result = split_nodes_link(result)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("Code", TextType.CODE),
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
        ]
        self.assertEqual(result, expected)

    # New tests for markdown_to_blocks
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
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

    def test_single_block(self):
        md = "# Heading"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading"])

    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_excessive_newlines(self):
        md = """
Paragraph 1



Paragraph 2

  

- List item 1
- List item 2


"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph 1",
                "Paragraph 2",
                "- List item 1\n- List item 2",
            ],
        )

    def test_different_block_types(self):
        md = """
# Heading

This is a paragraph.

- List item 1
- List item 2
"""
if __name__ == "__main__":
    unittest.main()