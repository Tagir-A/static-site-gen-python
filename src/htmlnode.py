class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        result = ""
        for prop in self.props:
            result += f" {prop}=\"{self.props[prop]}\""
        return result

    def __repr__(self):
        children = self.children if self.children is not None else []
        props = self.props if self.props is not None else {}
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={children!r}, props={props!r})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
