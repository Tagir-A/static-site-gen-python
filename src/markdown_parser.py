import re
from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for old_node in old_nodes:
        blocks = old_node.text.split(delimiter)
        if len(blocks) % 2 == 0:
            raise Exception("Closing delimiter missing")
        count = 0
        for block in blocks:
            if block:  # skip empty blocks
                if count % 2 == 0:
                    node = TextNode(block, old_node.text_type)
                    result.append(node)
                else:
                    node = TextNode(block, text_type)
                    result.append(node)
            count += 1

    return result


def split_nodes_image(old_nodes):
    result = []
    for old_node in old_nodes:
        blocks = extract_markdown_images(old_node.text)
        if len(blocks) == 0:
            result.append(old_node)
            continue
        remainder = old_node.text
        for block in blocks:
            alt_text = block[0]
            url = block[1]
            sections = remainder.split(f"![{alt_text}]({url})", 1)
            remainder = sections[1]
            if sections[0] != "":
                new_node = TextNode(sections[0], text_type=TextType.TEXT)
                result.append(new_node)
            image_node = TextNode(alt_text, TextType.IMAGE, url)
            result.append(image_node)
        if remainder != "":
            last_node = TextNode(remainder, text_type=TextType.TEXT)
            result.append(last_node)
    return result


def split_nodes_link(old_nodes):
    result = []
    for old_node in old_nodes:
        blocks = extract_markdown_links(old_node.text)
        if len(blocks) == 0:
            result.append(old_node)
            continue
        remainder = old_node.text
        for block in blocks:
            alt_text = block[0]
            url = block[1]
            sections = remainder.split(f"[{alt_text}]({url})", 1)
            remainder = sections[1]
            if sections[0] != "":
                new_node = TextNode(sections[0], text_type=TextType.TEXT)
                result.append(new_node)
            image_node = TextNode(alt_text, TextType.LINK, url)
            result.append(image_node)
        if remainder != "":
            last_node = TextNode(remainder, text_type=TextType.TEXT)
            result.append(last_node)
    return result


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    images = split_nodes_image(code)
    links = split_nodes_link(images)
    return links


def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        trimmed = block.strip()
        if trimmed:
            result.append(trimmed)
    return result


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\]]*)\]\(([^)]*)\)", text)
    return matches
