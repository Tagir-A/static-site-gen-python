from pathlib import Path
import shutil
from blocknode import BlockType, block_to_block_type
from markdown_parser import markdown_to_blocks, text_to_textnodes
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def main():
    test = TextNode("hello", TextType.LINK, "https://www.boot.dev")
    print(test)
    copy_static()
    generate_page('./content/index.md', './template.html',
                  './public/index.html')
    # print(f"{None}")


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Invalid TextType {text_node.text_type}")


def text_nodes_to_html_nodes(text_nodes):
    result = []
    for text_node in text_nodes:
        node = text_node_to_html_node(text_node)
        result.append(node)
    return result


def markdown_to_html_node(markdown):
    root = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                line = block
                count = 0
                for char in line:
                    if char == '#':
                        count += 1
                    else:
                        break
                text = line[count+1:]
                text_nodes = text_to_textnodes(text)
                html_nodes = text_nodes_to_html_nodes(text_nodes)
                node = ParentNode(f"h{count}", html_nodes)
                root.children.append(node)

            case BlockType.QUOTE:
                node = ParentNode('blockquote', [])
                lines = block.split('\n')
                stripped = []
                for line in lines:
                    stripped.append(line.removeprefix('> '))

                text_nodes = text_to_textnodes("\n".join(stripped))
                html_nodes = text_nodes_to_html_nodes(text_nodes)
                node.children.extend(html_nodes)
                root.children.append(node)

            case BlockType.ORDERED_LIST:
                node = ParentNode('ol', [])
                lines = block.split('\n')
                for line in lines:
                    stripped = line[3:]
                    text_nodes = text_to_textnodes(stripped)
                    html_nodes = text_nodes_to_html_nodes(text_nodes)
                    html_node = ParentNode('li', html_nodes)
                    node.children.append(html_node)
                root.children.append(node)

            case BlockType.UNORDERED_LIST:
                node = ParentNode('ul', [])
                lines = block.split('\n')
                for line in lines:
                    stripped = line.removeprefix('- ')
                    text_nodes = text_to_textnodes(stripped)
                    html_nodes = text_nodes_to_html_nodes(text_nodes)
                    html_node = ParentNode('li', html_nodes)
                    node.children.append(html_node)
                root.children.append(node)

            case BlockType.CODE:
                lines = block.split('\n')
                stripped_lines = lines[1:-1]
                text = "\n".join(stripped_lines) + "\n"
                text_node = TextNode(text, TextType.TEXT)
                html_node = text_node_to_html_node(text_node)
                node = ParentNode('pre', [ParentNode("code", [html_node])])
                root.children.append(node)

            case BlockType.PARAGRAPH:
                lines = block.split('\n')
                line = " ".join(lines)
                node = ParentNode('p', [])

                text_nodes = text_to_textnodes(line)
                html_nodes = text_nodes_to_html_nodes(text_nodes)
                node.children.extend(html_nodes)

                root.children.append(node)
            case _:
                text_nodes = text_to_textnodes(block)
                html_nodes = text_nodes_to_html_nodes(text_nodes)
                node = ParentNode('div', html_nodes)
                root.children.append(node)

    return root


def extract_title(markdown):
    blocks = markdown.split("\n\n")
    maybe_title = blocks[0]
    if not maybe_title.startswith("# "):
        raise Exception("Invalid Title")
    title = maybe_title.removeprefix("# ")
    stripped = title.strip()
    return stripped


def copy_static():
    clear_dir("./public")
    copy_dir_contents('./static', './public')


def clear_dir(path: str | Path) -> None:
    print(Path(path).resolve())
    p = Path(path)
    if not p.is_dir():
        raise ValueError(f"{p} is not a directory")

    for item in p.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def generate_page(from_path, template_path, dest_path):
    src = Path(from_path)
    dest = Path(dest_path)
    template = Path(template_path)
    print(
        f"Generating page from {src.resolve()} to {dest.resolve()} using {template.resolve()}")
    markdown = src.read_text()
    template_file = template.read_text()
    title = extract_title(markdown)
    template_file = template_file.replace("{{ Title }}", title)
    content = markdown_to_html_node(markdown)
    # print(f"content {template_file}")
    content_string = content.to_html()
    template_file = template_file.replace("{{ Content }}", content_string)
    dest.write_text(template_file)


def generate_pages(dir_path_content, template_path, dest_dir_path):
    src = Path(dir_path_content)
    dest = Path(dest_dir_path)
    template = Path(template_path)
    for item in src.iterdir():
        if item.is_dir():
            generate_pages(item, template_path, dest_dir_path)
        else:
            generate_page(item, template_path, dest_dir_path)


def copy_dir_contents(src: str | Path, dst: str | Path) -> None:
    src = Path(src)
    print(f"src{src.resolve()}")
    dst = Path(dst)
    print(f"dst{dst.resolve()}")

    if not src.is_dir():
        raise ValueError(f"{src} is not a directory")
    dst.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


main()
