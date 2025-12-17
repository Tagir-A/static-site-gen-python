import unittest

from src.markdown_parser import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link
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
        node = TextNode("This is text with a [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_multiple_links(self):
        node = TextNode("Here are two links: [first](url1.com) and [second](url2.com)", TextType.TEXT)
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
        node = TextNode("[link with spaces](https://example.com/path with spaces) [special!@#](url&param=value)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link with spaces", TextType.LINK, "https://example.com/path with spaces"),
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
        node = TextNode("This has an ![image](url.jpg) but no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]  # Should remain unchanged since no links
        self.assertListEqual(expected, new_nodes)

    def test_split_incomplete_syntax_not_links(self):
        node = TextNode("This has [incomplete link(url.com and [another](incomplete url", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]  # Should remain unchanged since no valid links
        self.assertListEqual(expected, new_nodes)

    def test_split_nested_brackets_not_links(self):
        node = TextNode("This has [text with [nested] brackets] but no actual links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]  # Should remain unchanged since no valid links
        self.assertListEqual(expected, new_nodes)

    def test_split_mixed_images_and_links(self):
        node = TextNode("Text with ![image](img.jpg) and [link](url.com) together", TextType.TEXT)
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


if __name__ == "__main__":
    unittest.main()
