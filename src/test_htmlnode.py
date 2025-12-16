import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(tag="a", props={"href": "https://x.com"})
        self.assertEqual(node.props_to_html(), ' href="https://x.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(tag="img", props={"src": "cat.png", "alt": "cat"})
        self.assertEqual(node.props_to_html(), ' src="cat.png" alt="cat"')

    def test_repr_empty_children_props(self):
        node = HTMLNode(tag="div", value="text")
        expected = "HTMLNode(tag='div', value='text', children=[], props={})"
        self.assertEqual(repr(node), expected)

    def test_repr_with_children_and_props(self):
        child1 = HTMLNode(tag="span", value="child1")
        child2 = HTMLNode(tag="span", value="child2")
        node = HTMLNode(tag="div", children=[child1, child2], props={"class": "container"})
        expected = "HTMLNode(tag='div', value=None, children=[HTMLNode(tag='span', value='child1', children=[], props={}), HTMLNode(tag='span', value='child2', children=[], props={})], props={'class': 'container'})"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()