import re 
from textnode import TextType, TextNode

def extract_markdown_images(text):
    img_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result = re.findall(img_pattern, text)
    return result

def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result = re.findall(link_pattern, text)
    return result

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            result.append(node)
        else:
            for image_alt, image_url in images:
                sections = node.text.split(f"![{image_alt}]({image_url})", 1)
                if sections[0]:
                    result.append(TextNode(sections[0], TextType.TEXT))
                result.append(TextNode(image_alt, TextType.IMAGE, image_url))
                if sections[1]:
                    result.append( TextNode(sections[1], TextType.TEXT))
    return result


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            result.append(node)
        else:
            for links_text, links_url in links:
                sections = node.text.split(f"[{links_text}]({links_url})", 1)
                if sections[0]:
                    result.append(TextNode(sections[0], TextType.TEXT))
                result.append(TextNode(links_text, TextType.LINK, links_url))
                if sections[1]:
                    result.append( TextNode(sections[1], TextType.TEXT))

    return result
