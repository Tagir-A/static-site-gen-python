import unittest

from src.markdown_parser import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from src.textnode import TextNode, TextType


class TestMarkdownParser(unittest.TestCase):
    def test_split_nodes_delimiter_code_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_code_multiple(self):
        node = TextNode("Text `code1` more text `code2` end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" more text ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_multiple_nodes(self):
        nodes = [
            TextNode("First `code`", TextType.TEXT),
            TextNode("Second **bold**", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("Second **bold**", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_missing_closing(self):
        node = TextNode("Text with `unclosed code", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_singular_image(self):
        input = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        result = extract_markdown_images(input)
        self.assertEqual(result, expected)

    def test_extract_multiple_images(self):
        input = "Here are two images: ![first](url1.jpg) and ![second](url2.png)"
        expected = [("first", "url1.jpg"), ("second", "url2.png")]
        result = extract_markdown_images(input)
        self.assertEqual(result, expected)

    def test_extract_no_images(self):
        input = "This is just plain text with no images"
        expected = []
        result = extract_markdown_images(input)
        self.assertEqual(result, expected)

    def test_extract_empty_string(self):
        input = ""
        expected = []
        result = extract_markdown_images(input)
        self.assertEqual(result, expected)

    def test_extract_images_with_special_chars(self):
        input = "![image with spaces](https://example.com/image with spaces.jpg) ![special!@#](url&param=value)"
        expected = [("image with spaces", "https://example.com/image with spaces.jpg"), ("special!@#", "url&param=value")]
        result = extract_markdown_images(input)
        self.assertEqual(result, expected)

    def test_extract_adjacent_images(self):
        input = "![img1](url1.jpg)![img2](url2.png)"
        expected = [("img1", "url1.jpg"), ("img2", "url2.png")]
        result = extract_markdown_images(input)
        self.assertEqual(result, expected)

    def test_extract_images_mixed_content(self):
        input = "Text ![image](url.jpg) more text `code` and **bold** ![another](url2.png)"
        expected = [("image", "url.jpg"), ("another", "url2.png")]
        result = extract_markdown_images(input)
        self.assertEqual(result, expected)

    def test_extract_images_with_brackets(self):
        input = "![image with (parentheses)](url.jpg)"
        expected = [("image with (parentheses)", "url.jpg")]
        result = extract_markdown_images(input)
        self.assertEqual(result, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_single_link(self):
        input = "This is text with a [link](https://example.com)"
        expected = [("link", "https://example.com")]
        result = extract_markdown_links(input)
        self.assertEqual(result, expected)

    def test_extract_multiple_links(self):
        input = "Here are two links: [first](url1.com) and [second](url2.com)"
        expected = [("first", "url1.com"), ("second", "url2.com")]
        result = extract_markdown_links(input)
        self.assertEqual(result, expected)

    def test_extract_no_links(self):
        input = "This is just plain text with no links"
        expected = []
        result = extract_markdown_links(input)
        self.assertEqual(result, expected)

    def test_extract_empty_string(self):
        input = ""
        expected = []
        result = extract_markdown_links(input)
        self.assertEqual(result, expected)

    def test_extract_links_with_special_chars(self):
        input = "[link with spaces](https://example.com/path with spaces) [special!@#](url&param=value)"
        expected = [("link with spaces", "https://example.com/path with spaces"), ("special!@#", "url&param=value")]
        result = extract_markdown_links(input)
        self.assertEqual(result, expected)

    def test_extract_adjacent_links(self):
        input = "[link1](url1.com)[link2](url2.com)"
        expected = [("link1", "url1.com"), ("link2", "url2.com")]
        result = extract_markdown_links(input)
        self.assertEqual(result, expected)

    def test_extract_images_not_links(self):
        input = "This has an ![image](url.jpg) but no links"
        expected = []
        result = extract_markdown_links(input)
        self.assertEqual(result, expected)

    def test_extract_incomplete_syntax_not_links(self):
        input = "This has [incomplete link(url.com and [another](incomplete url"
        expected = []
        result = extract_markdown_links(input)
        self.assertEqual(result, expected)

    def test_extract_nested_brackets_not_links(self):
        input = "This has [text with [nested] brackets] but no actual links"
        expected = []
        result = extract_markdown_links(input)
        self.assertEqual(result, expected)

    def test_extract_mixed_images_and_links(self):
        input = "Text with ![image](img.jpg) and [link](url.com) together"
        expected = [("link", "url.com")]
        result = extract_markdown_links(input)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
