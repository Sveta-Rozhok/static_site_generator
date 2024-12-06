import unittest
from markdown_processor import markdown_to_html_node, extract_title
from markdown_processor import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_olist,
    block_type_ulist,
    block_type_quote,
)
from htmlnode import HTMLNode

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_markdown_to_html_node_empty_input(self):
        result = markdown_to_html_node("")
        self.assertEqual(result.tag, "div")
        self.assertTrue(isinstance(result.children, list))
        self.assertEqual(len(result.children), 0)

    def test_heading(self):
        text = "# This is text"
        result = markdown_to_html_node(text)
        
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].value, "This is text")
    

    def test_paragraph(self):
        text = "This is text"
        result = markdown_to_html_node(text)
        self.assertEqual(result.children[0].tag, "p")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].value, "This is text")

    def test_unordered_list(self):
        text = """
        - Item 1\n- Item 2"""

        result = markdown_to_html_node(text)
        self.assertEqual(result.children[0].tag, "ul")
        self.assertEqual(len(result.children[0].children), 2)

        self.assertEqual(result.children[0].children[0].tag, "li")
        self.assertEqual(result.children[0].children[0].value, "Item 1")
    
        self.assertEqual(result.children[0].children[1].tag, "li")
        self.assertEqual(result.children[0].children[1].value, "Item 2")

    def test_ordered_list(self):
        text = "1. Item 1\n2. Item 2"
        result = markdown_to_html_node(text)
        self.assertEqual(result.children[0].tag, "ol")
        self.assertEqual(len(result.children[0].children), 2)

        self.assertEqual(result.children[0].children[0].tag, "li")
        self.assertEqual(result.children[0].children[0].value, "Item 1")
    
        self.assertEqual(result.children[0].children[1].tag, "li")
        self.assertEqual(result.children[0].children[1].value, "Item 2")
    

    def test_code(self):
        text = "```print('hello world')```"
        result = markdown_to_html_node(text)
 

        self.assertEqual(result.children[0].tag, "pre")
        self.assertEqual(len(result.children), 1)

        code_node = result.children[0].children[0]
        self.assertEqual(code_node.tag, "code")
        self.assertEqual(code_node.value, "print('hello world')")

    def test_quote(self):
        text = "> This is text"
        result = markdown_to_html_node(text)
        self.assertEqual(result.children[0].tag, "blockquote")

    def test_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
    
    def test_raise_exception_for_missing_header(self):
        with self.assertRaises(Exception) as context:
            extract_title("No header here")
        self.assertEqual(str(context.exception), "there is no header")

    def test_empty_header_after_pound(self):
        with self.assertRaises(Exception) as context:
            extract_title("#")
        
        self.assertEqual(str(context.exception), "there is no header")



if __name__ == "__main__":
    unittest.main()
