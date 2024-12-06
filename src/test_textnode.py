import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node, text_to_textnodes



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_difference(self):
        node = TextNode("Text A", TextType.LINK, url="http://example.com")
        node2 = TextNode("Text B", TextType.LINK, url="http://different.com")
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("Text A", TextType.LINK, url=None)
        self.assertIsNone(node.url)

    def test_text_difference(self):
        node = TextNode("Text A", TextType.TEXT)
        node2 = TextNode("Text B", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_equal_with_none_url(self):
        node = TextNode("Some text", TextType.BOLD, url=None)
        node2 = TextNode("Some text", TextType.BOLD, url=None)
        self.assertEqual(node, node2)

    def test_not_eq_text_type(self):
        nodes = [
        TextNode("This is a text node", TextType.BOLD),
        TextNode("This is a text node", TextType.ITALIC),
        TextNode("This is a text node", TextType.TEXT),
        TextNode("This is a text node", TextType.LINK),
        TextNode("This is a text node", TextType.CODE),
        TextNode("This is a text node", TextType.IMAGE),
    ]
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                self.assertNotEqual(nodes[i], nodes[j])

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Click me", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_split_nodes_delimiter_basic(self):
        node = TextNode("Hello `world` today", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 3)

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("Hello `world` and `python`", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 5)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(nodes[1].text_type, TextType.BOLD)

    def test_split_nodes_delimiter_missing(self):
        node = TextNode("Hello `world today", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_without(self):
        text = "Просто текст без разметки."
        expected = [TextNode("Просто текст без разметки.", TextType.TEXT)]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_bold(self):
        text = "Это **жирный** текст."
        expected = [TextNode("Это ", TextType.TEXT), TextNode("жирный", TextType.BOLD), TextNode(" текст.", TextType.TEXT)]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_italic(self):
        text = "Это *курсив* текст."
        expected = [TextNode("Это ", TextType.TEXT), TextNode("курсив", TextType.ITALIC), TextNode(" текст.", TextType.TEXT)]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)



if __name__ == "__main__":
    unittest.main()