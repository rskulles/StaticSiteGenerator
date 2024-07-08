import re
from enum import Enum
from htmlnode import LeafNode
from htmlnode import ParentNode
from htmlnode import HTMLNode

class TextType(Enum):
    TEXT   = 1
    BOLD   = 2
    ITALIC = 3
    CODE   = 4
    LINK   = 5
    IMAGE  = 6

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING   = 2
    CODE      = 3
    QUOTE     = 4
    ULIST     = 5
    OLIST     = 6


class TextNode:
    def __init__(self, text: str, text_type: TextType, url:str=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node:TextNode)->LeafNode:
        node = None
        match text_node.text_type:
            case TextType.TEXT:
                node = LeafNode(None,text_node.text)
            case TextType.BOLD:
                node = LeafNode("b",text_node.text)
            case TextType.ITALIC:
                node = LeafNode("i",text_node.text)
            case TextType.CODE:
                node = LeafNode("code",text_node.text)
            case TextType.LINK:
                node = LeafNode("a",text_node.text,props={"href":text_node.url})
            case TextType.IMAGE:
                node = LeafNode("img","", props={"src":text_node.url,"alt":text_node.text})
            case _:
                raise ValueError(f"Unkown Value {text_node.text_type}")
        return node

def split_node_delimiter(old_nodes, delimiter,text_type:TextType):
    new_nodes =[]
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
        else:
            sections = n.text.split(delimiter)
            append_nodes =[]
            for i in range(len(sections)):
                if i%2 == 0 and sections[i] != "":
                    append_nodes.append(TextNode(sections[i],TextType.TEXT))
                else:
                    text = ""
                    url = None

                    match text_type:
                        case TextType.BOLD:
                            text=sections[i];
                        case TextType.ITALIC:
                            text=sections[i]
                        case TextType.CODE:
                            text=sections[i]
                        case _:
                            raise ValueError(f"TextType of {tex_type} is not splitable by a delimiter")

                    append_nodes.append(TextNode(text,text_type,url))
            new_nodes.extend(append_nodes)
    return new_nodes

def __split_str_image__(text,src):
    return f"![{text}]({src})"

def __split_str_link__(text,src):
    return f"[{text}]({src})"

def __split_node__(old_nodes:list[TextNode], extract_func, split_str_func, text_type:TextType)->list[TextNode]:

    new_nodes = []

    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
        else:
            append_nodes = []
            matches = extract_func(n.text)
            if len(matches) == 0:
                append_nodes.append(n)
            else:
                text = n.text
                for i in range(len(matches)):
                    match_text = matches[i][0]
                    match_uri = matches[i][1]

                    split_str = split_str_func(match_text,match_uri)
                    sections = text.split(split_str,1)

                    if sections[0] != '':
                        append_nodes.append(TextNode(sections[0],TextType.TEXT))

                    append_nodes.append(TextNode(match_text,text_type,match_uri))

                    if sections[1] != '' and i != len(matches)-1:
                        text = sections[1]
                    elif sections[1] != '':
                        append_nodes.append(TextNode(sections[1],TextType.TEXT))

            new_nodes.extend(append_nodes)
    return new_nodes

def split_node_image(old_nodes):
   return __split_node__(old_nodes, extract_markdown_images,__split_str_image__,TextType.IMAGE)

def split_node_link(old_nodes):
    return __split_node__(old_nodes,extract_markdown_links,__split_str_link__,TextType.LINK)

def extract_markdown_images(text:str):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return matches

def extract_markdown_links(text:str):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)",text)
    return matches

def text_to_textnodes(text:str)->list[TextNode]:
    node = TextNode(text,TextType.TEXT)
    new_nodes = split_node_delimiter([node],'**',TextType.BOLD)
    new_nodes = split_node_delimiter(new_nodes,'*',TextType.ITALIC)
    new_nodes = split_node_delimiter(new_nodes,'`',TextType.CODE)
    new_nodes = split_node_image(new_nodes)
    new_nodes = split_node_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown:str)->list[str]:
    blocks = []
    lines = markdown.split("\n")
    concat = False
    block_count = 0

    for i in range(len(lines)):
        line = str.strip(lines[i])
        if line =="" or str.isspace(line):
            if concat:
                block_count += 1
            concat = False
            continue
        if concat :
            blocks[block_count] = str.join("\n",[blocks[block_count],line])
        else:
            blocks.append(line)
            concat = True

    return blocks

def __is_heading__(block:str)->bool:
    r = r"^#{1,6}\s"
    matches = re.findall(r,block)
    return len(matches) != 0

def __is_code__(block:str)->bool:
    return block.startswith("```") and block.endswith("```")

def __is_quote_(block:str)->bool:
    lines = block.split("\n")
    for line in lines:
        if not line.startswith("> "):
            return False
    return True

def __is_unordered_list__(block:str)->bool:
    lines = block.split("\n")
    for line in lines:
        if not line.startswith("* ") and not line.startswith("- "):
            return False
    return True

def __is_ordered_list__(block:str)->bool:
    if not block.startswith("1. "):
        return False

    lines = block.split("\n")
    r = r"^[0-9]+?\.\s"
    previous_line = -1
    for line in lines:
        matches =   re.findall(r,line)
        if len(matches) == 0:
            return False
        if previous_line < 0:
            previous_line = int(matches[0].replace(". ",""))
            continue
        else:
            value = int(matches[0].replace(". ",""))
            if value - previous_line != 1:
                return False
            previous_line = value
    return True

def block_to_block_type(block:str)->BlockType:

    if __is_heading__(block):
        return BlockType.HEADING

    if __is_code__(block):
        return BlockType.CODE

    if __is_quote_(block):
        return BlockType.QUOTE

    if __is_unordered_list__(block):
        return BlockType.ULIST

    if __is_ordered_list__(block):
        return BlockType.OLIST

    return BlockType.PARAGRAPH

def __block_to_paragraph__(block:str)->ParentNode:
    children = []
    text_nodes = text_to_textnodes(block)
    html_nodes = list(map(text_node_to_html_node,text_nodes))
    children.extend(html_nodes)
    parent_node = ParentNode("p",children)
    return parent_node

def __block_to_heading__(block:str)->ParentNode:
    match = re.findall(r"^#{1,6}\s",block)
    heading= len(str.strip(match[0]))
    text = block.replace(match[0],'')
    children = []
    text_nodes = text_to_textnodes(text)
    html_nodes = list(map(text_node_to_html_node,text_nodes))
    children.extend(html_nodes)
    return ParentNode(f"h{heading}",children)

def __block_to_quote__(block:str)->ParentNode:
    children =[]
    for line in block.split("\n"):
        p = __block_to_paragraph__(line[2:])
        children.append(p)
    return ParentNode("blockquote",children)

def __block_to_code__(block:str)->ParentNode:
    print(f"CODE BLOCK: {block}")
    return  ParentNode("pre",[LeafNode("code",str.strip(block[3:-3]))])

def __block_to_ulist__(block:str)->ParentNode:
    list_nodes=[]
    for line in block.split("\n"):
        text_nodes = text_to_textnodes(line[2:])
        list_nodes.append(ParentNode("li",list(map(text_node_to_html_node,text_nodes))))
    return ParentNode("ul",list_nodes)

def __block_to_olist__(block:str)->ParentNode:
    list_nodes=[]
    for line in block.split("\n"):
        match = re.findall(r"^[0-9]+?\.\s",line)
        text_nodes = text_to_textnodes(line[len(match[0]):])
        list_nodes.append(ParentNode("li",list(map(text_node_to_html_node,text_nodes))))
    return ParentNode("ol",list_nodes)

def markdown_to_html_node(markdown:str)->ParentNode:
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(__block_to_paragraph__(block))
            case BlockType.HEADING:
                children.append(__block_to_heading__(block))
            case BlockType.QUOTE:
                children.append(__block_to_quote__(block))
            case BlockType.CODE:
                children.append(__block_to_code__(block))
            case BlockType.ULIST:
                children.append(__block_to_ulist__(block))
            case BlockType.OLIST:
                children.append(__block_to_olist__(block))
            case _:
                raise ValueError("Don't know BlockType: {block_type}")

    root_node = ParentNode("div", children)
    return root_node

if __name__ == "__main__":
    text = """
```
print("Lord")
print("of")
print("the")
print("rings")
```
"""
    node = markdown_to_html_node(text)
    print(node)
    print(node.to_html())
