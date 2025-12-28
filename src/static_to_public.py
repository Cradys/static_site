import shutil
import os

def generate_public(source_path, destination_path):
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