import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node, TextNode, TextType
from node_delimiters import text_to_textnode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        if not block:
            continue
        blocks.append(block.strip())
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnode(text)
    leaf_children = []
    for text_node in text_nodes:
        leaf_children.append(text_node_to_html_node(text_node))
    return leaf_children
    
def list_to_elements(text, block_type):
    elements = []
    if block_type == BlockType.ORDERED_LIST:
        arr_text = text.split("\n")
        i = 1
        for text in arr_text:
            children = text_to_children(text.replace(f"{i}. ", ""))
            elements.append(ParentNode("li", children))
            i += 1
        
    if block_type == BlockType.UNORDERED_LIST:
        for el in text.split("- "):
            if not el:
                continue
            children = text_to_children(el.replace("\n", ""))
            elements.append(ParentNode("li", children))
    return elements
        
def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    block_nodes = []

    # TODO only for 
    # paragraph +
    # code -
    # heading -

    for block in markdown_blocks:
        if not block:
            continue
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            children = text_to_children(block)
            block_nodes.append(ParentNode("p", children))
        
        if block_type == BlockType.CODE:
            block = block[4:-3]
            block_nodes.append(ParentNode("pre", [LeafNode("code", block)]))
        
        if block_type == BlockType.HEADING:
            count = 0
            while block[count] == "#":
                count += 1
            # cut '#n ' from start    
            block = block[count+1:]
            
            children = text_to_children(block)
            block_nodes.append(ParentNode(f"h{count}", children))
        
        if block_type == BlockType.QUOTE:
            arr_quote_text = block.split("\n")
            quote_text = ""
            for i in range(len(arr_quote_text)):
                if i == 0:
                    quote_text += arr_quote_text[i][2:]
                else:
                    quote_text += arr_quote_text[i][1:]
            children = text_to_children(quote_text)
            block_nodes.append(ParentNode("blockquote", children))

        if block_type == BlockType.UNORDERED_LIST:
            children = list_to_elements(block, block_type)
            block_nodes.append(ParentNode("ul", children))

        if block_type == BlockType.ORDERED_LIST:
            children = list_to_elements(block, block_type)    
            block_nodes.append(ParentNode("ol", children))
    
    return ParentNode("div", block_nodes)




    # for block in markdown_blocks:
    #     if not block:
    #         continue
    #     block_type = block_to_block_type(block)
    #     if block_type != BlockType.CODE:
    #         text_nodes = text_to_children(block)
    #     if block_type == BlockType.CODE:
    #         text_nodes = [TextNode(block, TextType.TEXT)]
        
    #     children = []
    #     for node in text_nodes:
    #         children.append(text_node_to_html_node(node))

    #     if block_type == BlockType.CODE:
    #         block_nodes.append(ParentNode("blockquote", children))
    #     if block_type == BlockType.HEADING:
    #         h = 0
    #         while block[h] == "#":
    #             h += 1
    #         block_nodes.append(ParentNode(f"h{h}", children))
        
    # print(block_nodes)

            
