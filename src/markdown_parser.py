import re
from src.textnode import TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    old_text_type = old_nodes[0].text_type
    result = []
    for old_node in old_nodes:
        blocks = old_node.text.split(delimiter)
        if len(blocks) % 2 == 0:
            raise Exception("Closing delimiter missing")
        count = 0
        for block in blocks:
            if block:  # skip empty blocks
                if count % 2 == 0:
                    node = TextNode(block, old_text_type)
                    result.append(node)
                else:
                    node = TextNode(block, text_type)
                    result.append(node)
            count += 1

    return result


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\]]*)\]\(([^)]*)\)", text)
    return matches
