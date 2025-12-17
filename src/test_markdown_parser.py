import unittest

from src.markdown_parser import extract_markdown_images, extract_markdown_links, markdown_to_blocks, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


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

    def test_extract_multiple_same_images(self):
        input = "Here are two images: ![first](url1.jpg) and ![first](url1.jpg)"
        expected = [("first", "url1.jpg"), ("first", "url1.jpg")]
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
        expected = [("image with spaces", "https://example.com/image with spaces.jpg"),
                    ("special!@#", "url&param=value")]
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
        expected = [("link with spaces", "https://example.com/path with spaces"),
                    ("special!@#", "url&param=value")]
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


class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE,
                     "https://i.imgur.com/aKaOqIh.gif"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_multiple_images(self):
        node = TextNode(
            "Here are two images: ![first](url1.jpg) and ![second](url2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Here are two images: ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "url1.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "url2.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_no_images(self):
        node = TextNode(
            "This is just plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [node]
        self.assertListEqual(expected, new_nodes)

    def test_split_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [node]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_with_special_chars(self):
        node = TextNode(
            "![image with spaces](https://example.com/image with spaces.jpg) ![special!@#](url&param=value)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image with spaces", TextType.IMAGE,
                     "https://example.com/image with spaces.jpg"),
            TextNode(" ", TextType.TEXT),
            TextNode("special!@#", TextType.IMAGE, "url&param=value"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_adjacent_images(self):
        node = TextNode("![img1](url1.jpg)![img2](url2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("img1", TextType.IMAGE, "url1.jpg"),
            TextNode("img2", TextType.IMAGE, "url2.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_mixed_content(self):
        node = TextNode(
            "Text ![image](url.jpg) more text `code` and **bold** ![another](url2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url.jpg"),
            TextNode(" more text `code` and **bold** ", TextType.TEXT),
            TextNode("another", TextType.IMAGE, "url2.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_with_brackets(self):
        node = TextNode("![image with (parentheses)](url.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image with (parentheses)", TextType.IMAGE, "url.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("First ![image1](url1.jpg)", TextType.TEXT),
            TextNode("Second ![image2](url2.jpg)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "url1.jpg"),
            TextNode("Second ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "url2.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_at_start(self):
        node = TextNode("![start image](url.jpg) and some text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("start image", TextType.IMAGE, "url.jpg"),
            TextNode(" and some text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_at_end(self):
        node = TextNode("Some text and ![end image](url.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Some text and ", TextType.TEXT),
            TextNode("end image", TextType.IMAGE, "url.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_only_image(self):
        node = TextNode("![only image](url.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("only image", TextType.IMAGE, "url.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)


class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode(
            "This is text with a [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_multiple_links(self):
        node = TextNode(
            "Here are two links: [first](url1.com) and [second](url2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Here are two links: ", TextType.TEXT),
            TextNode("first", TextType.LINK, "url1.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.LINK, "url2.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_no_links(self):
        node = TextNode("This is just plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]
        self.assertListEqual(expected, new_nodes)

    def test_split_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_with_special_chars(self):
        node = TextNode(
            "[link with spaces](https://example.com/path with spaces) [special!@#](url&param=value)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link with spaces", TextType.LINK,
                     "https://example.com/path with spaces"),
            TextNode(" ", TextType.TEXT),
            TextNode("special!@#", TextType.LINK, "url&param=value"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_adjacent_links(self):
        node = TextNode("[link1](url1.com)[link2](url2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link1", TextType.LINK, "url1.com"),
            TextNode("link2", TextType.LINK, "url2.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_not_links(self):
        node = TextNode(
            "This has an ![image](url.jpg) but no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]  # Should remain unchanged since no links
        self.assertListEqual(expected, new_nodes)

    def test_split_incomplete_syntax_not_links(self):
        node = TextNode(
            "This has [incomplete link(url.com and [another](incomplete url", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]  # Should remain unchanged since no valid links
        self.assertListEqual(expected, new_nodes)

    def test_split_nested_brackets_not_links(self):
        node = TextNode(
            "This has [text with [nested] brackets] but no actual links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]  # Should remain unchanged since no valid links
        self.assertListEqual(expected, new_nodes)

    def test_split_mixed_images_and_links(self):
        node = TextNode(
            "Text with ![image](img.jpg) and [link](url.com) together", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text with ![image](img.jpg) and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(" together", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("First [link1](url1.com)", TextType.TEXT),
            TextNode("Second [link2](url2.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1.com"),
            TextNode("Second ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_at_start(self):
        node = TextNode("[start link](url.com) and some text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("start link", TextType.LINK, "url.com"),
            TextNode(" and some text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_at_end(self):
        node = TextNode("Some text and [end link](url.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Some text and ", TextType.TEXT),
            TextNode("end link", TextType.LINK, "url.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_only_link(self):
        node = TextNode("[only link](url.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("only link", TextType.LINK, "url.com"),
        ]
        self.assertListEqual(expected, new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes_basic(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_empty_string(self):
        text = ""
        expected = []
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_plain_text(self):
        text = "This is just plain text with no markdown"
        expected = [
            TextNode("This is just plain text with no markdown", TextType.TEXT)]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_only_bold(self):
        text = "**bold text**"
        expected = [TextNode("bold text", TextType.BOLD)]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_only_italic(self):
        text = "_italic text_"
        expected = [TextNode("italic text", TextType.ITALIC)]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_only_code(self):
        text = "`code block`"
        expected = [TextNode("code block", TextType.CODE)]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_only_image(self):
        text = "![alt text](https://example.com/image.jpg)"
        expected = [TextNode("alt text", TextType.IMAGE,
                             "https://example.com/image.jpg")]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_only_link(self):
        text = "[link text](https://example.com)"
        expected = [TextNode("link text", TextType.LINK,
                             "https://example.com")]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_multiple_bold(self):
        text = "**first** and **second** bold"
        expected = [
            TextNode("first", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
            TextNode(" bold", TextType.TEXT),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_multiple_italic(self):
        text = "_first_ and _second_ italic"
        expected = [
            TextNode("first", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.ITALIC),
            TextNode(" italic", TextType.TEXT),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_multiple_code(self):
        text = "`first` and `second` code"
        expected = [
            TextNode("first", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.CODE),
            TextNode(" code", TextType.TEXT),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_multiple_images(self):
        text = "![first](url1.jpg) and ![second](url2.png)"
        expected = [
            TextNode("first", TextType.IMAGE, "url1.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "url2.png"),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_multiple_links(self):
        text = "[first](url1.com) and [second](url2.com)"
        expected = [
            TextNode("first", TextType.LINK, "url1.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.LINK, "url2.com"),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_adjacent_bold_italic(self):
        text = "**bold**_italic_"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_adjacent_code_blocks(self):
        text = "`code1``code2`"
        expected = [
            TextNode("code1", TextType.CODE),
            TextNode("code2", TextType.CODE),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_adjacent_images_links(self):
        text = "![img](url.jpg)[link](url.com)"
        expected = [
            TextNode("img", TextType.IMAGE, "url.jpg"),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_special_chars_in_content(self):
        text = "**bold!@#** _italic$%^_ `code&*()` ![img!@#](url.jpg) [link$%^](url.com)"
        expected = [
            TextNode("bold!@#", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic$%^", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code&*()", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("img!@#", TextType.IMAGE, "url.jpg"),
            TextNode(" ", TextType.TEXT),
            TextNode("link$%^", TextType.LINK, "url.com"),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_elements_at_start(self):
        text = "**bold** at start"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" at start", TextType.TEXT),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_elements_at_end(self):
        text = "at end **bold**"
        expected = [
            TextNode("at end ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_empty_alt_text(self):
        text = "![](url.jpg)"
        expected = [
            TextNode("", TextType.IMAGE, "url.jpg"),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_urls_with_special_chars(self):
        text = "![img](https://example.com/path?param=value&other=123) [link](url&special=chars)"
        expected = [
            TextNode("img", TextType.IMAGE,
                     "https://example.com/path?param=value&other=123"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url&special=chars"),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_complex_mixed(self):
        text = "**bold** _italic_ `code` ![img](url.jpg) [link](url.com) plain text"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url.jpg"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(" plain text", TextType.TEXT),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)

    def test_text_to_text_nodes_processing_order(self):
        # Test that processing order is: bold -> italic -> code -> images -> links
        text = "**_bold italic_** `code` ![img](url.jpg) [link](url.com)"
        expected = [
            # Bold processed first, then italic removes underscores
            TextNode("bold italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url.jpg"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(expected, text_nodes)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
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


if __name__ == "__main__":
    unittest.main()
