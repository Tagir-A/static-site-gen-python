import unittest

from htmlnode import HTMLNode, LeafNode


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
        node = HTMLNode(tag="div", children=[child1, child2], props={
                        "class": "container"})
        expected = "HTMLNode(tag='div', value=None, children=[HTMLNode(tag='span', value='child1', children=[], props={}), HTMLNode(tag='span', value='child2', children=[], props={})], props={'class': 'container'})"
        self.assertEqual(repr(node), expected)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_img_with_src_alt(self):
        node = LeafNode("img", "Alt text", {
                        "src": "image.jpg", "alt": "Alt text"})
        self.assertEqual(
            node.to_html(), '<img src="image.jpg" alt="Alt text">Alt text</img>')

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Some text")
        self.assertEqual(node.to_html(), "<span>Some text</span>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Content")
        self.assertEqual(node.to_html(), "<div>Content</div>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Title")
        self.assertEqual(node.to_html(), "<h1>Title</h1>")

    def test_leaf_to_html_li(self):
        node = LeafNode("li", "Item")
        self.assertEqual(node.to_html(), "<li>Item</li>")

    def test_leaf_to_html_ul(self):
        node = LeafNode("ul", "List")
        self.assertEqual(node.to_html(), "<ul>List</ul>")

    def test_leaf_to_html_ol(self):
        node = LeafNode("ol", "Ordered list")
        self.assertEqual(node.to_html(), "<ol>Ordered list</ol>")

    def test_leaf_to_html_blockquote(self):
        node = LeafNode("blockquote", "Quote")
        self.assertEqual(node.to_html(), "<blockquote>Quote</blockquote>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "print('hello')")
        self.assertEqual(node.to_html(), "<code>print('hello')</code>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_leaf_to_html_empty_tag(self):
        node = LeafNode("", "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_leaf_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_empty_value_raises(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("input", "Value", {
                        "type": "text", "name": "username", "placeholder": "Enter username"})
        self.assertEqual(node.to_html(
        ), '<input type="text" name="username" placeholder="Enter username">Value</input>')

    def test_leaf_to_html_no_props(self):
        node = LeafNode("em", "Emphasized text")
        self.assertEqual(node.to_html(), "<em>Emphasized text</em>")


if __name__ == "__main__":
    unittest.main()
