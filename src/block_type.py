from enum import Enum

import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    if not block:
        return BlockType.PARAGRAPH
    if re.match(r'^#{1,6}\s', block):
        return BlockType.HEADING
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    lines = block.split('\n')
    if not lines:
        return BlockType.PARAGRAPH
    if all(line.startswith('>') for line in lines if line):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines if line):
        return BlockType.UNORDERED_LIST
    if lines and all(line for line in lines):
        ordered_pattern = re.compile(r'^(\d+)\.\s')
        expected_number = 1
        for line in lines:
            match = ordered_pattern.match(line)
            if not match or int(match.group(1)) != expected_number:
                return BlockType.PARAGRAPH
            expected_number += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
