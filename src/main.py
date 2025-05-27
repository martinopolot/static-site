from textnode import TextNode, TextType

def main():
    node = TextNode("This is some archor text", TextType.LINK, "https://wwwboot.dev")
    print(node)

#print("hello world")
main()


