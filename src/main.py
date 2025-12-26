import shutil
import os
from textnode import TextType, TextNode
from markdown_to_blocks import markdown_to_html_node

destination_path = "./public"
source_path = "./static"
template_path = "template.html"
content_path = "content/index.md"

def main():
    test_node = TextNode("This is some anchor text", TextType("link"), "https://www.boot.dev")

    generate_public()
    generate_page(content_path, template_path, destination_path)

def generate_public():
    source = os.path.abspath(source_path)
    destination = os.path.abspath(destination_path)

    if os.path.exists(destination):
        shutil.rmtree("./public/")
    
    os.mkdir(destination)
    copy_source_to_destination(source, destination)    
    
def copy_source_to_destination(source, destination):
    source_content = os.listdir(source)

    for el in source_content:
        abs_el_path = os.path.join(source, el)
        if os.path.isfile(abs_el_path):
            shutil.copy(abs_el_path, destination)
        else:
            abs_dest_path = os.path.join(destination, el)
            os.mkdir(abs_dest_path)
            copy_source_to_destination(abs_el_path, abs_dest_path)
    return 

def extract_title(markdown):
    if markdown.startswith("#"):
        return (markdown.split("\n"))[0][2:].strip()
    else: 
        raise Exception("title not found")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as f:
        markdown_file = f.read()
    
    with open(template_path) as f:
        template_file = f.read()

    html_str = markdown_to_html_node(markdown_file).to_html()
    title_str = extract_title(markdown_file)
    html_file = template_file.replace("{{ Title }}", title_str).replace("{{ Content }}", html_str)

    if not os.path.exists(dest_path):
        os.makedirs("public")
    shutil.copy(template_path, dest_path+"/index.html")

    with open(dest_path+"/index.html", "w") as f:
        f.write(html_file)


if __name__ == "__main__":
    main()