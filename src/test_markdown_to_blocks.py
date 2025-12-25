import unittest
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        heading1 = "# heading"
        heading6 = "###### heading"
        code = "```\ncode code\n```"
        quote = "> Quote\n> Next\n> Last"
        unordered_list = "- This is a list\n- with items"
        ordered_list = "1. ordered_list\n2. order \n3. last"
        paragraph = "some text\n text\n tttteeeeexxxttt"

        self.assertEqual(block_to_block_type(heading1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading6), BlockType.HEADING)
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(unordered_list), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(ordered_list), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
        
    def test_heading(self):
        md = """
# Heading 1

## Heading + **bold** here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading + <b>bold</b> here</h2></div>",
    )
        
    def test_quotes(self):
        md = """
> some text
>
> some _italic_ and end

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>some text some <i>italic</i> and end</blockquote></div>",
    )

    def test_unordered_list(self):
        md = """
- Item 1
- Item **bold**
- Item _italic_
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item <b>bold</b></li><li>Item <i>italic</i></li></ul></div>",
    )

    def test_ordered_list(self):
        md = """
1. Item 1
2. Item **bold**
3. Item _italic_
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item <b>bold</b></li><li>Item <i>italic</i></li></ol></div>",
    )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )
    
if __name__ == "__main__":
    unittest.main()