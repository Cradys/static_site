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
default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    generate_public(source_dir_path, destination_dir_path)
    # generate_page(content_path, template_path, destination_path)
    generate_pages_recursive(content_dir_path, template_path, destination_dir_path, basepath)

if __name__ == "__main__":
    main()