import shutil
import os
from markdown_to_blocks import markdown_to_html_node
from pathlib import Path 

def extract_title(markdown):
    print(f"Extract title")
    for line in markdown.split("\n"):
        if line.startswith("# "):
            print(f"Extracted title: {line[2:]}")
            return line[2:]
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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")

    with open(template_path) as f:
        template = f.read()
        
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    
    
    
    for file in os.listdir(dir_path_content):
        dir_content = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)

        if os.path.isfile(dir_content):
            print(dir_content, file)
            with open(dir_content) as f:
                markdown_file = f.read()
            html = markdown_to_html_node(markdown_file).to_html()
            title = extract_title(markdown_file)
            template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

            to_file = open(dest_path, "w")
            to_file.write(template)
        else:
            
            generate_pages_recursive(dir_content, template_path, dest_path)
    return