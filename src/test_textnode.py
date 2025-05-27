import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_equal_nodes(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.TEXT)
        self.assertEqual(node1, node2)

    def test_unequal_type(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_unequal_url(self):
        node1 = TextNode("Click", TextType.LINK, "http://example.com")
        node2 = TextNode("Click", TextType.LINK, "http://different.com")
        self.assertNotEqual(node1, node2)
    
    def test_repr(self):
        node = TextNode("Code sample", TextType.CODE)
        expected = "TextNode('Code sample', TextType.CODE, None)"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()
