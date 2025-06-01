# import unittest
# #from textnode import TextNode, TextType
# from src.textnode import TextNode, TextType
# from text_to_textnodes import text_to_textnodes


# class TestTextToTextNodes(unittest.TestCase):
#     def test_mixed_markdown(self):
#         text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
#         expected = [
#             TextNode("This is ", TextType.TEXT),
#             TextNode("text", TextType.BOLD),
#             TextNode(" with an ", TextType.TEXT),
#             TextNode("italic", TextType.ITALIC),
#             TextNode(" word and a ", TextType.TEXT),
#             TextNode("code block", TextType.CODE),
#             TextNode(" and an ", TextType.TEXT),
#             TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
#             TextNode(" and a ", TextType.TEXT),
#             TextNode("link", TextType.LINK, "https://boot.dev"),
#         ]
#         result = text_to_textnodes(text)
#         self.assertEqual(result, expected)

# if __name__ == "__main__":
#     unittest.main()
import unittest
from textnode import TextNode, TextType
from markdown_parser import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_mixed_markdown(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT, None),
            TextNode("text", TextType.BOLD, None),
            TextNode(" with an ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" word and a ", TextType.TEXT, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" and an ", TextType.TEXT, None),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
