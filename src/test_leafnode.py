import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
   class TestLeafNode(unittest.TestCase):
    def test_props_to_html(self):
        node = LeafNode(tag="a", value="Link", props={"href": "https://www.example.com", "target": "_blank"})

    def test_repr(self):
        node = LeafNode(tag="p", value="Hello", props={"class": "text"})
        expected_repr = "HTMLNode(tag=p, value=Hello, props={'class': 'text'})"
        self.assertEqual(repr(node), expected_repr)

    def test_empty_props(self):
       node = LeafNode(tag="em", value="Italic", props={})
       self.assertEqual(node.to_html(), "<em>Italic</em>")


if __name__ == '__main__':
    unittest.main()