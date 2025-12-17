from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code_text"
    QUOTE = "q"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def block_to_block_type(block):
    lines = block.split('\n')

    # Code blocks (check first and last lines)
    if len(lines) >= 2 and lines[0].strip() == '```' and lines[-1].strip() == '```':
        return BlockType.CODE

    # Headings (single line only)
    if len(lines) == 1:
        line = lines[0]
        if line.startswith('#'):
            count = 0
            for char in line:
                if char == '#':
                    count += 1
                else:
                    break
            if 1 <= count <= 6 and len(line) > count and line[count] == ' ':
                return BlockType.HEADING

    # Quote blocks
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE

    # Unordered lists
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered lists
    ordered_pattern = True
    for i, line in enumerate(lines, 1):
        if not line.strip().startswith(f"{i}. "):
            ordered_pattern = False
            break
    if ordered_pattern:
        return BlockType.ORDERED_LIST

    # Default to paragraph
    return BlockType.PARAGRAPH
