import shutil
import os
from textnode import TextType, TextNode 

def main():
    test_node = TextNode("This is some anchor text", TextType("link"), "https://www.boot.dev")

    generate_public()

def generate_public():
    source = os.path.abspath("./static")
    destination = os.path.abspath("./public")

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

if __name__ == "__main__":
    main()