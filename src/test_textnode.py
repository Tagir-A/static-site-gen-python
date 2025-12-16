import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_all_text_types(self):
        for text_type in TextType:
            with self.subTest(text_type=text_type):
                url = None
                if text_type in (TextType.LINK, TextType.IMAGE):
                    url = "https://example.com"
                node = TextNode("Same text", text_type, url)
                node2 = TextNode("Same text", text_type, url)
                self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("text one", TextType.BOLD)
        node2 = TextNode("text two", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("shared text", TextType.BOLD)
        node2 = TextNode("shared text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("link", TextType.LINK, "https://example.com")
        node2 = TextNode("link", TextType.LINK, "https://example.org")
        self.assertNotEqual(node, node2)

    def test_not_eq_none_url_vs_set(self):
        node = TextNode("code", TextType.CODE)
        node2 = TextNode("code", TextType.CODE, "https://example.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
