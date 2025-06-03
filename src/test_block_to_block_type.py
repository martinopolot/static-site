import unittest
from block_to_block_type import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Subheading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Deep Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Too Many"), BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```code```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\ncode here"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("``````"), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\nLine 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("> Line 1\n>\n> Line 2"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("-Item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- Item 1\nNot a list"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- Item 1\n-\n- Item 2"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item 1\n3. Item 3"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("2. Item 1\n3. Item 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.Item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("a. Item"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Not a # heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```incomplete code"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Not > a quote"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
