import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_without_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(tag=None, children=[], props={"class": "text"})

    def test_without_children(self):
        child_node = ParentNode(tag="span", children=[LeafNode(None, "Child text")], props={})
        node = ParentNode(tag="div", children=[child_node], props={"class": "text"})
        self.assertEqual(node.to_html(), '<div class="text"><span>Child text</span></div>')

    def test_parentnode_in_parentnode(self):
        child_node = ParentNode(tag="span", children=[], props={})
        node = ParentNode(tag="div", children=[child_node], props={"class": "text"})
        self.assertEqual(node.to_html(), '<div class="text"><span></span></div>')

    def test_to_html_with_children(self):
        child1 = LeafNode("b", "Bold text", {})
        child2 = LeafNode(None, "Normal text", {})
        child3 = LeafNode("i", "italic text", {})
        child4 = LeafNode(None, "Normal text", {})
        node = ParentNode(tag="p", children=[child1, child2, child3, child4], props={})
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_children_with_and_without_tags(self):
        child_with_tag = LeafNode("strong", "Text with tag",  {"some_prop": "value"})
        child_without_tag = LeafNode(None, "Text without tag", {"some_prop": "value"})
        node = ParentNode(tag="div", children=[child_with_tag, child_without_tag], props={})
        expected_html = '<div><strong some_prop="value">Text with tag</strong>Text without tag</div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_props_in_constructor(self):
        props = {"class": "test-class", "id": "unique-id"}
        node = ParentNode(tag="section", children=[], props=props)
        self.assertEqual(node.props, props)

if __name__ == "__main__":
    unittest.main()