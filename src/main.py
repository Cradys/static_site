import os
import shutil
from textnode import TextType, TextNode 

def main():
    if os.path.exists("./public"):
        print("deleting ./public")
        shutil.rmtree("./public")

if __name__ == "__main__":
    main()