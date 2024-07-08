import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        expected = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(props={'href':'https://www.google.com','target':'_blank'})
        self.assertEqual(node.props_to_html(), expected)

    def test_leaf_node(self):
        ln1 = LeafNode("p","This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(ln1.to_html(),expected)
        ln1 = LeafNode("a","click me!",{"href":"https://www.google.com"})
        expected = '<a href="https://www.google.com">click me!</a>'
        self.assertEqual(ln1.to_html(),expected)
    def test_parent_node(self):
        node = ParentNode("p",[
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i","italic text"),
            LeafNode(None, "Normal text")
        ],)
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(),expected)
