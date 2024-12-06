import unittest

from extract_links import extract_markdown_images, extract_markdown_links, split_nodes_link
from textnode import TextNode, TextType

class TestMarkdownExtraction(unittest.TestCase):
    def test_one_img(self):
        text = "This is text with a ![example](http://example.com/image.png)"
        expected = [("example", "http://example.com/image.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_link(self):
        text = "This is text with a [example](https://www.boot.dev)"
        expected = [("example", "https://www.boot.dev")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_links(self):
        text = "Check [Google](https://www.google.com) and [Boot.dev](https://www.boot.dev)"
        expected = [("Google", "https://www.google.com"), ("Boot.dev", "https://www.boot.dev")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_img_link(self):
        text = "Here is an ![image](http://example.com/image.png) and a [link](http://example.com)"
        expected_links = [("link", "http://example.com")]
        result_links = extract_markdown_links(text)
        self.assertEqual(result_links, expected_links)

        expected_images = [("image", "http://example.com/image.png")]
        result_images = extract_markdown_images(text)
        self.assertEqual(result_images, expected_images)

    def test_split_nodes_basic(self):
        node = TextNode("This is a [link](https://example.com)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].url, "https://example.com")

    def test_split_nodes_empty(self):
        node = TextNode("", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "")
    
    def test_split_nodes_no_links(self):
        node = TextNode("Plain text without links", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Plain text without links")

 
if __name__ == "__main__":
    unittest.main()