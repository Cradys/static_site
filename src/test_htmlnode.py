import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.node = HTMLNode("<b>", "bob", "ddddd", {"href": "www/www"})
        self.node2 = HTMLNode("<b>", "bob", "ddddd")

    def test_props_to_html(self):
        self.assertEqual(self.node.props_to_html(), ' href="www/www"')
        self.assertEqual(self.node2.props_to_html(), "")
    
    def test_to_html(self):
        with self.assertRaises(NotImplementedError) as e:
            self.node.to_html()
    
class TestLeafNode(unittest.TestCase):
    def setUp(self):
        self.node = LeafNode("b", "sometext")
        self.node2 = LeafNode("b", "sometext", {"href": "google.com"})        
    
    def test_leaf__values(self):
        self.assertEqual(self.node.value, self.node2.value)
        self.assertEqual(self.node.tag, self.node2.tag)
        self.assertNotEqual(self.node.props, self.node2.props)
    
    def test_leaf_to_html(self):
        self.assertEqual(self.node2.to_html(), '<b href="google.com">sometext</b>')
        self.node3 = LeafNode("", "sometext")
        self.assertEqual(self.node3.to_html(), "sometext")
        self.node3.value = ""
        with self.assertRaises(ValueError) as e:
            self.node3.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()

    def test_to_html_with_children_props(self):
        child_node = LeafNode("a", "child", {"href": "google.c"})
        parent_node = ParentNode("div", [child_node], {"class": "check"})
        self.assertEqual(parent_node.to_html(), '<div class="check"><a href="google.c">child</a></div>')

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

if __name__ == "__main__":
    unittest.main()
