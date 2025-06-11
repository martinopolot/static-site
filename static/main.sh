#!/bin/bash

# Run tests
python3 -m unittest discover src -v

# Run main.py to generate site and copy static files
python3 main.py
# from textnode import TextNode, TextType
# def main():
#     node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
#     print(node)
# main()


# # # # Run tests
# # python3 -m unittest discover src -v

# # # Run main.py to generate site and copy static files
# # python3 main.py