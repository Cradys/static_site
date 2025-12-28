import shutil
import os
import sys
from textnode import TextType, TextNode
from markdown_to_blocks import markdown_to_html_node
from static_to_public import generate_public
from pages_generator import generate_pages_recursive

destination_dir_path = "./docs"
source_dir_path = "./static"
template_path = "./template.html"
content_dir_path = "./content"

basepath = sys.argv[0]
if basepath == "src/main.py" or not basepath:
    basepath = "/"
print(f"basepath ---- {basepath}")

def main():
    test_node = TextNode("This is some anchor text", TextType("link"), "https://www.boot.dev")

    generate_public(source_dir_path, destination_dir_path)
    # generate_page(content_path, template_path, destination_path)
    generate_pages_recursive(content_dir_path, template_path, destination_dir_path, basepath)

if __name__ == "__main__":
    main()