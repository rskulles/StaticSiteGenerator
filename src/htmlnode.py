
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if self.props == None:
            return ""

        s = ""
        for k,v in self.props.items():
            s += f' {k}="{v}"'
        return s
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    def to_html(self):

        if self.tag == None or self.tag == "":
            raise ValueError("Tag must be present")

        if self.children == None or len(self.children) == 0:
            raise ValueError("Children must be present")
        str = f"<{self.tag}{self.props_to_html()}>"
        for c in self.children:
            str+= c.to_html()
        str += f"</{self.tag}>"
        return str
