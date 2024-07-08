import unittest

from textnode import TextNode
from textnode import TextType
from textnode import split_node_delimiter
import textnode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", "bold", "https://google.com")
        node2 = TextNode("This is a text node", "bold", "https://google.com")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node also", "bold")
        self.assertNotEqual(node, node2)

    def test_neq2(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_neq3(self):
        node = TextNode("This is a text node", "bold", "https://google.com")
        node2 = TextNode("This is a text node", "bold", "https://yahoo.com")
        self.assertNotEqual(node, node2)
    def test_to_html(self):

        text_node = TextNode("Normal Text",TextType.TEXT)
        expected_text = "Normal Text"

        bold_node = TextNode("Bold Text",TextType.BOLD)
        expected_bold = "<b>Bold Text</b>"

        italic_node = TextNode("Italic Text",TextType.ITALIC)
        expected_italic = "<i>Italic Text</i>"

        code_node = TextNode("Code Text",TextType.CODE)
        expected_code = "<code>Code Text</code>"

        link_node = TextNode("Link Text",TextType.LINK, "https://google.com")
        expected_link ='<a href="https://google.com">Link Text</a>'

        img_node = TextNode("Alt Text",TextType.IMAGE, "./my_cool_image.png")
        expected_img = '<img src="./my_cool_image.png" alt="Alt Text"></img>'

        self.assertEqual(expected_text, textnode.text_node_to_html_node(text_node).to_html())
        self.assertEqual(expected_bold, textnode.text_node_to_html_node(bold_node).to_html())
        self.assertEqual(expected_italic, textnode.text_node_to_html_node(italic_node).to_html())
        self.assertEqual(expected_code, textnode.text_node_to_html_node(code_node).to_html())
        self.assertEqual(expected_link, textnode.text_node_to_html_node(link_node).to_html())
        self.assertEqual(expected_img, textnode.text_node_to_html_node(img_node).to_html())

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_node_delimiter([node],'`',TextType.CODE)
        self.assertEqual(len(new_nodes),3)
        self.assertEqual(new_nodes[0].text,"This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text,"code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

        self.assertEqual(new_nodes[2].text," word")
        self.assertEqual(new_nodes[2].text_type,TextType.TEXT)
    def test_markdown_to_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.
This is the same paragraph on a new line

* This is a list
* with items"""
        blocks = textnode.markdown_to_blocks(markdown)
        self.assertEqual(len(blocks),3)
        self.assertEqual(blocks[0],"# This is a heading")
        self.assertEqual(blocks[1],"This is a paragraph of text. It has some **bold** and *italic* words inside of it.\nThis is the same paragraph on a new line")
        self.assertEqual(blocks[2],"* This is a list\n* with items")
    def test_block_to_block_type(self):
        blocks = [
            "This is a paragraph.\nIt is on two lines.",
            "# This is a heading",
            "```This is a code block;\nsudo apt do something cool;```",
            ">A quote\n>Some more quote.",
            "- unordered list item 1\n- unordered list item 2",
            "1. ordered list item 1\n2. ordered list item 2",
        ]
        self.assertEqual(textnode.block_to_block_type(blocks[0]),textnode.BlockType.PARAGRAPH)
        self.assertEqual(textnode.block_to_block_type(blocks[1]),textnode.BlockType.HEADING)
        self.assertEqual(textnode.block_to_block_type(blocks[2]),textnode.BlockType.CODE)
        self.assertEqual(textnode.block_to_block_type(blocks[3]),textnode.BlockType.QUOTE)
        self.assertEqual(textnode.block_to_block_type(blocks[4]),textnode.BlockType.ULIST)
        self.assertEqual(textnode.block_to_block_type(blocks[5]),textnode.BlockType.OLIST)

if __name__ == "__main__":
    unittest.main()
